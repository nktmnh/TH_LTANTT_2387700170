from __future__ import annotations

import json
from pathlib import Path


class SecurityRuleEngine:
    """Load configurable severities and descriptions for built-in rule IDs."""

    def __init__(self, rules_path: str | Path | None = None) -> None:
        self.rules: dict[str, dict] = {}
        if rules_path:
            data = json.loads(Path(rules_path).read_text(encoding="utf-8"))
            self.rules = {item["id"]: item for item in data.get("rules", [])}

    def apply(self, findings: list[dict]) -> list[dict]:
        results = []
        for finding in findings:
            result = dict(finding)
            rule = self.rules.get(result["ruleId"], {})
            if rule.get("enabled", True):
                result["severity"] = rule.get(
                    "severity", result.get("severity", "warning")
                )
                result["message"] = rule.get("description", result["message"])
                results.append(result)
        return results
