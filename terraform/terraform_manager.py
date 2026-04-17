
from __future__ import annotations

from pathlib import Path

from utils.command_runner import run_command
from utils.config import DEFAULT_AMI_ID, TERRAFORM_DIR

TERRAFORM_MAIN_TEMPLATE = """terraform {
  required_version = ">= 1.0.0"
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
  }
}

provider "aws" {
  region = var.aws_region
}

variable "aws_region" {
  type        = string
  description = "AWS region for the EC2 deployment."
}

variable "key_pair_name" {
  type        = string
  description = "Existing AWS key pair name."
}

variable "instance_type" {
  type        = string
  description = "EC2 instance type."
}

variable "ami_id" {
  type        = string
  description = "AMI ID used for the EC2 instance."
}

resource "aws_instance" "llm_ec2" {
  ami           = var.ami_id
  instance_type = var.instance_type
  key_name      = var.key_pair_name

  tags = {
    Name = "llm-controller-instance"
  }
}

output "public_ip" {
  description = "Public IP of the EC2 instance."
  value       = aws_instance.llm_ec2.public_ip
}
"""


def create_main_tf(key_pair_name: str, instance_type: str, aws_region: str) -> tuple[Path, Path]:
    TERRAFORM_DIR.mkdir(parents=True, exist_ok=True)
    main_tf_path = TERRAFORM_DIR / "main.tf"
    tfvars_path = TERRAFORM_DIR / "terraform.auto.tfvars"

    main_tf_path.write_text(TERRAFORM_MAIN_TEMPLATE, encoding="utf-8")
    tfvars_path.write_text(
        "\n".join(
            [
                f'aws_region = "{aws_region}"',
                f'key_pair_name = "{key_pair_name}"',
                f'instance_type = "{instance_type}"',
                f'ami_id = "{DEFAULT_AMI_ID}"',
                "",
            ]
        ),
        encoding="utf-8",
    )
    return main_tf_path, tfvars_path


def run_terraform_apply() -> None:
    run_command(["terraform", "init"], cwd=TERRAFORM_DIR)
    run_command(["terraform", "apply", "-auto-approve"], cwd=TERRAFORM_DIR)
