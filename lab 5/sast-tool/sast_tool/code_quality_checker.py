from __future__ import annotations

import ast
import subprocess
import sys
from pathlib import Path


class CodeQualityChecker:
    """Measure basic risk-oriented code metrics and optional flake8 findings."""

    def __init__(self, max_function_lines: int = 50, max_complexity: int = 10) -> None:
        self.max_function_lines = max_function_lines
        self.max_complexity = max_complexity

    @staticmethod
    def _complexity(node: ast.AST) -> int:
        branches = (
            ast.If,
            ast.For,
            ast.AsyncFor,
            ast.While,
            ast.ExceptHandler,
            ast.IfExp,
            ast.comprehension,
            ast.Match,
        )
        return 1 + sum(isinstance(n, branches) for n in ast.walk(node))

    def metrics(self, source: str) -> dict:
        tree = ast.parse(source)
        functions = [
            n
            for n in ast.walk(tree)
            if isinstance(n, (ast.FunctionDef, ast.AsyncFunctionDef))
        ]
        imports = sum(
            isinstance(n, (ast.Import, ast.ImportFrom)) for n in ast.walk(tree)
        )
        return {
            "function_count": len(functions),
            "long_functions": [
                n.name
                for n in functions
                if (getattr(n, "end_lineno", n.lineno) - n.lineno + 1)
                > self.max_function_lines
            ],
            "high_complexity": {
                n.name: self._complexity(n)
                for n in functions
                if self._complexity(n) > self.max_complexity
            },
            "dependency_count": imports,
        }

    def check_file(self, path: str | Path) -> tuple[dict, list[dict]]:
        file_path = Path(path)
        source = file_path.read_text(encoding="utf-8", errors="replace")
        metrics = self.metrics(source)
        findings: list[dict] = []
        for name in metrics["long_functions"]:
            findings.append(
                {
                    "ruleId": "SAST007",
                    "message": (
                        f"Function '{name}' exceeds "
                        f"{self.max_function_lines} lines."
                    ),
                    "line": 1,
                    "severity": "note",
                    "source": str(file_path),
                }
            )
        for name, complexity in metrics["high_complexity"].items():
            findings.append(
                {
                    "ruleId": "SAST008",
                    "message": f"Function '{name}' has complexity {complexity}.",
                    "line": 1,
                    "severity": "warning",
                    "source": str(file_path),
                }
            )
        try:
            proc = subprocess.run(
                [
                    sys.executable,
                    "-m",
                    "flake8",
                    "--format=%(path)s:%(row)d:%(code)s:%(text)s",
                    str(file_path),
                ],
                capture_output=True,
                text=True,
                timeout=15,
                check=False,
            )
            for output in proc.stdout.splitlines():
                parts = output.split(":", 3)
                if len(parts) == 4:
                    try:
                        line = int(parts[1])
                    except ValueError:
                        line = 1
                    findings.append(
                        {
                            "ruleId": "SAST009",
                            "message": f"flake8 {parts[2]}: {parts[3].strip()}",
                            "line": line,
                            "severity": "note",
                            "source": str(file_path),
                        }
                    )
        except (subprocess.TimeoutExpired, FileNotFoundError):
            pass
        return metrics, findings
