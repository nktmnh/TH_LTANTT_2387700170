"""Small, deterministic DevSecOps checks suitable for an educational CI gate."""

from __future__ import annotations

import ast
import json
import re
from dataclasses import asdict, dataclass
from pathlib import Path


@dataclass(frozen=True)
class Finding:
    gate: str
    severity: str
    file: str
    line: int
    message: str


SECRET_PATTERNS = (
    ("hard-coded password", re.compile(r"(?i)password\s*[=:]\s*['\"][^'\"]{8,}['\"]")),
    ("hard-coded API key", re.compile(r"(?i)(api[_-]?key|token)\s*[=:]\s*['\"][A-Za-z0-9_\-]{16,}['\"]")),
    ("private key material", re.compile(r"-----BEGIN (?:RSA |EC )?PRIVATE KEY-----")),
)


def finding(gate: str, severity: str, path: Path, line: int, message: str, root: Path) -> Finding:
    return Finding(gate, severity, path.relative_to(root).as_posix(), line, message)


def scan_python(path: Path, root: Path) -> list[Finding]:
    findings: list[Finding] = []
    try:
        tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
    except SyntaxError as error:
        return [finding("sast", "high", path, error.lineno or 1, "Python syntax error", root)]
    for node in ast.walk(tree):
        if not isinstance(node, ast.Call):
            continue
        func = node.func
        if isinstance(func, ast.Name) and func.id in {"eval", "exec"}:
            findings.append(finding("sast", "high", path, node.lineno, f"Unsafe {func.id}() call", root))
        if isinstance(func, ast.Attribute) and func.attr in {"run", "Popen", "call"}:
            if any(keyword.arg == "shell" and isinstance(keyword.value, ast.Constant) and keyword.value.value is True for keyword in node.keywords):
                findings.append(finding("sast", "high", path, node.lineno, "subprocess with shell=True", root))
    return findings


def scan_secrets(path: Path, root: Path) -> list[Finding]:
    findings: list[Finding] = []
    for number, line in enumerate(path.read_text(encoding="utf-8", errors="ignore").splitlines(), 1):
        for description, pattern in SECRET_PATTERNS:
            if pattern.search(line):
                findings.append(finding("secrets", "critical", path, number, f"Possible {description}", root))
    return findings


def scan_requirements(path: Path, root: Path) -> list[Finding]:
    findings: list[Finding] = []
    denied = {"django": "Example policy: upgrade framework before allowing it"}
    for number, raw in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
        line = raw.strip()
        if not line or line.startswith("#"):
            continue
        name = re.split(r"[<>=!~\[]", line, maxsplit=1)[0].strip().lower()
        if "==" not in line:
            findings.append(finding("dependency", "medium", path, number, "Dependency version must be pinned with ==", root))
        if name in denied:
            findings.append(finding("dependency", "high", path, number, denied[name], root))
    return findings


def scan_compose(path: Path, root: Path) -> list[Finding]:
    findings: list[Finding] = []
    lines = path.read_text(encoding="utf-8").splitlines()
    text = "\n".join(lines)
    for number, line in enumerate(lines, 1):
        compact = line.replace(" ", "")
        if "privileged:true" in compact:
            findings.append(finding("iac", "critical", path, number, "Privileged container is forbidden", root))
        if "/var/run/docker.sock" in line:
            findings.append(finding("iac", "high", path, number, "Docker socket mount is forbidden", root))
        if re.search(r'[-\s]?["\']?0\.0\.0\.0:', line):
            findings.append(finding("iac", "high", path, number, "Public interface binding is forbidden", root))
    if "read_only: true" not in text:
        findings.append(finding("iac", "medium", path, 1, "Container filesystem should be read-only", root))
    if "no-new-privileges:true" not in text:
        findings.append(finding("iac", "medium", path, 1, "Missing no-new-privileges security option", root))
    return findings


def scan_project(root: Path) -> list[Finding]:
    root = root.resolve()
    # Tests intentionally contain insecure snippets as scanner fixtures; they are
    # exercised by unit tests but are not deployable application source.
    ignored = {".git", ".venv", "__pycache__", "reports", "screenshots", "tests"}
    results: list[Finding] = []
    for path in root.rglob("*"):
        if not path.is_file() or any(part in ignored for part in path.parts):
            continue
        if path.suffix == ".py":
            results.extend(scan_python(path, root))
            results.extend(scan_secrets(path, root))
        elif path.name in {"requirements.txt", "requirements-dev.txt"}:
            results.extend(scan_requirements(path, root))
        elif path.name in {"docker-compose.yml", "compose.yml"}:
            results.extend(scan_compose(path, root))
    return results


def write_report(findings: list[Finding], destination: Path) -> None:
    destination.parent.mkdir(parents=True, exist_ok=True)
    payload = {
        "status": "passed" if not findings else "failed",
        "summary": {"total": len(findings), "high_or_critical": sum(item.severity in {"high", "critical"} for item in findings)},
        "findings": [asdict(item) for item in findings],
    }
    destination.write_text(json.dumps(payload, indent=2), encoding="utf-8")
