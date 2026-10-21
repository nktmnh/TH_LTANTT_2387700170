from __future__ import annotations

import json
from pathlib import Path


class SarifReporter:
    """Write findings as SARIF 2.1.0 for compatible editors and CI services."""

    LEVELS = {
        "error": "error",
        "high": "error",
        "warning": "warning",
        "medium": "warning",
        "note": "note",
        "low": "note",
    }

    def build(self, findings: list[dict]) -> dict:
        rule_ids = sorted({f["ruleId"] for f in findings})
        rules = [{"id": rid, "shortDescription": {"text": rid}} for rid in rule_ids]
        results = []
        for item in findings:
            result = {
                "ruleId": item["ruleId"],
                "level": self.LEVELS.get(item.get("severity", "warning"), "warning"),
                "message": {"text": item["message"]},
            }
            source = item.get("source")
            if source:
                result["locations"] = [
                    {
                        "physicalLocation": {
                            "artifactLocation": {"uri": Path(source).as_posix()},
                            "region": {"startLine": max(1, int(item.get("line", 1)))},
                        }
                    }
                ]
            results.append(result)
        return {
            "$schema": "https://json.schemastore.org/sarif-2.1.0.json",
            "version": "2.1.0",
            "runs": [
                {
                    "tool": {
                        "driver": {
                            "name": "Lab5 SAST Tool",
                            "version": "1.0.0",
                            "rules": rules,
                        }
                    },
                    "results": results,
                }
            ],
        }

    def write(self, findings: list[dict], output_path: str | Path) -> Path:
        target = Path(output_path)
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(
            json.dumps(self.build(findings), indent=2, ensure_ascii=False) + "\n",
            encoding="utf-8",
        )
        return target
