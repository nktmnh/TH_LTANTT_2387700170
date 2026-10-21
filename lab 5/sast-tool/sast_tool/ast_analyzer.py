from __future__ import annotations

import ast
from pathlib import Path


class ASTAnalyzer(ast.NodeVisitor):
    """Find risky Python constructs without executing the analyzed source."""

    DANGEROUS_CALLS = {
        "eval": ("SAST001", "Use of eval() is dangerous and should be avoided."),
        "exec": ("SAST002", "Use of exec() can execute untrusted code."),
    }

    def __init__(self, filename: str = "<string>") -> None:
        self.filename = filename
        self.findings: list[dict] = []

    def visit_Call(self, node: ast.Call) -> None:
        name = node.func.id if isinstance(node.func, ast.Name) else None
        if name in self.DANGEROUS_CALLS:
            rule_id, message = self.DANGEROUS_CALLS[name]
            self.findings.append(
                {
                    "ruleId": rule_id,
                    "message": message,
                    "line": node.lineno,
                    "severity": "warning",
                    "source": self.filename,
                }
            )
        if isinstance(node.func, ast.Attribute) and node.func.attr in {"loads", "load"}:
            if isinstance(node.func.value, ast.Name) and node.func.value.id == "pickle":
                self.findings.append(
                    {
                        "ruleId": "SAST004",
                        "message": "Pickle deserialization can execute code.",
                        "line": node.lineno,
                        "severity": "warning",
                        "source": self.filename,
                    }
                )
        if isinstance(node.func, ast.Attribute) and node.func.attr == "Popen":
            if any(
                k.arg == "shell"
                and isinstance(k.value, ast.Constant)
                and k.value.value is True
                for k in node.keywords
            ):
                self.findings.append(
                    {
                        "ruleId": "SAST006",
                        "message": "subprocess.Popen with shell=True is risky.",
                        "line": node.lineno,
                        "severity": "warning",
                        "source": self.filename,
                    }
                )
        self.generic_visit(node)

    def analyze(self, source: str) -> list[dict]:
        self.findings = []
        try:
            tree = ast.parse(source, filename=self.filename)
        except SyntaxError as exc:
            return [
                {
                    "ruleId": "SAST000",
                    "message": f"Syntax error: {exc.msg}",
                    "line": exc.lineno or 1,
                    "severity": "error",
                    "source": self.filename,
                }
            ]
        self.visit(tree)
        return self.findings

    def analyze_file(self, path: str | Path) -> list[dict]:
        file_path = Path(path)
        self.filename = str(file_path)
        return self.analyze(file_path.read_text(encoding="utf-8", errors="replace"))
