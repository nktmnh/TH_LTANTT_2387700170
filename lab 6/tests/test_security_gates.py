import tempfile
import unittest
from pathlib import Path

from devsecops.security_gates import scan_compose, scan_python, scan_requirements, scan_secrets, write_report


class SecurityGateTests(unittest.TestCase):
    def make_file(self, name: str, content: str) -> tuple[tempfile.TemporaryDirectory, Path]:
        temporary = tempfile.TemporaryDirectory()
        path = Path(temporary.name) / name
        path.write_text(content, encoding="utf-8")
        return temporary, path

    def test_sast_allows_safe_code(self):
        temp, path = self.make_file("safe.py", "print('safe')\n")
        self.addCleanup(temp.cleanup)
        self.assertEqual([], scan_python(path, path.parent))

    def test_sast_detects_eval(self):
        temp, path = self.make_file("bad.py", "eval(user_input)\n")
        self.addCleanup(temp.cleanup)
        self.assertEqual("high", scan_python(path, path.parent)[0].severity)

    def test_sast_detects_exec(self):
        temp, path = self.make_file("bad.py", "exec(user_input)\n")
        self.addCleanup(temp.cleanup)
        self.assertIn("exec", scan_python(path, path.parent)[0].message)

    def test_sast_detects_shell_true(self):
        temp, path = self.make_file("bad.py", "import subprocess\nsubprocess.run('id', shell=True)\n")
        self.addCleanup(temp.cleanup)
        self.assertEqual(1, len(scan_python(path, path.parent)))

    def test_secret_scan_allows_environment_lookup(self):
        temp, path = self.make_file("safe.py", "token = os.environ['TOKEN']\n")
        self.addCleanup(temp.cleanup)
        self.assertEqual([], scan_secrets(path, path.parent))

    def test_secret_scan_detects_password(self):
        temp, path = self.make_file("bad.py", "password = 'example_secret_123'\n")
        self.addCleanup(temp.cleanup)
        self.assertEqual("critical", scan_secrets(path, path.parent)[0].severity)

    def test_dependency_requires_pin(self):
        temp, path = self.make_file("requirements.txt", "flask\n")
        self.addCleanup(temp.cleanup)
        self.assertEqual("medium", scan_requirements(path, path.parent)[0].severity)

    def test_dependency_allows_pin(self):
        temp, path = self.make_file("requirements.txt", "flask==3.1.0\n")
        self.addCleanup(temp.cleanup)
        self.assertEqual([], scan_requirements(path, path.parent))

    def test_iac_detects_privileged(self):
        temp, path = self.make_file("docker-compose.yml", "services:\n  app:\n    privileged: true\n")
        self.addCleanup(temp.cleanup)
        self.assertTrue(any(item.severity == "critical" for item in scan_compose(path, path.parent)))

    def test_iac_detects_public_port(self):
        temp, path = self.make_file("docker-compose.yml", "services:\n  app:\n    ports:\n      - '0.0.0.0:8080:80'\n")
        self.addCleanup(temp.cleanup)
        self.assertTrue(any("Public" in item.message for item in scan_compose(path, path.parent)))

    def test_iac_hardened_configuration(self):
        temp, path = self.make_file("docker-compose.yml", "services:\n  app:\n    read_only: true\n    security_opt:\n      - no-new-privileges:true\n")
        self.addCleanup(temp.cleanup)
        self.assertEqual([], scan_compose(path, path.parent))

    def test_report_is_json(self):
        temp = tempfile.TemporaryDirectory()
        self.addCleanup(temp.cleanup)
        output = Path(temp.name) / "report.json"
        write_report([], output)
        self.assertIn('"status": "passed"', output.read_text(encoding="utf-8"))
