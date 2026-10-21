from __future__ import annotations

import tracemalloc
import psutil


class MemoryAnalyzer:
    """Report Python allocation snapshots and process RSS; flag oversized integers."""

    def __init__(self, process: psutil.Process | None = None) -> None:
        self.process = process or psutil.Process()
        if not tracemalloc.is_tracing():
            tracemalloc.start()

    def snapshot(self) -> dict:
        current, peak = tracemalloc.get_traced_memory()
        rss = self.process.memory_info().rss
        return {
            "python_current_bytes": current,
            "python_peak_bytes": peak,
            "process_rss_bytes": rss,
        }

    @staticmethod
    def check_overflow(value: int, bits: int = 63) -> bool:
        if bits < 2:
            raise ValueError("bits must be at least 2")
        return not (-(2 ** (bits - 1)) <= int(value) <= (2 ** (bits - 1) - 1))

    @staticmethod
    def compare(before: dict, after: dict, threshold_bytes: int = 1024 * 1024) -> dict:
        """Flag sustained allocation growth between two comparable snapshots.

        This is a heuristic for teaching and diagnostics, not proof of a leak.
        """
        if threshold_bytes < 0:
            raise ValueError("threshold_bytes cannot be negative")
        growth = int(after["python_current_bytes"]) - int(
            before["python_current_bytes"]
        )
        return {
            "python_growth_bytes": growth,
            "threshold_bytes": threshold_bytes,
            "leak_suspected": growth > threshold_bytes,
        }

    def analyze(self) -> dict:
        result = self.snapshot()
        result["overflow_detected"] = False
        return result
