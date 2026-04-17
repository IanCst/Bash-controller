
from __future__ import annotations

import subprocess


class SessionManager:

    def __init__(self) -> None:
        self._processes: list[subprocess.Popen[str]] = []

    def add_process(self, process: subprocess.Popen[str]) -> None:
        self._processes.append(process)

    def cleanup(self) -> None:
        for process in self._processes:
            if process.poll() is None:
                process.terminate()
        self._processes.clear()
