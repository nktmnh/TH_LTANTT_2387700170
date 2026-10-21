import json
import tempfile
import unittest
from pathlib import Path
from sast_tool.sarif_reporter import SarifReporter


class SarifReporterTests(unittest.TestCase):
    def test_writes_sarif_21_with_location(self):
        finding = {
            "ruleId": "SAST001",
            "message": "Avoid eval",
            "line": 4,
            "source": "sample.py",
            "severity": "high",
        }
        with tempfile.TemporaryDirectory() as tmp:
            target = SarifReporter().write([finding], Path(tmp) / "report.sarif")
            data = json.loads(target.read_text(encoding="utf-8"))
        self.assertEqual("2.1.0", data["version"])
        result = data["runs"][0]["results"][0]
        self.assertEqual("error", result["level"])
        self.assertEqual(
            4, result["locations"][0]["physicalLocation"]["region"]["startLine"]
        )


if __name__ == "__main__":
    unittest.main()
