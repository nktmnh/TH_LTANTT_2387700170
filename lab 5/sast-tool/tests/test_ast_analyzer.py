import unittest
from sast_tool.ast_analyzer import ASTAnalyzer


class ASTAnalyzerTests(unittest.TestCase):
    def test_detects_eval_and_exec(self):
        findings = ASTAnalyzer().analyze("eval('1')\nexec('x=2')")
        self.assertEqual({"SAST001", "SAST002"}, {f["ruleId"] for f in findings})

    def test_syntax_error_is_reported(self):
        self.assertEqual("SAST000", ASTAnalyzer().analyze("def broken(:")[0]["ruleId"])


if __name__ == "__main__":
    unittest.main()
