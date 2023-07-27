from exportResults import GetResults
from src.optimization.optimizeWMOs import OptimizeWMOs

def main():
    main = GetResults(x = [1, 1, 1, 1, 1, 1, 1, 1], 
                 contractor='City of Tracy')
    main.exportResults()

    # parameterize the optimization - defaults below...
    # year='2045'
    # contractor='City of Tracy'
    # wmoFloor=None
    # wmoCeiling=None
    # lowerBounds=[0]*8
    # upperBounds='longtermWMOVolumeLimits'

    # print("Instantiate optimizer with chosen parameters...")
    # optimizeWMOs = OptimizeWMOs(
    #     year=year,
    #     contractor=contractor,
    #     wmoFloor=wmoFloor,
    #     wmoCeiling=wmoCeiling,
    #     lowerBounds=lowerBounds,
    #     upperBounds=upperBounds
    # )
    # print('Optimizer instantiated!')
    
    # print("\nOptimize CaUWMET model...")
    # optimizeWMOs.optimize()
    # print('Optimization complete!')
          
    # print("\nVisualize results:")
    # optimizeWMOs.visualization_a(save=True)
    
    
if __name__ == "__main__":
    main()
    