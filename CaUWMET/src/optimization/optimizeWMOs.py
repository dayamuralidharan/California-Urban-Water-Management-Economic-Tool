# Script defining the CostProblem and OptimizeWMOs classes

#!pip install numpy matplotlib pymoo

#from IPython.core.debugger import set_trace

import matplotlib.pyplot as plt
import matplotlib as mpl
import numpy as np
import warnings

from pymoo.core.problem import ElementwiseProblem
from pymoo.algorithms.soo.nonconvex.pso import PSO
from pymoo.termination import get_termination
from pymoo.optimize import minimize

from src.modelLogic.modelLogic import ModelLogic

warnings.filterwarnings('ignore')  # turn off warnings

### PyMoo Optimization Problem Class ###

class CostProblem(ElementwiseProblem): 
    '''
    This class is a PyMoo problem class designed to simulate the effects of longtermWMOSupply levels...
    ...on water usage cost optimization (economicLoss) for a given contractor. 
    The objective space of F(X) is mapped by an algorithm, within the u/l bounds for each dimension of X.
    Optionally, F(X) can be constrained by inequality constraints G(X): 
       + g1(x) > wmoFloor  :: defines a floor value of the sum( longtermWMOSupply ) 
       + g2(x) < wmoCeiling :: defines a ceiling value of the sum( longtermWMOSupply )
    https://pymoo.org/
    '''
    def __init__(self, 
                 lowerBounds: list,          # lower bound of each longtermWMO type for a given scenario - len(list)=8
                 upperBounds: list,          # upper bound of each longtermWMO type for a given scenario - len(list)=8
                 modelLogic: ModelLogic,     # prepared ModelLogic object with InputData and StorageUtilities
                 wmoFloor=None,              # how low are we constraining the sum longtermWMOs?
                 wmoCeiling=None,            # how high are we constraining the sum longtermWMOs?
                 **kwargs):    
        '''
        Initializing the CostProblem class requires parameterizing a CaUWMET model for a given contractor.
        Inputs:
            wmoFloor/wmoCeiling :: number > 0, max sum of the longtermWMO allocations
            lowerBounds/upperBounds :: list of numbers, length 8
            modelLogic :: ModelLogic object loaded with InputData, StorageUtilities, and Contractor
        '''
        self.wmoFloor = wmoFloor if wmoFloor is not None else None
        self.wmoCeiling = wmoCeiling if wmoCeiling is not None else None
        self.n_ieq_constr = sum([i != None for i in [self.wmoFloor, self.wmoCeiling]]) #TODO: Recommend making name clearer
        self.lowerBounds = lowerBounds
        self.upperBounds = [ ub if ub>0 else 0.0001 for ub in upperBounds ]  #TODO: refine how the upper bound 0 vals are handled
        self.objectiveFunction = modelLogic.execute
        
        # parameterize the objective function
        super().__init__(
            n_var=8, n_obj=1, n_ieq_constr=self.n_ieq_constr, 
            xl=self.lowerBounds, xu=self.upperBounds,  # xl and xu set longtermWMOSupply bounds 
            **kwargs
        )


    def _evaluate(self, x, out, *args, **kwargs):
        '''
        Inputs:
           x :: list of numbers, length 8
        Returns objective function f(x)
        Returns inequality constraints g(x)
        '''
        if self.n_ieq_constr > 0:
            out["F"] = self.objectiveFunction(x)
            G1 = self.wmoFloor - np.sum(x) if self.wmoFloor is not None else None       # np.sum(x) >= self.wmoFloor
            G2 = np.sum(x) - self.wmoCeiling  if self.wmoCeiling is not None else None  # self.wmoCeiling >= np.sum(x)
            out["G"] = [ g for g in [G1,G2] if g is not None ]
        else:
            out["F"] = self.objectiveFunction(x)


### instantiate CaUWMET model and execute MOO problem ###

class OptimizeWMOs:
    '''
    This class parameterizes, executes, and reports the optimization results of the CostProblem() class.
    Parameterizing the contractor prepares a ModelLogic object, and the year sets the longtermWMO Volumelimits (upper bounds).
    The other inputs are used to execute the PyMoo optimization. Results are stored and accessed for visualization methods. 
    TODO: Need to handle class inheritance better
    '''
    def __init__(self, 
                 contractor='City of Tracy',
                 modelLogic=ModelLogic,
                 wmoFloor=None,
                 wmoCeiling=None,
                 lowerBounds=[0]*8,
                 upperBounds='longtermWMOVolumeLimits'):
        
        self.modelLogic = modelLogic
        self.modelLogic.contractor = contractor
        self.wmoFloor = wmoFloor
        self.wmoCeiling = wmoCeiling
        self.lowerBounds = lowerBounds
        self.upperBounds = upperBounds if upperBounds != 'longtermWMOVolumeLimits' else [
            self.modelLogic.inputData.longtermWMOConservationVolumeLimit[self.modelLogic.inputData.longtermWMOConservationVolumeLimit.index==contractor][self.modelLogic.inputData.futureYear][0],
            self.modelLogic.inputData.longtermWMOSurfaceVolumeLimit[self.modelLogic.inputData.longtermWMOSurfaceVolumeLimit.index==contractor][self.modelLogic.inputData.futureYear][0],
            self.modelLogic.inputData.longtermWMOGroundwaterVolumeLimit[self.modelLogic.inputData.longtermWMOGroundwaterVolumeLimit.index==contractor][self.modelLogic.inputData.futureYear][0],
            self.modelLogic.inputData.longtermWMODesalinationVolumeLimit[self.modelLogic.inputData.longtermWMODesalinationVolumeLimit.index==contractor][self.modelLogic.inputData.futureYear][0],
            self.modelLogic.inputData.longtermWMORecycledVolumeLimit[self.modelLogic.inputData.longtermWMORecycledVolumeLimit.index==contractor][self.modelLogic.inputData.futureYear][0],
            self.modelLogic.inputData.longtermWMOPotableReuseVolumeLimit[self.modelLogic.inputData.longtermWMOPotableReuseVolumeLimit.index==contractor][self.modelLogic.inputData.futureYear][0],
            self.modelLogic.inputData.longtermWMOTransfersExchangesVolumeLimit[self.modelLogic.inputData.longtermWMOTransfersExchangesVolumeLimit.index==contractor][self.modelLogic.inputData.futureYear][0],
            self.modelLogic.inputData.longtermWMOOtherSupplyVolumeLimit[self.modelLogic.inputData.longtermWMOOtherSupplyVolumeLimit.index==contractor][self.modelLogic.inputData.futureYear][0],
        ]
    
    def optimize(self, result=False):
        '''
        This method parameterizes the CostProblem and executes the PyMoo optimization. 
        The optimization algorithm and termination criteria are hardcoded for now...
        '''
        # parameterize the problem
        problem = CostProblem(
            modelLogic=self.modelLogic,
            wmoFloor=self.wmoFloor, wmoCeiling=self.wmoCeiling, 
            lowerBounds=self.lowerBounds, upperBounds=self.upperBounds
        )
        
        # parameterize algorithm
        algorithm = PSO(  # TODO: enable users to play with hyperparameters????
            pop_size=20,
            w=0.8, c1=10.0, c2=1.0,
            adaptive=True,
            max_velocity_rate=0.3
        )
        # parameterize the termination criteria
        termination = get_termination("n_gen", 20)
        
        # execute optimization
        self.res = minimize(
            problem, 
            algorithm, 
            termination, 
            seed=42, 
            verbose=True,
            save_history=True
        )
        
        print("\nBest solution found: \nX = %s\nF = %s" % (self.res.X, self.res.F))
        print(f"Execution time: {round(self.res.exec_time)} seconds")
        
        if result: 
            return self.res
    
    
    # TODO: update code below to report values of the best option once integrated into model execution function
    # def report_best(self):
    #     X = self.res.X
    #     best_results = ModelLogic.execute(X, optimize=False)
    #     print(best_results)  # TODO: output to CSV
    #     return best_results
    
    
    # TODO: Replace pseudocode below to report values of a given
    # def report_custom(self, X):
        
        
    def visualization_a(self, save=False):
        '''
        This method can be called after the self.res object has been created by the optimize() method. 
        Accessing the optimization history in self.res allows for plotting of the optimization search results.
        '''
        # get the particles 
        # TODO: this could be its own method...
        X = []
        F = []
        colors = []
        c = 0
        try:
            for h in self.res.history:
                for p in h.particles:
                    if self.wmoCeiling is not None:
                        if np.sum(p._X) < self.wmoCeiling:
                            X.append(p._X)
                            F.append(p._F)
                            colors.append(c)
                    else: 
                        X.append(p._X)
                        F.append(p._F)
                        colors.append(c)
                c+=1
        except: 
            print("Couldn't get particles. Aborting...")
        
        # assign plot variables
        TAF = np.sum(X,axis=1)  # sum of longtermWMOSupply variables
        loss_millions = [f*10**-6 for f in F]
        
        # matplotlib
        fig, ax = plt.subplots(1, 1, figsize=(6, 6))          # setup the plot
        cmap = plt.cm.viridis                                 # define the colormap
        cmaplist = [cmap(i) for i in range(cmap.N)]           # extract all colors from map
        cmap = mpl.colors.LinearSegmentedColormap.from_list(  # create the new map
            'Custom cmap', cmaplist, cmap.N
        )
        bounds = np.linspace(0, len(self.res.history), len(self.res.history)+1)   # define the bins
        norm = mpl.colors.BoundaryNorm(bounds, cmap.N)        # normalize
        
        # define scatter plot axes
        ax.scatter(TAF, loss_millions, c=colors, cmap=cmap, norm=norm, alpha=0.5)
        ax.set_title("Particle Costs evaluated in Optimization History\nOptimal Point shown in Red")
        ax.set_xlabel("Sum of Long-term Water Management Option Fixed Yield Augmentation (acre-feet/year)")
        ax.set_xscale('log')
        ax.set_ylabel("Expected Costs and Losses ($ Million)")
        ax.ticklabel_format(axis="y", style="sci", useOffset=False)
        
        # create a second axes for the colorbar
        ax2 = fig.add_axes([0.95, 0.1, 0.03, 0.8])
        cb = mpl.colorbar.ColorbarBase(
            ax2, cmap=cmap, norm=norm,
            spacing='proportional', ticks=bounds, boundaries=bounds, format='%1i'
        )
        ax2.set_ylabel('Iteration Number', size=12)
        
        # plot the best result in red 
        ax.scatter(x=sum(self.res.X), y=self.res.F*10**-6, c='red')
        
        if save:
            population = self.res.algorithm.pop_size
            n_iter = self.res.algorithm.n_iter
            start_time = round(self.res.algorithm.start_time)
            contractor = self.modelLogic.contractor.replace(" ", "")
            year = self.modelLogic.inputData.futureYear
            figname = f'graphics/{contractor}-{year}_optimization_p-{population}_n-{n_iter}_{start_time}.png'
            plt.savefig(figname)
        else: 
            plt.show()


