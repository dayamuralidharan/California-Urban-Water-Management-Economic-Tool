from exportResults import GetResults
from src.optimization.optimizeWMOs import OptimizeWMOs

def main():
    #TODO: link to optimize var in execute function
    #TODO: link x in line 37 with optimized x
    optimize = False

    if optimize:
        # parameterize the optimization - defaults below...
        year='2045'
        contractor='City of Tracy'
        wmoFloor=None
        wmoCeiling=None
        lowerBounds=[0]*8
        upperBounds='longtermWMOVolumeLimits'

        print("Instantiate optimizer with chosen parameters...")
        optimizeWMOs = OptimizeWMOs(
            year=year,
            contractor=contractor,
            wmoFloor=wmoFloor,
            wmoCeiling=wmoCeiling,
            lowerBounds=lowerBounds,
            upperBounds=upperBounds
        )
        print('Optimizer instantiated!')
        
        print("\nOptimize CaUWMET model...")
        optimizeWMOs.optimize()
        print('Optimization complete!')
            
        print("\nVisualize results:")
        optimizeWMOs.visualization_a(save=True)

    else:
        main = GetResults(x = [0, 0, 0, 0, 0, 0, 0, 0],
                    contractor='Alameda County Water District')
        main.exportResults()
    
if __name__ == "__main__":
    main()
# San Gorgonio Pass Water Agency: [0, 0, 0, 0, 0, 0, 9.99999999e+02, 0]
# City of Tracy: X = [0, 0, 0, 0, 1.33711230e+03, 0, 7.49913174e+03, 0]
# City of Coalinga: [0, 0, 0, 0, 0, 0, 1.74204268e+02, 0]