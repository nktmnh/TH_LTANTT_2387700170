import unittest
from pathlib import Path
from runtime_monitor import RuntimeMonitor


class RuntimeMonitorTests(unittest.TestCase):
    def test_current_process_metrics(self):
        result = RuntimeMonitor().snapshot()
        self.assertEqual("python", Path(result["name"]).stem.lower())
        self.assertGreater(result["rss_bytes"], 0)
        self.assertGreater(result["pid"], 0)


if __name__ == "__main__":
    unittest.main()
