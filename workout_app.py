#!/usr/bin/env python3
"""
Native Workout Tracker desktop launcher (no browser).

- Starts local server on port 8081
- Opens app in a native macOS webview window
- Stops server when app window closes
"""

from __future__ import annotations

import os
import signal
import socket
import subprocess
import sys
import time
import urllib.request

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
SERVER_PATH = os.path.join(BASE_DIR, "server.py")
SERVER_PORT = 8081
SERVER_URL = f"http://127.0.0.1:{SERVER_PORT}"
LOG_PATH = "/tmp/workout-server.log"


def is_port_open(host: str, port: int) -> bool:
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.settimeout(0.4)
        return sock.connect_ex((host, port)) == 0


def kill_existing_server_on_port(port: int) -> None:
    """Kill existing listener on the workout port so app owns lifecycle."""
    try:
        output = subprocess.check_output(
            ["lsof", "-nP", f"-iTCP:{port}", "-sTCP:LISTEN", "-t"],
            text=True,
        ).strip()
    except subprocess.CalledProcessError:
        return

    if not output:
        return

    for line in output.splitlines():
        line = line.strip()
        if not line:
            continue
        try:
            os.kill(int(line), signal.SIGTERM)
        except OSError:
            pass

    # Wait briefly for the port to clear
    deadline = time.time() + 3
    while time.time() < deadline:
        if not is_port_open("127.0.0.1", port):
            return
        time.sleep(0.1)


def start_server() -> subprocess.Popen:
    log_file = open(LOG_PATH, "ab")
    return subprocess.Popen(
        [sys.executable, SERVER_PATH],
        cwd=BASE_DIR,
        stdout=log_file,
        stderr=subprocess.STDOUT,
    )


def wait_for_server(timeout_seconds: float = 10) -> bool:
    deadline = time.time() + timeout_seconds
    while time.time() < deadline:
        try:
            with urllib.request.urlopen(SERVER_URL, timeout=0.8) as response:
                if response.status == 200:
                    return True
        except Exception:
            pass
        time.sleep(0.2)
    return False


def stop_server(proc: subprocess.Popen | None) -> None:
    if not proc:
        return
    if proc.poll() is not None:
        return
    try:
        proc.terminate()
        proc.wait(timeout=3)
    except Exception:
        try:
            proc.kill()
        except Exception:
            pass


def main() -> int:
    kill_existing_server_on_port(SERVER_PORT)
    proc = start_server()

    if not wait_for_server():
        stop_server(proc)
        return 1

    try:
        import webview

        webview.create_window(
            "Workout Tracker",
            SERVER_URL,
            width=1200,
            height=860,
            min_size=(900, 680),
            resizable=True,
        )
        webview.start()
        return 0
    finally:
        stop_server(proc)


if __name__ == "__main__":
    raise SystemExit(main())
