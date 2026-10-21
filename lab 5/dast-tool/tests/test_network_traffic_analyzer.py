import unittest
from network_traffic_analyzer import NetworkTrafficAnalyzer


class NetworkAnalyzerTests(unittest.TestCase):
    def test_snapshot_has_expected_counter_shape(self):
        counters = NetworkTrafficAnalyzer().snapshot()
        self.assertIsInstance(counters, dict)
        if counters:
            self.assertTrue(
                {"bytes_sent", "bytes_recv", "packets_sent", "packets_recv"}.issubset(
                    next(iter(counters.values()))
                )
            )


if __name__ == "__main__":
    unittest.main()
