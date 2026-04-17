
from __future__ import annotations

from cli.commands import (
    apply_terraform_flow,
    connect_ssh_flow,
    exit_flow,
    generate_terraform_flow,
    log_prompt_flow,
    run_llm_script_flow,
    run_remote_command_flow,
)
from utils.session import SessionManager


def interactive_menu(session: SessionManager) -> None:
    while True:
        print("\n=== EC2 LLM Controller ===")
        print("1) Generate Terraform config")
        print("2) Terraform init + apply")
        print("3) Connect SSH")
        print("4) Upload & run LLM management script")
        print("5) Run custom remote command")
        print("6) Log prompt to CSV")
        print("7) Exit")

        choice = input("Choose an option: ").strip()
        if choice == "1":
            generate_terraform_flow()
        elif choice == "2":
            apply_terraform_flow()
        elif choice == "3":
            connect_ssh_flow(session)
        elif choice == "4":
            run_llm_script_flow()
        elif choice == "5":
            run_remote_command_flow()
        elif choice == "6":
            log_prompt_flow()
        elif choice == "7":
            exit_flow(session)
            print("Exited cleanly.")
            return
        else:
            print("Invalid option, try again.")
