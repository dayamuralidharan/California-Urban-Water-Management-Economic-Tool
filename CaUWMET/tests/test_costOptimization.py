import os
import pandas as pd
from unittest import TestCase

from src.modelLogic.inputData import InputData
from src.modelLogic.modelLogic import ModelLogic
from src.modelLogic.storageUtilities import StorageUtilities
from tests.inputDataLocationsForTesting import InputDataLocationsForTesting

from src.optimization.optimizeWMOs import OptimizeWMOs
from src.optimization.getResults import GetResults
        
class costOptimizationTest(TestCase):
    def setUp(self): 
        self.modelLogic = ModelLogic(
            InputData(InputDataLocationsForTesting()),
            StorageUtilities()
        )
        self.optimizeWMOs = OptimizeWMOs(
            verbose=False,
            modelLogic=self.modelLogic,
            contractor='Metropolitan Water District of Southern California',
            wmoFloor=None,
            wmoCeiling=None,
            lowerBounds=[0]*8,
            upperBounds=[0]*8,
            zero_threshold=1,
            n_gen=1,
            pop_size=1
        )
        self.modelOutputsOptimAll = GetResults(modelLogic=self.modelLogic)
        self.qaqcResultsOptimAll = GetResults(modelLogic=self.modelLogic)
        self.modelOutputsZeroAll = GetResults(modelLogic=self.modelLogic)
        self.qaqcResultsZeroAll = GetResults(modelLogic=self.modelLogic)
        self.testFile = 'tests/test_outputs.xlsx'
        self.testGraphic = 'tests/test_graphic.png'


    def tearDown(self):
        if os.path.exists(self.testFile): os.remove(self.testFile)
        if os.path.exists(self.testGraphic): os.remove(self.testGraphic)


    def testCostOptimization(self):
        targetF = 20359407689.471325
        self.optimizeWMOs.optimize(result=False)
        self.Xb, self.Fb = self.optimizeWMOs.reportBest()
        self.modelOutputsOptim, self.qaqcResultsOptim = self.optimizeWMOs.exportResults()
        self.X0, self.F0 = self.optimizeWMOs.reportZero()
        self.modelOutputsZero, self.qaqcResultsZero = self.optimizeWMOs.exportResults()

        # test resultant X & F values
        self.assertTrue(all(x<1 for x in self.optimizeWMOs.res.X))
        self.assertTrue(all(x==0 for x in self.Xb))
        self.assertTrue(all(x==0 for x in self.X0))
        
        self.assertEqual(self.optimizeWMOs.res.F[0], targetF)
        self.assertEqual(self.Fb, targetF)
        self.assertEqual(self.F0, targetF)

        # test algorithm history
        self.assertEqual(len(self.optimizeWMOs.res.history), 1)
        self.assertEqual(len(self.optimizeWMOs.res.pop), 1)

        # test outputs
        self.assertEqual(len(self.modelOutputsOptim), 30)
        self.assertEqual(len(self.qaqcResultsOptim), 11)
        self.assertEqual(len(self.modelOutputsZero), 30)
        self.assertEqual(len(self.qaqcResultsZero), 11)

        self.assertTrue(all(isinstance(x, pd.DataFrame) for x in list(self.modelOutputsOptim.values())[:2]))
        self.assertTrue(all(isinstance(x, pd.Series) for x in list(self.modelOutputsOptim.values())[2:]))
        self.assertTrue(all(isinstance(x, pd.Series) for x in list(self.qaqcResultsOptim.values())))

        self.assertTrue(all(isinstance(x, pd.DataFrame) for x in list(self.modelOutputsZero.values())[:2]))
        self.assertTrue(all(isinstance(x, pd.Series) for x in list(self.modelOutputsZero.values())[2:]))
        self.assertTrue(all(isinstance(x, pd.Series) for x in list(self.qaqcResultsZero.values())))

        # test aggregate outputs
        self.modelOutputsOptimAll.appendResults(self.modelOutputsOptim)
        self.qaqcResultsOptimAll.appendResults(self.qaqcResultsOptim)
        self.modelOutputsZeroAll.appendResults(self.modelOutputsZero)
        self.qaqcResultsZeroAll.appendResults(self.qaqcResultsZero)

        self.assertEqual(len(self.modelOutputsOptimAll.aggregatedOutputs), 30)
        self.assertEqual(len(self.qaqcResultsOptimAll.aggregatedOutputs), 11)
        self.assertEqual(len(self.modelOutputsZeroAll.aggregatedOutputs), 30)
        self.assertEqual(len(self.qaqcResultsZeroAll.aggregatedOutputs), 11)

        self.assertTrue(all(isinstance(x, pd.DataFrame) for x in list(self.modelOutputsOptimAll.aggregatedOutputs.values())))
        self.assertTrue(all(isinstance(x, pd.DataFrame) for x in list(self.qaqcResultsOptimAll.aggregatedOutputs.values())))
        self.assertTrue(all(isinstance(x, pd.DataFrame) for x in list(self.modelOutputsZeroAll.aggregatedOutputs.values())))
        self.assertTrue(all(isinstance(x, pd.DataFrame) for x in list(self.qaqcResultsZeroAll.aggregatedOutputs.values())))

        # TODO: improve graphics test
        # test graphics
        self.optimizeWMOs.visualization_a(test=True)
        self.assertTrue(os.path.exists(self.testGraphic))

        # TODO: improve test by parsing through all excel outputs
        # Test excel writer
        self.modelOutputsOptimAll.writeResults(filename=self.testFile)
        self.assertTrue(os.path.exists(self.testFile))

        # with pd.ExcelFile(self.test_filename) as xls:
            # Check the sheet names
            # sheet_names = xls.sheet_names
            # self.assertIn('HydroYearType', sheet_names)
            # self.assertIn('Your_Sheet_Name', sheet_names)  # Replace with the actual sheet name

            # # Check the dimensions of the sheets
            # hydro_year_sheet = xls.parse('HydroYearType')
            # your_sheet = xls.parse('Your_Sheet_Name')  # Replace with the actual sheet name

            # # Check the number of rows and columns
            # self.assertEqual(len(hydro_year_sheet), expected_rows_hydro_year)
            # self.assertEqual(len(hydro_year_sheet.columns), expected_columns_hydro_year)

            # self.assertEqual(len(your_sheet), expected_rows_your_sheet)
            # self.assertEqual(len(your_sheet.columns), expected_columns_your_sheet)

