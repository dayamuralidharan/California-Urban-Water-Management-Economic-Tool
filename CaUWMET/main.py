import logging

from src.modelLogic.modelLogic import ModelLogic
from src.modelLogic.inputData import InputData
from src.modelLogic.storageUtilities import StorageUtilities
from src.modelLogic.inputDataLocations import InputDataLocations

from src.optimization.optimizeWMOs import OptimizeWMOs
from exportResults import GetResults

def main():
    print("Begin CaUWMET!")
    
    # setup log file
    try:  ### WARNING! this clears the log file if one already exists....
        with open("CaUWMET.log","w") as file: pass
    finally:
        logger = logging.getLogger()
        logger.setLevel(logging.INFO)
        handler = logging.FileHandler('CaUWMET.log')
        logger.addHandler(handler)
    # begin logging
    logger.info('CaUWMET Optimization Logs')
    logger.info(f"{datetime.now()}")

    # optimize = True #TODO: link to optimize variable in modelLogic.execute function

    print("Prepare model logic...")
    
    try:
        modelLogic = ModelLogic(InputData(InputDataLocations()),StorageUtilities())
        logger.info("ModelLogic - OK\n")
        print("Model Logic Prepared!")
    except:
        logger.info('ModelLogic Failure!')
        logger.info(f"#### START ERROR LOG ####\n{e}\n####  END ERROR LOG  ####")
        print("ModelLogic failure! See CaUWMET.log for more details....")
    
    logger.info('------------------------')
    logger.info("Begin Contractor Loop")
    logger.info('------------------------')
    for contractor in modelLogic.inputData.contractorsList:
        logger.info(f"##### {contractor} #####")
        # parameterize the optimization - defaults below...
        wmoFloor=None
        wmoCeiling=None
        lowerBounds=[0]*8
        upperBounds='longtermWMOVolumeLimits'
        
        print(f"Instantiate optimizer for {contractor}...")
        try:
            optimizeWMOs = OptimizeWMOs(
                contractor=contractor,
                modelLogic=modelLogic,
                wmoFloor=wmoFloor,
                wmoCeiling=wmoCeiling,
                lowerBounds=lowerBounds,
                upperBounds=upperBounds
            )
            print('Optimizer ready!')
        except:
            logger.info('OptimizeWMOs Failure!')
            logger.info(f"#### START ERROR LOG ####\n{e}\n####  END ERROR LOG  ####")
            print("OptimizeWMOs failure! See CaUWMET.log for more details....")

        print("\nOptimize CaUWMET model...")
        result = optimizeWMOs.optimize(result=True)
        print("Model Optimized!")
        
        print("\nVisualize results...")
        optimizeWMOs.visualization_a(save=True)
        print("Visualization complete!")
        
        print("\nExport results...")
        #GetResults(x=result.X, contractor=contractor).exportResults()
        print("Results exported!")
        print('\nOptimization complete!')
    
    logger.info(f"{datetime.now()}")
    logger.info('Operation Complete!')
if __name__ == "__main__":
    main()
# San Gorgonio Pass Water Agency: [0, 0, 0, 0, 0, 0, 9.99999999e+02, 0]
# City of Tracy: X = [0, 0, 0, 0, 2.34790511e+03, 0, 7.49822714e+03, 0]
