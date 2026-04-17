
from __future__ import annotations

import platform
import subprocess
from pathlib import Path

from utils.command_runner import run_command
from utils.session import SessionManager
from utils.terminal import launch_in_new_terminal


def _build_ssh_command(pem_path: Path, user: str, host: str, remote_command: str | None = None) -> list[str]:
    command = ["ssh", "-i", str(pem_path), f"{user}@{host}"]
    if remote_command:
        command.append(remote_command)
    return command


def connect_ssh(
    pem_path: Path,
    user: str,
    host: str,
    open_in_new_terminal: bool,
    session: SessionManager,
) -> bool:
    command = _build_ssh_command(pem_path=pem_path, user=user, host=host)
    if open_in_new_terminal and launch_in_new_terminal(command):
        return True

    process = subprocess.Popen(command, text=True)
    session.add_process(process)
    process.wait()
    return process.returncode == 0


def upload_and_execute_script(pem_path: Path, user: str, host: str, local_script_path: Path) -> None:
    remote_script_path = "/home/ubuntu/llm_manager.sh"

    run_command(
        [
            "scp",
            "-i",
            str(pem_path),
            str(local_script_path),
            f"{user}@{host}:{remote_script_path}",
        ]
    )
    run_command(
        _build_ssh_command(
            pem_path=pem_path,
            user=user,
            host=host,
            remote_command=f"chmod +x {remote_script_path} && bash {remote_script_path}",
        )
    )


def run_remote_command(pem_path: Path, user: str, host: str, command_text: str) -> None:
    run_command(
        _build_ssh_command(
            pem_path=pem_path,
            user=user,
            host=host,
            remote_command=command_text,
        )
    )


def cleanup_ssh_sessions() -> None:
    if platform.system().lower() != "linux":
        return

    subprocess.run(
        ["pkill", "-f", "ec2-34-207-132-136.compute-1.amazonaws.com"],
        check=False,
        text=True,
    )
