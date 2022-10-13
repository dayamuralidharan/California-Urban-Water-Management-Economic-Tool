import os
import pandas as pd

# Input directories and filenames
dirname = os.path.dirname(__file__)

# Input Assumptions
contingentConservationInputData = "../inputData/contingentWMOsInput_Conservation.csv"

inputContingentConservationFile = os.path.join(dirname, contingentConservationInputData)

contingentConservationData = pd.read_csv(inputContingentConservationFile)

contingentConservationUseReduction = contingentConservationData[contingentConservationData['Variable'] == 'Use Reduction with Contingency Conservation Campaign (% of Total Applied Use)'
contingentConservationStorageTrigger = contingentConservationData[contingentConservationData['Variable'] == 'Storage Volume Trigger for Contingency Conservation (AF)'
