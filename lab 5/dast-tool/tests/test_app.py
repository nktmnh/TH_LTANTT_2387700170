import unittest
from app import create_app


class ApiTests(unittest.TestCase):
    def setUp(self):
        self.client = create_app().test_client()

    def test_health_and_monitor_endpoints(self):
        self.assertEqual("ok", self.client.get("/api/health").get_json()["status"])
        self.assertGreater(self.client.get("/api/monitor").get_json()["pid"], 0)

    def test_security_and_sandbox_endpoints(self):
        response = self.client.post("/api/security", json={"source": "eval(x)"})
        self.assertEqual("dynamic_eval", response.get_json()["findings"][0]["behavior"])
        response = self.client.post("/api/sandbox", json={"command": ["echo", "api"]})
        self.assertEqual("api", response.get_json()["stdout"].strip())
        rejected = self.client.post(
            "/api/sandbox", json={"command": ["python", "-c", "pass"]}
        )
        self.assertEqual(400, rejected.status_code)


if __name__ == "__main__":
    unittest.main()
