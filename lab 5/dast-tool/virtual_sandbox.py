from __future__ import annotations

import subprocess
import tempfile
from pathlib import Path


class VirtualSandbox:
    """A constrained demo runner, not an OS security boundary or malware sandbox.

    Only `echo` is allowed. Commands run without a shell, in a fresh temporary
    directory, with a short timeout and no inherited environment variables.
    """

    ALLOWED_COMMANDS = {"echo"}

    def __init__(self, timeout: float = 3.0) -> None:
        self.timeout = timeout

    def run(self, command: list[str]) -> dict:
        if not command or command[0].lower() not in self.ALLOWED_COMMANDS:
            raise ValueError(
                "Only the safe 'echo' command is allowed in this demo sandbox."
            )
        if any("\x00" in part for part in command):
            raise ValueError("NUL bytes are not allowed.")
        with tempfile.TemporaryDirectory(prefix="lab5-sandbox-") as working_dir:
            result = subprocess.run(
                command,
                cwd=working_dir,
                shell=False,
                capture_output=True,
                text=True,
                timeout=self.timeout,
                check=False,
                env={},
            )
        return {
            "returncode": result.returncode,
            "stdout": result.stdout,
            "stderr": result.stderr,
            "working_directory_is_temporary": True,
            "working_directory_removed": not Path(working_dir).exists(),
        }
