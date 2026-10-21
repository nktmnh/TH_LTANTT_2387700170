import unittest
from security_behavior_checker import SecurityBehaviorChecker


class BehaviorCheckerTests(unittest.TestCase):
    def test_detects_eval_and_system(self):
        findings = SecurityBehaviorChecker().analyze_source(
            "eval(x)\nimport os\nos.system('x')"
        )
        self.assertEqual(
            {"dynamic_eval", "system_command"}, {f["behavior"] for f in findings}
        )


if __name__ == "__main__":
    unittest.main()
