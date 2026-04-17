
from __future__ import annotations

from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
TERRAFORM_DIR = PROJECT_ROOT / "terraform"
SCRIPTS_DIR = PROJECT_ROOT / "scripts"
LOGS_DIR = PROJECT_ROOT / "logs"

DEFAULT_PEM_PATH = PROJECT_ROOT / "LLM access.pem"
DEFAULT_EC2_USER = "ubuntu"
DEFAULT_EC2_HOST = "ec2-34-207-132-136.compute-1.amazonaws.com"
DEFAULT_KEY_PAIR_NAME = "llm-access-key"
DEFAULT_INSTANCE_TYPE = "t3.medium"
DEFAULT_AWS_REGION = "us-east-1"
DEFAULT_AMI_ID = "ami-053b0d53c279acc90"

LLM_SCRIPT_PATH = SCRIPTS_DIR / "llm_manager.sh"
