
from __future__ import annotations

import os
import platform
import shlex
import shutil
import subprocess
from typing import Sequence


def launch_in_new_terminal(command: Sequence[str]) -> bool:
    system = platform.system().lower()
    quoted_command = " ".join(shlex.quote(part) for part in command)

    if system == "linux" and os.environ.get("WSL_DISTRO_NAME"):
        subprocess.Popen(
            ["cmd.exe", "/c", "start", "wsl.exe", "bash", "-lc", f"{quoted_command}; exec bash"],
            text=True,
        )
        return True

    if system == "linux":
        terminal_variants = [
            ["gnome-terminal", "--", "bash", "-lc", f"{quoted_command}; exec bash"],
            ["x-terminal-emulator", "-e", f"bash -lc '{quoted_command}; exec bash'"],
            ["konsole", "-e", "bash", "-lc", f"{quoted_command}; exec bash"],
            ["xfce4-terminal", "-e", f"bash -lc '{quoted_command}; exec bash'"],
        ]
        for terminal_command in terminal_variants:
            if shutil.which(terminal_command[0]):
                subprocess.Popen(terminal_command, text=True)
                return True

    return False
