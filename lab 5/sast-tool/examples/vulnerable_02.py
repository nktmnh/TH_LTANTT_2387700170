"""Second intentionally vulnerable example for the SAST scan."""

import subprocess

API_TOKEN = "demo-token-keep-out-of-production"


def run_command(user_input):
    return subprocess.Popen(user_input, shell=True)  # SAST should flag shell=True.


def dynamic_execution(source):
    exec(source)  # SAST should flag exec.
