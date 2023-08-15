from exportResults import GetResults
from src.optimization.optimizeWMOs import OptimizeWMOs

def main():
    #TODO: link to optimize var in execute function
    #TODO: link x in line 37 with optimized x
    optimize = True

    if optimize:
        # parameterize the optimization - defaults below...
        contractor='City of Tracy'
        wmoFloor=None
        wmoCeiling=None
        lowerBounds=[0]*8
        upperBounds='longtermWMOVolumeLimits'

        print("Instantiate optimizer with chosen parameters...")
        optimizeWMOs = OptimizeWMOs(
            contractor=contractor,
            wmoFloor=wmoFloor,
            wmoCeiling=wmoCeiling,
            lowerBounds=lowerBounds,
            upperBounds=upperBounds
        )
        print('Optimizer instantiated!')
        
        print("\nOptimize CaUWMET model...")
        result = optimizeWMOs.optimize(result=True)
        print('Optimization complete!')
            
        print("\nVisualize results:")
        optimizeWMOs.visualization_a(save=True)

        GetResults(x=result.X, contractor=contractor).exportResults()
    
if __name__ == "__main__":
    main()
# San Gorgonio Pass Water Agency: [0, 0, 0, 0, 0, 0, 9.99999999e+02, 0]
# City of Tracy: X = [0, 0, 0, 0, 2.34790511e+03, 0, 7.49822714e+03, 0]
