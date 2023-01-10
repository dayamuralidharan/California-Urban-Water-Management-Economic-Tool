from unittest import TestCase
from src.modelLogic.costOptimizer import CostOptimizer
from unittest.mock import Mock, MagicMock

class CostOptimizationTests(TestCase):
    
    def test_cost_was_optimized(self):
        modelLogic = Mock()
        modelLogic.executeModelLogic = MagicMock()
        costOptimizer = CostOptimizer(modelLogic)
        #costOptimizer.optimize()
        #modelLogic.executeModelLogic.assert_called_once()