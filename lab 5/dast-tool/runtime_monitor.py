from __future__ import annotations

import os
import psutil


class RuntimeMonitor:
    """Capture a bounded point-in-time view of one process."""

    def __init__(self, pid: int | None = None) -> None:
        self.pid = pid or os.getpid()
        self.process = psutil.Process(self.pid)

    def snapshot(self) -> dict:
        with self.process.oneshot():
            memory = self.process.memory_info()
            return {
                "pid": self.pid,
                "name": self.process.name(),
                "cpu_percent": self.process.cpu_percent(interval=0.05),
                "rss_bytes": memory.rss,
                "vms_bytes": memory.vms,
                "open_files": len(self.process.open_files()),
                "status": self.process.status(),
            }
