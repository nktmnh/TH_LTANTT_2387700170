from __future__ import annotations

import argparse
from pathlib import Path

from .ast_analyzer import ASTAnalyzer
from .code_quality_checker import CodeQualityChecker
from .sarif_reporter import SarifReporter
from .security_rule_engine import SecurityRuleEngine
from .vuln_pattern_matcher import VulnPatternMatcher


def scan(paths: list[Path], rules_path: Path) -> list[dict]:
    engine = SecurityRuleEngine(rules_path)
    matcher = VulnPatternMatcher()
    quality = CodeQualityChecker()
    findings: list[dict] = []
    for path in paths:
        source = path.read_text(encoding="utf-8", errors="replace")
        findings.extend(ASTAnalyzer(filename=str(path)).analyze(source))
        findings.extend(matcher.analyze(source, str(path)))
        _, quality_findings = quality.check_file(path)
        findings.extend(quality_findings)
    # Deduplicate identical detections from AST + pattern rules.
    unique = {(f["ruleId"], f["source"], f["line"], f["message"]): f for f in findings}
    return engine.apply(list(unique.values()))


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Static security scan for Python files; writes SARIF 2.1.0."
    )
    parser.add_argument(
        "paths", nargs="+", type=Path, help="Python source files or folders"
    )
    parser.add_argument("--rules", type=Path, default=Path("rules/default_rules.json"))
    parser.add_argument("--output", type=Path, default=Path("report.sarif"))
    args = parser.parse_args()
    files = sorted(
        {
            f
            for p in args.paths
            for f in ([p] if p.is_file() else p.rglob("*.py"))
            if f.is_file() and f.suffix == ".py"
        }
    )
    if not files:
        parser.error("No Python files found in the supplied path(s).")
    findings = scan(files, args.rules)
    SarifReporter().write(findings, args.output)
    print(f"Analysis complete: {len(files)} file(s), {len(findings)} finding(s).")
    print(f"SARIF report saved to {args.output}")
    for item in findings:
        print(
            f"{item.get('source')}:{item.get('line')}: "
            f"{item['severity']} {item['ruleId']} {item['message']}"
        )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
