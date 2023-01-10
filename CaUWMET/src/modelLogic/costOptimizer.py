# Find water management portfolio option that has the least cost

# Loop through incremental volumes of supply/demand options input by user for each contractor - j
# Calculate average annual cost for each contractor - k
# Total average annual cost for all contractors - j
# Fit a curve to total annual average cost from each incremental volume loop
# Calculate global minimum on curve
# Return supply volume increments that correspond to that global min


class CostOptimizer:
    
    def __init__(self, modelLogic):
        self.modelLogic = modelLogic
        
    def optimize(self):
        self.modelLogic.executeModelLogic()
        return False