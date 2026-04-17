
from __future__ import annotations

import subprocess
from pathlib import Path
from typing import Sequence


def run_command(command: Sequence[str], cwd: Path | None = None) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        list(command),
        cwd=str(cwd) if cwd else None,
        check=True,
        text=True,
    )


def spawn_command(command: Sequence[str], cwd: Path | None = None) -> subprocess.Popen[str]:
    return subprocess.Popen(
        list(command),
        cwd=str(cwd) if cwd else None,
        text=True,
    )
