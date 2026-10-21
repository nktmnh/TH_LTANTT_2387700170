from __future__ import annotations

import ast
from pathlib import Path


class SecurityBehaviorChecker(ast.NodeVisitor):
    """Find suspicious API calls in code without importing or executing it."""

    def __init__(self) -> None:
        self.findings: list[dict] = []

    def visit_Call(self, node: ast.Call) -> None:
        function = node.func
        name = (
            function.id
            if isinstance(function, ast.Name)
            else function.attr if isinstance(function, ast.Attribute) else ""
        )
        module = (
            function.value.id
            if isinstance(function, ast.Attribute)
            and isinstance(function.value, ast.Name)
            else ""
        )
        if name in {"eval", "exec"}:
            self.findings.append(
                {
                    "behavior": f"dynamic_{name}",
                    "line": node.lineno,
                    "severity": "high",
                    "message": f"Dynamic {name} execution detected.",
                }
            )
        elif module == "os" and name == "system":
            self.findings.append(
                {
                    "behavior": "system_command",
                    "line": node.lineno,
                    "severity": "high",
                    "message": "os.system command execution detected.",
                }
            )
        elif name == "Popen" and any(
            k.arg == "shell"
            and isinstance(k.value, ast.Constant)
            and k.value.value is True
            for k in node.keywords
        ):
            self.findings.append(
                {
                    "behavior": "shell_true",
                    "line": node.lineno,
                    "severity": "medium",
                    "message": "subprocess call uses shell=True.",
                }
            )
        self.generic_visit(node)

    def analyze_source(self, source: str) -> list[dict]:
        self.findings = []
        try:
            self.visit(ast.parse(source))
        except SyntaxError as exc:
            self.findings.append(
                {
                    "behavior": "syntax_error",
                    "line": exc.lineno or 1,
                    "severity": "low",
                    "message": f"Could not analyze syntax: {exc.msg}",
                }
            )
        return list(self.findings)

    def analyze_file(self, path: str | Path) -> list[dict]:
        return self.analyze_source(
            Path(path).read_text(encoding="utf-8", errors="replace")
        )
