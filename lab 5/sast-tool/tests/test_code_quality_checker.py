import unittest
from sast_tool.code_quality_checker import CodeQualityChecker


class CodeQualityTests(unittest.TestCase):
    def test_metrics_count_functions_and_imports(self):
        metrics = CodeQualityChecker().metrics(
            "import os\ndef f(x):\n    if x:\n        return 1\n    return 0\n"
        )
        self.assertEqual(1, metrics["function_count"])
        self.assertEqual(1, metrics["dependency_count"])
        self.assertEqual({}, metrics["high_complexity"])


if __name__ == "__main__":
    unittest.main()
