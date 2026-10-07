import subprocess, logging
from datetime import datetime

logging.basicConfig(filename='netrecon.log', level=logging.INFO)

def log(msg):
    now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    logging.info(f"[{now}] {msg}")

import shutil

def detect_service(ip, ports):
    ports_str = ','.join(str(p) for p in ports)
    nmap_path = shutil.which("nmap") or r"C:\Users\vonha\Downloads\nmap-portable\nmap-7.92\nmap.exe"
    cmd = [nmap_path, "-sV", "-p", ports_str, ip]
    log(f"Running service detection on {ip}:{ports_str}")
    try:
        result = subprocess.check_output(cmd).decode()
        log(result)
        return result
    except subprocess.CalledProcessError as e:
        return f"Error: {e.output.decode()}"
