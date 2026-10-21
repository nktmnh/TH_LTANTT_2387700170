from __future__ import annotations

import ast
import re


class VulnPatternMatcher:
    """Match source-level credential and unsafe-deserialization patterns."""

    CREDENTIAL = re.compile(
        r"(?i)\b(password|passwd|secret|api[_-]?key|token)\s*=\s*"
        r"(['\"])(?!['\"])([^'\"]{3,})\2"
    )

    def analyze(self, source: str, filename: str = "<string>") -> list[dict]:
        findings: list[dict] = []
        for line_no, line in enumerate(source.splitlines(), 1):
            match = self.CREDENTIAL.search(line)
            if match:
                findings.append(
                    {
                        "ruleId": "SAST003",
                        "message": f"Possible hardcoded {match.group(1)}.",
                        "line": line_no,
                        "severity": "warning",
                        "source": filename,
                    }
                )
        try:
            tree = ast.parse(source, filename=filename)
        except SyntaxError:
            return findings
        for node in ast.walk(tree):
            if isinstance(node, ast.Call) and isinstance(node.func, ast.Attribute):
                if (
                    isinstance(node.func.value, ast.Name)
                    and node.func.value.id == "pickle"
                    and node.func.attr in {"load", "loads"}
                ):
                    findings.append(
                        {
                            "ruleId": "SAST004",
                            "message": "Pickle deserialization can execute code.",
                            "line": node.lineno,
                            "severity": "warning",
                            "source": filename,
                        }
                    )
        return findings
