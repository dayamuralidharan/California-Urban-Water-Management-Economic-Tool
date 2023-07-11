# Script defining the CostProblem and OptimizeWMOs classes

#!pip install numpy matplotlib pymoo

#from IPython.core.debugger import set_trace

import matplotlib.pyplot as plt
import matplotlib as mpl
import numpy as np
import time
import warnings

from pymoo.core.problem import ElementwiseProblem
from pymoo.algorithms.soo.nonconvex.pso import PSO
from pymoo.termination import get_termination
from pymoo.optimize import minimize

from src.modelLogic.modelLogic import ModelLogic
from src.modelLogic.inputData import InputData
from src.modelLogic.storageUtilities import StorageUtilities
from src.modelLogic.inputDataLocations import InputDataLocations

warnings.filterwarnings('ignore')  # turn off warnings

### PyMoo Optimization Problem Class ###

class CostProblem(ElementwiseProblem): 
    '''
    This class is a PyMoo problem class designed to simulate the effects of longtermWMOSupply levels...
    ...on water usage cost optimization (economicLoss) for a given contractor. 
    The objective space of F(X) is mapped by an algorithm, within the u/l bounds for each dimension of X.
    Optionally, F(X) can be constrained by inequality constraints G(X): 
       + g1(x) > wmoFloor  :: defines a floor value of the sum( longtermWMOSupply ) 
       + g2(x) < wmoSupply :: defines a ceiling value of the sum( longtermWMOSupply )
    https://pymoo.org/
    '''
    def __init__(self, 
                 lowerBounds: list,          # lower bound of each longtermWMO type for a given scenario - len(list)=8
                 upperBounds: list,          # upper bound of each longtermWMO type for a given scenario - len(list)=8
                 modelLogic: ModelLogic,     # prepared ModelLogic object with InputData and StorageUtilities
                 wmoFloor=None,              # how low are we constraining the sum longtermWMOs?
                 wmoSupply=None,             # how high are we constraining the sum longtermWMOs?
                 **kwargs):    
        '''
        Initializing the CostProblem class requires parameterizing a CaUWMET model for a given contractor.
        Inputs:
            wmoFloor/wmoSupply :: number > 0, max sum of the longtermWMO allocations
            lowerBounds/upperBounds :: list of numbers, length 8
            modelLogic :: ModelLogic object loaded with InputData, StorageUtilities, and Contractor
        '''
        self.wmoFloor = wmoFloor if wmoFloor is not None else None
        self.wmoSupply = wmoSupply if wmoSupply is not None else None
        self.n_ieq_constr = sum([i != None for i in [self.wmoFloor, self.wmoSupply]]) #TODO: Recommend making name clearer
        self.lowerBounds = lowerBounds
        self.upperBounds = [ ub if ub>0 else 0.01 for ub in upperBounds ]
        self.objectiveFunction = modelLogic.executeModelLogicForContractor
        
        super().__init__(  # parameterize the objective function
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
        tic = time.perf_counter()
        if self.n_ieq_constr > 0:
            out["F"] = self.objectiveFunction(x)
            G1 = self.wmoFloor - np.sum(x)   # np.sum(x) >= self.wmoFloor
            G2 = np.sum(x) - self.wmoSupply  # self.wmoSupply >= np.sum(x)
            out["G"] = [G1, G2]
        else:
            out["F"] = self.objectiveFunction(x)
        toc = time.perf_counter()
        

### instantiate CaUWMET model and execute MOO problem ###

class OptimizeWMOs:
    '''
    This class parameterizes, executes, and reports the optimization results of the CostProblem() class.
    Parameterizing the contractor prepares a ModelLogic object, and the year sets the longtermWMO Volumelimits (upper bounds).
    The other inputs are used to execute the PyMoo optimization. Results are stored and accessed for visualization methods. 
    TODO: Need to handle class inheritance better
    '''
    def __init__(self, 
                 year='2045', 
                 contractor='Metropolitan Water District of Southern California',
                 wmoFloor=None, 
                 wmoSupply=None, 
                 lowerBounds=[0]*8, 
                 upperBounds='longtermWMOVolumeLimits'):
        
        self.inputData = InputData(InputDataLocations())
        self.modelLogic = ModelLogic(self.inputData, StorageUtilities())
        self.modelLogic.contractor = contractor
        self.wmoFloor = wmoFloor
        self.wmoSupply = wmoSupply
        self.lowerBounds = lowerBounds
        self.upperBounds = upperBounds if upperBounds != 'longtermWMOVolumeLimits' else [
            self.inputData.longtermWMOSurfaceVolumeLimit[self.inputData.longtermWMOSurfaceVolumeLimit.index==contractor][year][0],
            self.inputData.longtermWMOGroundwaterVolumeLimit[self.inputData.longtermWMOGroundwaterVolumeLimit.index==contractor][year][0],
            self.inputData.longtermWMODesalinationVolumeLimit[self.inputData.longtermWMODesalinationVolumeLimit.index==contractor][year][0],
            self.inputData.longtermWMORecycledVolumeLimit[self.inputData.longtermWMORecycledVolumeLimit.index==contractor][year][0],
            self.inputData.longtermWMOPotableReuseVolumeLimit[self.inputData.longtermWMOPotableReuseVolumeLimit.index==contractor][year][0],
            self.inputData.longtermWMOTransfersExchangesVolumeLimit[self.inputData.longtermWMOTransfersExchangesVolumeLimit.index==contractor][year][0],
            self.inputData.longtermWMOOtherSupplyVolumeLimit[self.inputData.longtermWMOOtherSupplyVolumeLimit.index==contractor][year][0],
            self.inputData.longtermWMOConservationVolumeLimit[self.inputData.longtermWMOConservationVolumeLimit.index==contractor][year][0],
        ]
        
    
    def optimize(self):
        '''
        This method parameterizes the CostProblem and executes the PyMoo optimization. 
        The optimization algorithm and termination criteria are hardcoded for now...
        '''
        # parameterize the problem
        problem = CostProblem(
            modelLogic=self.modelLogic,
            wmoFloor=self.wmoFloor, wmoSupply=self.wmoSupply, 
            lowerBounds=self.lowerBounds, upperBounds=self.upperBounds
        )
        # parameterize algorithm
        algorithm = PSO(
            pop_size=10,
            w=0.9, c1=5.0, c2=1.0,
            adaptive=True,
            max_velocity_rate=0.2
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

        print("Best solution found: \nX = %s\nF = %s" % (self.res.X, self.res.F))
        
        return self.res
        
        
    def visualization_a(self):
        '''
        This method can be called after the self.res object has been created by the optimize() method. 
        Accessing the optimization history in self.res allows for plotting of the optimization search results.
        
        '''
        # get the particles - this should be its own self callable method...
        X = []
        F = []
        try:
            for h in self.res.history:
                for p in h.particles:
                    X.append(p._X)
                    F.append(p._F)
        except: 
            print("Couldn't get particles. Aborting...")
        
        # assign plot variables
        TAF = np.sum(X,axis=1)  # sum of longtermWMOSupply variables
        loss_millions = [f*10**-6 for f in F]
        colors = [ item for item in list(range(len(self.res.history))) for i in range(len(self.res.pop)) ]  # this only works for the n_gen=5 because of this....

        # matplotlib
        fig, ax = plt.subplots(1, 1, figsize=(6, 6))          # setup the plot
        cmap = plt.cm.viridis                                 # define the colormap
        cmaplist = [cmap(i) for i in range(cmap.N)]           # extract all colors from map
        cmap = mpl.colors.LinearSegmentedColormap.from_list(  # create the new map
            'Custom cmap', cmaplist, cmap.N
        )
        bounds = np.linspace(0, len(self.res.history), len(self.res.history)+1)   # define the bins
        norm = mpl.colors.BoundaryNorm(bounds, cmap.N)        # normalize

        ax.scatter(TAF, loss_millions, c=colors, cmap=cmap, norm=norm, alpha=0.5)
        ax.set_title("Particle Costs evaluated in Optimization History\nOptimal Point shown in Red")
        ax.set_xlabel("Sum of longtermWMO Supply variables")
        ax.set_ylabel("Total Economic Losses ($ Million)")
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
        
        return ax


        