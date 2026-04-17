
from __future__ import annotations

from pathlib import Path

from terraform.terraform_manager import create_main_tf, run_terraform_apply
from utils.config import (
    DEFAULT_AWS_REGION,
    DEFAULT_EC2_HOST,
    DEFAULT_EC2_USER,
    DEFAULT_INSTANCE_TYPE,
    DEFAULT_KEY_PAIR_NAME,
    DEFAULT_PEM_PATH,
    LLM_SCRIPT_PATH,
)
from utils.csv_logger import save_prompt_to_csv
from utils.session import SessionManager
from utils.ssh_manager import (
    cleanup_ssh_sessions,
    connect_ssh,
    upload_and_execute_script,
    run_remote_command,
)


def _prompt(message: str, default: str) -> str:
    value = input(f"{message} [{default}]: ").strip()
    return value or default


def generate_terraform_flow() -> None:
    key_pair = _prompt("AWS key pair name", DEFAULT_KEY_PAIR_NAME)
    instance_type = _prompt("EC2 instance type", DEFAULT_INSTANCE_TYPE)
    aws_region = _prompt("AWS region", DEFAULT_AWS_REGION)

    main_tf_path, tfvars_path = create_main_tf(
        key_pair_name=key_pair,
        instance_type=instance_type,
        aws_region=aws_region,
    )
    print(f"Terraform config written: {main_tf_path}")
    print(f"Terraform variables written: {tfvars_path}")


def apply_terraform_flow() -> None:
    run_terraform_apply()
    print("Terraform apply completed.")


def connect_ssh_flow(session: SessionManager) -> None:
    pem_path = _prompt("PEM key path", str(DEFAULT_PEM_PATH))
    host = _prompt("EC2 host", DEFAULT_EC2_HOST)
    user = _prompt("EC2 user", DEFAULT_EC2_USER)
    open_new_terminal = _prompt("Open SSH in a new terminal? (y/n)", "y").lower() == "y"

    connected = connect_ssh(
        pem_path=Path(pem_path),
        user=user,
        host=host,
        open_in_new_terminal=open_new_terminal,
        session=session,
    )
    if connected and open_new_terminal:
        print("SSH launched in a new terminal window.")


def run_llm_script_flow() -> None:
    pem_path = Path(_prompt("PEM key path", str(DEFAULT_PEM_PATH)))
    host = _prompt("EC2 host", DEFAULT_EC2_HOST)
    user = _prompt("EC2 user", DEFAULT_EC2_USER)
    upload_and_execute_script(
        pem_path=pem_path,
        user=user,
        host=host,
        local_script_path=LLM_SCRIPT_PATH,
    )
    print("LLM management script uploaded and executed.")


def run_remote_command_flow(command_text: str | None = None) -> None:
    pem_path = Path(_prompt("PEM key path", str(DEFAULT_PEM_PATH)))
    host = _prompt("EC2 host", DEFAULT_EC2_HOST)
    user = _prompt("EC2 user", DEFAULT_EC2_USER)
    command_to_run = command_text or input("Remote command: ").strip()
    if not command_to_run:
        print("No command entered.")
        return
    run_remote_command(
        pem_path=pem_path,
        user=user,
        host=host,
        command_text=command_to_run,
    )


def log_prompt_flow() -> None:
    prompt = input("Enter prompt text: ").strip()
    if not prompt:
        print("Prompt is empty; nothing was logged.")
        return
    csv_path = save_prompt_to_csv(prompt)
    print(f"Prompt saved to {csv_path}")


def exit_flow(session: SessionManager) -> None:
    session.cleanup()
    cleanup_ssh_sessions()
