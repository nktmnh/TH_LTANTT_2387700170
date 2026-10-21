import unittest
from virtual_sandbox import VirtualSandbox


class VirtualSandboxTests(unittest.TestCase):
    def test_echo_runs_and_temp_dir_is_removed(self):
        result = VirtualSandbox().run(["echo", "test"])
        self.assertEqual("test", result["stdout"].strip())
        self.assertTrue(result["working_directory_removed"])

    def test_rejects_non_allowlisted_command(self):
        with self.assertRaises(ValueError):
            VirtualSandbox().run(["python", "-c", "print('unsafe')"])


if __name__ == "__main__":
    unittest.main()
