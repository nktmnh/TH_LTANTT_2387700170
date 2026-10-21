import unittest
from pathlib import Path
from sast_tool.main import scan


class ScanIntegrationTests(unittest.TestCase):
    def test_findings_retain_source_filename(self):
        findings = scan(
            [Path("examples/vulnerable_01.py")], Path("rules/default_rules.json")
        )
        self.assertTrue(findings)
        self.assertTrue(all(f["source"] != "<string>" for f in findings))


if __name__ == "__main__":
    unittest.main()
