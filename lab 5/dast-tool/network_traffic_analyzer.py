from __future__ import annotations

import psutil


class NetworkTrafficAnalyzer:
    """Read host-wide interface byte/packet counters (not packet contents)."""

    def snapshot(self) -> dict:
        counters = psutil.net_io_counters(pernic=True) or {}
        return {
            name: {
                "bytes_sent": value.bytes_sent,
                "bytes_recv": value.bytes_recv,
                "packets_sent": value.packets_sent,
                "packets_recv": value.packets_recv,
            }
            for name, value in sorted(counters.items())
        }
