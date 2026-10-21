from __future__ import annotations

import json
from memory_analyzer import MemoryAnalyzer
from network_traffic_analyzer import NetworkTrafficAnalyzer
from runtime_monitor import RuntimeMonitor
from security_behavior_checker import SecurityBehaviorChecker
from virtual_sandbox import VirtualSandbox


def main() -> None:
    print("Runtime:", json.dumps(RuntimeMonitor().snapshot(), indent=2))
    print("Memory:", json.dumps(MemoryAnalyzer().analyze(), indent=2))
    print("Network interfaces:", len(NetworkTrafficAnalyzer().snapshot()))
    print(
        "Behavior demo:",
        json.dumps(
            SecurityBehaviorChecker().analyze_source("eval(user_input)"), indent=2
        ),
    )
    print(
        "Sandbox demo:",
        json.dumps(VirtualSandbox().run(["echo", "safe sandbox demo"]), indent=2),
    )


if __name__ == "__main__":
    main()
