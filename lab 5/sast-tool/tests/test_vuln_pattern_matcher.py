import unittest
from sast_tool.vuln_pattern_matcher import VulnPatternMatcher


class PatternMatcherTests(unittest.TestCase):
    def test_detects_credentials_and_pickle(self):
        source = "password = 'secret-value'\nimport pickle\npickle.loads(data)\n"
        findings = VulnPatternMatcher().analyze(source, "demo.py")
        self.assertEqual({"SAST003", "SAST004"}, {f["ruleId"] for f in findings})
        self.assertTrue(all(f["source"] == "demo.py" for f in findings))


if __name__ == "__main__":
    unittest.main()
