terraform {
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
