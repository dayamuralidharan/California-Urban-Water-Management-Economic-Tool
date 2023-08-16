from datetime import datetime
from datetime import timedelta
import logging

from src.modelLogic.modelLogic import ModelLogic
from src.modelLogic.inputData import InputData
from src.modelLogic.storageUtilities import StorageUtilities
from src.modelLogic.inputDataLocations import InputDataLocations

from src.optimization.optimizeWMOs import OptimizeWMOs
from exportResults import GetResults

# Main CaUWMET loop script
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

    print("Prepare model logic...")
    try:
        modelLogic = ModelLogic(InputData(InputDataLocations()),StorageUtilities())
        contractors = modelLogic.inputData.contractorsList[:5]  #TODO: remove index reference for prod
        logger.info("ModelLogic - OK")
        print("Model logic prepared!")
    except Exception as e:
        logger.info('ModelLogic Failure!')
        logger.info(f"#### START ERROR LOG ####\n{e}\n####  END ERROR LOG  ####")
        print("ModelLogic failure! See CaUWMET.log for more details....")
    
    logger.info(f"Begin optimization loop through {len(contractors)} Contractors")
    logger.info('---')
    logger.info('{')  # results logged as json
    
    # Contractor Loop
    for contractor in contractors:
        error = False
        logger.info("  {")
        logger.info(f"    contractor: '{contractor}',")

        # parameterize the optimization - defaults below...
        wmoFloor=None
        wmoCeiling=None
        lowerBounds=[0]*8
        upperBounds='longtermWMOVolumeLimits'

        print(f"\nInstantiate optimizer for {contractor}...")
        try:
            optimizeWMOs = OptimizeWMOs(
                verbose=False,
                modelLogic=modelLogic,
                contractor=contractor,
                wmoFloor=wmoFloor,
                wmoCeiling=wmoCeiling,
                lowerBounds=lowerBounds,
                upperBounds=upperBounds
            )
            print('Optimizer ready!')
        except Exception as e:
            logger.info(f"    error: '{e}'")
            logger.info("  },") if contractor != contractors[-1] else logger.info("  }")
            print("OptimizeWMOs failure! See CaUWMET.log for more details....")
            error = True
            pass
        if error:
            continue
        
        print("Optimize model...")
        try:
            result = optimizeWMOs.optimize(result=True)
            X_optim = list(result.X)
            F_optim = result.F[0]
            X_zero, F_zero = optimizeWMOs.report_best(zero_threshold=1)
            exec_time = timedelta(seconds = round(result.exec_time))
            print("Model optimized!")
        except Exception as e:
            logger.info(f"    error: '{e}'")
            logger.info("  },") if contractor != contractors[-1] else logger.info("  }")
            print("Optimization failure! See CaUWMET.log for more details....")
            error = True
            pass
        if error:
            continue
        
        print("Visualize results...")
        try:
            viz_a = optimizeWMOs.visualization_a(save=True)
            print("Visualization complete!")
        except Exception as e:
            logger.info(f"    error: '{e}'")
            logger.info("  },") if contractor != contractors[-1] else logger.info("  }")
            print("Visualization failure! See CaUWMET.log for more details....")
            error = True
            pass
        if error:
            continue
        
        print("Export results...")
        try:
            #GetResults(x=result.X, contractor=contractor).exportResults()
            print("Results exported!")
        except Exception as e:
            logger.info(f"    error: '{e}'")
            logger.info("  },") if contractor != contractors[-1] else logger.info("  }")
            print("Export results failure! See CaUWMET.log for more details....")
            error = True
            pass
        if error:
            continue
        
        # log results if there are no errors
        logger.info(f"    error: 'None',")
        logger.info(f"    X_optim: {X_optim},")
        logger.info(f"    X_zero: {X_zero},")
        logger.info(f"    F_optim: {F_optim},")
        logger.info(f"    F_zero: {F_zero},")
        logger.info(f"    execution_time: '{exec_time}',")
        logger.info(f"    viz_path: '{viz_a}'")
        logger.info("  },") if contractor != contractors[-1] else logger.info("  }")
        print(f'Optimization complete for {contractor}!')

    # close json, complete logging
    logger.info("}")
    logger.info('---')
    logger.info(f"{datetime.now()}")
    logger.info('Operation Complete!')
    print("\nModel optimization complete for all Contractors!")
    print("CaUWMET Complete!")


if __name__ == "__main__":
    main()

