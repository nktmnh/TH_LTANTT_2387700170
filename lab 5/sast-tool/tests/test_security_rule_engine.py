import json
import tempfile
import unittest
from pathlib import Path
from sast_tool.security_rule_engine import SecurityRuleEngine


class RuleEngineTests(unittest.TestCase):
    def test_custom_severity_and_disabled_rule(self):
        with tempfile.TemporaryDirectory() as tmp:
            rules = Path(tmp) / "rules.json"
            rules.write_text(
                json.dumps(
                    {
                        "rules": [
                            {
                                "id": "SAST001",
                                "severity": "low",
                                "description": "custom",
                                "enabled": True,
                            },
                            {"id": "SAST002", "enabled": False},
                        ]
                    }
                ),
                encoding="utf-8",
            )
            findings = [
                {"ruleId": "SAST001", "message": "old"},
                {"ruleId": "SAST002", "message": "hidden"},
            ]
            output = SecurityRuleEngine(rules).apply(findings)
        self.assertEqual(1, len(output))
        self.assertEqual("low", output[0]["severity"])
        self.assertEqual("custom", output[0]["message"])


if __name__ == "__main__":
    unittest.main()
