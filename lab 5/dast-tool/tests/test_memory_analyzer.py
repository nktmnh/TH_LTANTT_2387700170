import unittest
from memory_analyzer import MemoryAnalyzer


class MemoryAnalyzerTests(unittest.TestCase):
    def test_snapshot_has_memory_counters(self):
        result = MemoryAnalyzer().analyze()
        self.assertGreater(result["process_rss_bytes"], 0)
        self.assertIn("python_peak_bytes", result)

    def test_detects_integer_overflow(self):
        self.assertFalse(MemoryAnalyzer.check_overflow(10))
        self.assertTrue(MemoryAnalyzer.check_overflow(2**63))

    def test_compare_snapshots_flags_sustained_growth(self):
        before = {"python_current_bytes": 100}
        after = {"python_current_bytes": 1200}
        result = MemoryAnalyzer.compare(before, after, threshold_bytes=500)
        self.assertEqual(1100, result["python_growth_bytes"])
        self.assertTrue(result["leak_suspected"])


if __name__ == "__main__":
    unittest.main()
