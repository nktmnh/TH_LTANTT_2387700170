from __future__ import annotations

import argparse
from pathlib import Path

from devsecops.security_gates import scan_project, write_report


def main() -> int:
    parser = argparse.ArgumentParser(description="Run Lab 6 DevSecOps security gates")
    parser.add_argument("--root", type=Path, default=Path("."))
    parser.add_argument("--report", type=Path, default=Path("reports/security-report.json"))
    args = parser.parse_args()
    root = args.root.resolve()
    report = args.report if args.report.is_absolute() else root / args.report
    findings = scan_project(root)
    write_report(findings, report)
    print(f"Security gates: {'PASSED' if not findings else 'FAILED'}")
    print(f"Findings: {len(findings)} | Report: {report.relative_to(root)}")
    for item in findings:
        print(f"[{item.severity.upper()}] {item.gate}: {item.file}:{item.line} - {item.message}")
    return 1 if any(item.severity in {"high", "critical"} for item in findings) else 0


if __name__ == "__main__":
    raise SystemExit(main())
