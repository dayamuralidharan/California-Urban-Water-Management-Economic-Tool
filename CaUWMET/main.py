# Main - Loop and Report CaUWMET Model Optimization for all Contractors

import argparse
from datetime import datetime
from datetime import timedelta
import logging

from src.modelLogic.modelLogic import ModelLogic
from src.modelLogic.inputData import InputData
from src.modelLogic.storageUtilities import StorageUtilities
from src.modelLogic.inputDataLocations import InputDataLocations

from src.optimization.optimizeWMOs import OptimizeWMOs
from src.optimization.getResults import GetResults

# Main CaUWMET loop script
def main():
    print("Begin CaUWMET!")
    
    # get arguments
    parser = argparse.ArgumentParser(
        prog='CaUWMET Model Optimization',
        description='This program loops through contractors\nto report CaUWMET model optimization results.'
    )
    parser.add_argument("-v", "--verbose", action="store_true",
                        help="Enable verbose mode")
    parser.add_argument("-c", "--contractors", nargs='+', type=str,
                        help="Specify one or more contractors to run the model on")
    args = parser.parse_args()

    # setup log file
    try:  # WARNING! this clears the log file if one already exists....
        with open("CaUWMET.log","w") as file: pass
    finally:
        logger = logging.getLogger()
        logger.setLevel(logging.INFO)
        handler = logging.FileHandler('CaUWMET.log')
        logger.addHandler(handler)
    
    # begin logging
    logger.info('CaUWMET Optimization Logs')
    logger.info(f"Start Datetime: {datetime.now()}")

    print("Prepare model logic...")
    try:
        modelLogic = ModelLogic(InputData(InputDataLocations()),StorageUtilities())
        contractors = args.contractors if args.contractors is not None else modelLogic.inputData.contractorsList
        logger.info("ModelLogic - OK")
        print("Model logic prepared")
    except Exception as e:
        logger.info('ModelLogic Failure!')
        logger.info(f"#### START ERROR LOG ####\n{e}\n####  END ERROR LOG  ####")
        print("ModelLogic failure! See CaUWMET.log for details....")
    
    logger.info(f"Begin optimization loop through {len(contractors)} Contractors")
    logger.info('---')
    logger.info('{')  # results logged as json
    
    # Contractor Loop
    modelOutputsOptimAll = GetResults(modelLogic=modelLogic)
    qaqcResultsOptimAll = GetResults(modelLogic=modelLogic)
    modelOutputsZeroAll = GetResults(modelLogic=modelLogic)
    qaqcResultsZeroAll = GetResults(modelLogic=modelLogic)

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
                verbose=args.verbose,
                modelLogic=modelLogic,
                contractor=contractor,
                wmoFloor=wmoFloor,
                wmoCeiling=wmoCeiling,
                lowerBounds=lowerBounds,
                upperBounds=upperBounds
            )
            print('Optimizer ready')
        except Exception as e:
            logger.info(f"    error: '{e}'")
            logger.info("  },") if contractor != contractors[-1] else logger.info("  }")
            print("OptimizeWMOs failure! See CaUWMET.log for details....")
            error = True
            pass
        if error:
            continue
        
        print("Optimize model...")
        try:
            result = optimizeWMOs.optimize(result=True)
            X_optim, F_optim = optimizeWMOs.reportBest(zero_threshold=1,result=True)
            exec_time = timedelta(seconds = round(result.exec_time))
            print("Model optimized")
        except Exception as e:
            logger.info(f"    error: '{e}'")
            logger.info("  },") if contractor != contractors[-1] else logger.info("  }")
            print("Optimization failure! See CaUWMET.log for details....")
            error = True
            pass
        if error:
            continue

        print("Export optimized results...")
        try:
            modelOutputsOptim, qaqcResultsOptim = optimizeWMOs.exportResults()
            modelOutputsOptimAll.appendResults(modelOutputsOptim)
            qaqcResultsOptimAll.appendResults(qaqcResultsOptim)
            print("Optimized results exported")
        except Exception as e:
            logger.info(f"    error: '{e}'")
            logger.info("  },") if contractor != contractors[-1] else logger.info("  }")
            print("Export optimized results failure! See CaUWMET.log for details....")
            error = True
            pass
        if error:
            continue

        print("Compute zeroed result...")
        try:
            X_zero, F_zero = optimizeWMOs.reportZero(result=True)
            print("Zeroed result computed")
        except Exception as e:
            logger.info(f"    error: '{e}'")
            logger.info("  },") if contractor != contractors[-1] else logger.info("  }")
            print("Zeroed result computation failure! See CaUWMET.log for details....")
            error = True
            pass
        if error:
            continue
        
        print("Export zeroed results...")
        try:
            modelOutputsZero, qaqcResultsZero = optimizeWMOs.exportResults()
            modelOutputsZeroAll.appendResults(modelOutputsZero)
            qaqcResultsZeroAll.appendResults(qaqcResultsZero)
            print("Zeroed results exported")
        except Exception as e:
            logger.info(f"    error: '{e}'")
            logger.info("  },") if contractor != contractors[-1] else logger.info("  }")
            print("Export zeroed results failure! See CaUWMET.log for details....")
            error = True
            pass
        if error:
            continue

        print("Visualize results...")
        try:
            viz_a = optimizeWMOs.visualization_a(save=True)
            print("Visualization complete")
        except Exception as e:
            logger.info(f"    error: '{e}'")
            logger.info("  },") if contractor != contractors[-1] else logger.info("  }")
            print("Visualization failure! See CaUWMET.log for details....")
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

    # close json
    logger.info("}")
    logger.info('---')
    logger.info('Optimization loop complete!')

    print('Write outputs to excel files...')
    try:
        filenames = [
            'ModelOutputs_Optimal.xlsx',
            'QAQCResults_Optimal.xlsx',
            'ModelOutputs_Zero.xlsx',
            'QAQCResults_Zero.xlsx'
        ]
        modelOutputsOptimAll.writeResults(filenames[0])
        qaqcResultsOptimAll.writeResults(filenames[1])
        modelOutputsZeroAll.writeResults(filenames[2])
        qaqcResultsZeroAll.writeResults(filenames[3])
        logger.info(f"Excel file outputs: {filenames}")
        print('Outputs written to excel files')
    except Exception as e:
        logger.info('Write outputs to excel Failure!')
        logger.info(f"#### START ERROR LOG ####\n{e}\n####  END ERROR LOG  ####")
        print("Write outputs to excel failure! See CaUWMET.log for details....")
        pass

    # finish logging
    logger.info(f"End Datetime: {datetime.now()}")
    logger.info('Operation Complete!')
    print('Close CaUWMET.log')
    print("\nModel optimization complete for all Contractors!")
    print("CaUWMET Complete!")


if __name__ == "__main__":
    main()

