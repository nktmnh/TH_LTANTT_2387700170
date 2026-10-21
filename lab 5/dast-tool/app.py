from __future__ import annotations

from flask import Flask, jsonify, request
from memory_analyzer import MemoryAnalyzer
from network_traffic_analyzer import NetworkTrafficAnalyzer
from runtime_monitor import RuntimeMonitor
from security_behavior_checker import SecurityBehaviorChecker
from virtual_sandbox import VirtualSandbox


def create_app() -> Flask:
    app = Flask(__name__)
    runtime, memory, network = (
        RuntimeMonitor(),
        MemoryAnalyzer(),
        NetworkTrafficAnalyzer(),
    )
    behavior, sandbox = SecurityBehaviorChecker(), VirtualSandbox()

    @app.get("/api/health")
    def health():
        return jsonify({"status": "ok", "service": "lab5-dast", "version": "1.0.0"})

    @app.get("/api/monitor")
    def monitor():
        return jsonify(runtime.snapshot())

    @app.get("/api/memory")
    def memory_status():
        return jsonify(memory.analyze())

    @app.get("/api/network")
    def network_status():
        return jsonify({"interfaces": network.snapshot()})

    @app.post("/api/security")
    def security_scan():
        body = request.get_json(silent=True) or {}
        source = body.get("source", "")
        if not isinstance(source, str) or len(source) > 100_000:
            return (
                jsonify(
                    {"error": "source must be a string of at most 100000 characters"}
                ),
                400,
            )
        return jsonify({"findings": behavior.analyze_source(source)})

    @app.post("/api/sandbox")
    def sandbox_run():
        body = request.get_json(silent=True) or {}
        command = body.get("command", [])
        if not isinstance(command, list) or not all(
            isinstance(part, str) for part in command
        ):
            return jsonify({"error": "command must be a list of strings"}), 400
        try:
            return jsonify(sandbox.run(command))
        except ValueError as exc:
            return jsonify({"error": str(exc)}), 400
        except TimeoutError:
            return jsonify({"error": "sandbox command timed out"}), 408

    return app


if __name__ == "__main__":
    create_app().run(host="127.0.0.1", port=5000, debug=False)
