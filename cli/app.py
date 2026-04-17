
from __future__ import annotations

import argparse

from cli.commands import (
    apply_terraform_flow,
    connect_ssh_flow,
    exit_flow,
    generate_terraform_flow,
    log_prompt_flow,
    run_llm_script_flow,
    run_remote_command_flow,
)
from cli.menu import interactive_menu
from utils.session import SessionManager


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="ec2-llm-controller",
        description="Manage an AWS EC2-based LLM environment with Terraform and SSH.",
    )
    subparsers = parser.add_subparsers(dest="command")

    subparsers.add_parser("menu", help="Run interactive menu mode.")
    subparsers.add_parser("generate-tf", help="Generate terraform/main.tf and tfvars.")
    subparsers.add_parser("apply-tf", help="Run terraform init and terraform apply -auto-approve.")
    subparsers.add_parser("ssh", help="Open an SSH session to the configured EC2 instance.")
    subparsers.add_parser("run-llm-script", help="Upload and run scripts/llm_manager.sh on EC2.")
    subparsers.add_parser("log-prompt", help="Capture a user prompt and save it to timestamped CSV.")

    remote_parser = subparsers.add_parser("run-remote", help="Execute a custom remote shell command over SSH.")
    remote_parser.add_argument("command_text", help="Command to execute remotely.")

    return parser


def run() -> None:
    parser = build_parser()
    args = parser.parse_args()
    session = SessionManager()

    command = args.command
    if command in (None, "menu"):
        interactive_menu(session)
    elif command == "generate-tf":
        generate_terraform_flow()
    elif command == "apply-tf":
        apply_terraform_flow()
    elif command == "ssh":
        connect_ssh_flow(session)
    elif command == "run-llm-script":
        run_llm_script_flow()
    elif command == "log-prompt":
        log_prompt_flow()
    elif command == "run-remote":
        run_remote_command_flow(args.command_text)
    else:
        parser.print_help()
    exit_flow(session)
