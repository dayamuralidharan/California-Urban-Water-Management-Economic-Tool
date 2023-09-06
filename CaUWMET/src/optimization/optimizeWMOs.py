# Script defining the OptimizeWMOs class

import matplotlib.pyplot as plt
import matplotlib as mpl
import numpy as np
import pandas as pd
import warnings

from pymoo.algorithms.soo.nonconvex.pso import PSO
from pymoo.termination import get_termination
from pymoo.optimize import minimize

from src.modelLogic.modelLogic import ModelLogic
from src.optimization.costProblem import CostProblem

warnings.filterwarnings('ignore')  # turn off warnings

### Optimize CaUWMET Model Longterm WMOs Class ###

# TODO: Need to handle class inheritance better
class OptimizeWMOs:
    '''
    This class parameterizes, executes, and reports the optimization results of the CostProblem() class.
    Parameterizing the contractor prepares a ModelLogic object, and the year sets the longtermWMO Volumelimits (upper bounds).
    The other inputs are used to execute the PyMoo optimization. Results are stored and accessed for visualization methods. 
    '''
    def __init__(self, 
                 verbose=False,
                 modelLogic=ModelLogic,
                 contractor='City of Tracy',
                 wmoFloor=None,
                 wmoCeiling=None,
                 lowerBounds=[0]*8,
                 upperBounds='longtermWMOVolumeLimits',
                 zero_threshold=1):
        self.verbose = verbose
        self.zero_threshold = zero_threshold
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
            lowerBounds=self.lowerBounds, upperBounds=self.upperBounds,
            zero_threshold=self.zero_threshold
        )
        
        # parameterize algorithm
        algorithm = PSO(  # TODO: enable users to play with hyperparameters????
            pop_size=20,
            w=0.8, c1=10.0, c2=1.0,
            adaptive=True,
            max_velocity_rate=0.3
        )
        # parameterize the termination criteria
        termination = get_termination("n_gen", 20)  # TODO: enable ftol termination
        
        # execute optimization
        self.res = minimize(
            problem, 
            algorithm, 
            termination, 
            seed=42, 
            verbose=self.verbose,
            save_history=True
        )
        
        # zero the X values below the zero_threshold
        # because this is what is happening at CostProblem._evaluate()
        self.X = [ 0 if x < self.zero_threshold else x for x in self.res.X ]
        self.F = self.modelLogic.execute(self.X)

        print("Best solution found: \nX = %s\nF = %s" % (self.X, self.F))
        print(f"Execution time: {round(self.res.exec_time)} seconds")
        
        if result: 
            return self.res
    
    
    def reportBest(self):
        '''
        This method reports the X values, 0'd below the zero_threshold, and the new F value.
        Note: 
            Must be run after .optimize method!
        '''
        return self.X, self.F


    def reportZero(self):
        '''
        This method 0's out all the X values, then recomputes the new F value.
        Note: 
            Must be run after .optimize method!
        '''
        self.X = [0]*len(self.X)
        self.F = self.modelLogic.execute(self.X)
        return self.X, self.F
    
    
    def exportResults(self):
        '''
        This method exports the results of the output handlers for aggregation into a table. 
        Note: 
            Must be run after .optimize method!
        '''
        modelOutputs = {
            'longtermWMOVolumeLimits': pd.DataFrame(data={
                self.modelLogic.contractor: self.upperBounds
            }),
            'longtermWMOOptimizedVolumes': pd.DataFrame(data={
                self.modelLogic.contractor: self.X
            }),

        # Outputs
        # Water Balance Outputs
            'SWPCVPSupplyDelivery': self.modelLogic.outputHandler.SWPCVPSupplyDelivery[self.modelLogic.contractor], # (acre-feet/year)
            'excessSupply': self.modelLogic.outputHandler.excessSupply[self.modelLogic.contractor], # (acre-feet/year)
            'unallocatedSWPCVPDeliveries': self.modelLogic.outputHandler.unallocatedSWPCVPDeliveries[self.modelLogic.contractor], # (acre-feet/year)
            'putSurface': self.modelLogic.outputHandler.putSurface[self.modelLogic.contractor], # (acre-feet/year)
            'putGroundwater': self.modelLogic.outputHandler.putGroundwater[self.modelLogic.contractor], # (acre-feet/year)
            'volumeSurfaceCarryover': self.modelLogic.outputHandler.volumeSurfaceCarryover[self.modelLogic.contractor], # (acre-feet)
            'volumeGroundwaterBank': self.modelLogic.outputHandler.volumeGroundwaterBank[self.modelLogic.contractor], # (acre-feet)
            'waterMarketTransferDeliveries': self.modelLogic.outputHandler.waterMarketTransferDeliveries[self.modelLogic.contractor], # ($)
            'totalShortage': self.modelLogic.outputHandler.totalShortage[self.modelLogic.contractor], # (acre-feet/year)

            # Cost Outputs
            # Total Costs
            'totalAnnualCost': self.modelLogic.outputHandler.totalAnnualCost[self.modelLogic.contractor], # ($)
            'totalEconomicLoss': self.modelLogic.outputHandler.totalEconomicLoss[self.modelLogic.contractor], # ($)
            'totalReliabilityMgmtCost': self.modelLogic.outputHandler.totalReliabilityMgmtCost[self.modelLogic.contractor], # ($)

            # WMO Costs
            'waterMarketTransferCost': self.modelLogic.outputHandler.waterMarketTransferCost[self.modelLogic.contractor], # ($)

            'surfaceLongTermWMOCost': self.modelLogic.outputHandler.surfaceLongTermWMOCost[self.modelLogic.contractor], # ($)
            'groundwaterLongTermWMOCost': self.modelLogic.outputHandler.groundwaterLongTermWMOCost[self.modelLogic.contractor], # ($)
            'desalinationLongTermWMOCost': self.modelLogic.outputHandler.desalinationLongTermWMOCost[self.modelLogic.contractor], # ($)
            'recycledLongTermWMOCost': self.modelLogic.outputHandler.recycledLongTermWMOCost[self.modelLogic.contractor], # ($)
            'potableReuseLongTermWMOCost': self.modelLogic.outputHandler.potableReuseLongTermWMOCost[self.modelLogic.contractor], # ($)
            'transfersAndExchangesLongTermWMOCost': self.modelLogic.outputHandler.transfersAndExchangesLongTermWMOCost[self.modelLogic.contractor], # ($)
            'otherSupplyLongTermWMOCost': self.modelLogic.outputHandler.otherSupplyLongTermWMOCost[self.modelLogic.contractor], # ($)
            'conservationLongTermWMOCost': self.modelLogic.outputHandler.conservationLongTermWMOCost[self.modelLogic.contractor], # ($)

            #System operations costs
            'swpCVPDeliveryCost': self.modelLogic.outputHandler.swpCVPDeliveryCost[self.modelLogic.contractor], # ($)
            'putGroundwaterBankCost': self.modelLogic.outputHandler.putGroundwaterBankCost[self.modelLogic.contractor], # ($)
            'takeGroundwaterBankCost': self.modelLogic.outputHandler.takeGroundwaterBankCost[self.modelLogic.contractor], # ($)
            'groundwaterPumpingSavings': self.modelLogic.outputHandler.groundwaterPumpingSavings[self.modelLogic.contractor], # ($)
            'waterTreatmentCost': self.modelLogic.outputHandler.waterTreatmentCost[self.modelLogic.contractor], # ($)
            'distributionCost': self.modelLogic.outputHandler.distributionCost[self.modelLogic.contractor], # ($)
            'wastewaterTreatmentCost': self.modelLogic.outputHandler.wastewaterTreatmentCost[self.modelLogic.contractor], # ($)
        }
        
        # QAQC Results
        qaqcResults = {
            'totalAnnualCost': self.modelLogic.outputHandler.totalAnnualCost[self.modelLogic.contractor], # ($)
            'totalEconomicLoss': self.modelLogic.outputHandler.totalEconomicLoss[self.modelLogic.contractor], # ($)
            'appliedDemands': self.modelLogic.outputHandler.appliedDemands[self.modelLogic.contractor], # (acre-feet/year)
            'demandsToBeMetByStorage': self.modelLogic.outputHandler.demandsToBeMetByStorage[self.modelLogic.contractor], # (acre-feet/year)
            'volumeGroundwaterBank': self.modelLogic.outputHandler.volumeGroundwaterBank[self.modelLogic.contractor], # (acre-feet/year)
            'takeGroundwater': self.modelLogic.outputHandler.takeGroundwater[self.modelLogic.contractor], # (acre-feet/year)
            'putGroundwater': self.modelLogic.outputHandler.putGroundwater[self.modelLogic.contractor], # (acre-feet/year)
            'demandsToBeMetByContingentOptions': self.modelLogic.outputHandler.demandsToBeMetByContingentOptions[self.modelLogic.contractor], # (acre-feet/year)
            'contingentConservationReductionVolume': self.modelLogic.outputHandler.contingentConservationReductionVolume[self.modelLogic.contractor], # (acre-feet/year)
            'waterMarketTransferDeliveries': self.modelLogic.outputHandler.waterMarketTransferDeliveries[self.modelLogic.contractor], # (acre-feet/year)
            'totalShortage': self.modelLogic.outputHandler.totalShortage[self.modelLogic.contractor], # (acre-feet/year)
        }
        
        return modelOutputs, qaqcResults


    def visualization_a(self, save=False):
        '''
        This method can be called after the self.res object has been created by the optimize() method. 
        Accessing the optimization history in self.res allows for plotting of the optimization search results.
        Note: 
            Must be run after .optimize method!
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
        loss_millions = [ f*10**-6 for f in F ]
        
        # matplotlib
        fig, ax = plt.subplots(1, 1, figsize=(6, 6))          # setup the plot
        cmap = plt.cm.viridis                                 # define the colormap
        cmaplist = [ cmap(i) for i in range(cmap.N) ]           # extract all colors from map
        cmap = mpl.colors.LinearSegmentedColormap.from_list(  # create the new map
            'Custom cmap', cmaplist, cmap.N
        )
        bounds = np.linspace(0, len(self.res.history), len(self.res.history)+1)   # define the bins
        norm = mpl.colors.BoundaryNorm(bounds, cmap.N)        # normalize
        
        # define scatter plot axes
        ax.scatter(TAF, loss_millions, c=colors, cmap=cmap, norm=norm, alpha=0.5)
        ax.set_title("Particle Costs evaluated in Optimization History\nOptimal Point shown in Red")
        ax.set_xlabel("Sum of Long-term Water Management Option Fixed Yield Augmentation (acre-feet/year")
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
        ax.scatter(x=sum(self.res.X), y=self.res.F*10**-6, c='red', marker="o")
        ## TODO: fix - this one doesn't show on the log-x plots and messes up the y axis....
        #ax.scatter(x=sum(self.X_zero), y=self.F_zero, c='red', marker="*", edgecolors='red')
        
        if save:
            population = self.res.algorithm.pop_size
            n_iter = self.res.algorithm.n_iter
            start_time = round(self.res.algorithm.start_time)
            contractor = self.modelLogic.contractor.replace(" ", "")
            year = self.modelLogic.inputData.futureYear
            figname = f'graphics/{contractor}-{year}_optimization_p-{population}_n-{n_iter}_{start_time}.png'
            plt.savefig(figname) # TODO: configure png so it doesn't cut off data for some plots
            return figname
        else: 
            plt.show()


