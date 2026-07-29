terraform {
  required_version = ">= 1.5.0"
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
    random = {
      source  = "hashicorp/random"
      version = "~> 3.6"
    }
  }
}

provider "aws" {
  region = var.aws_region
}

data "aws_caller_identity" "current" {}

resource "random_password" "rag_api_key" {
  length  = 32
  special = false
}

locals {
  name_prefix = var.project_name
  account_id  = data.aws_caller_identity.current.account_id
  image_uri   = "${aws_ecr_repository.rag.repository_url}:${var.image_tag}"
}

# --- ECR ---
resource "aws_ecr_repository" "rag" {
  name                 = "${local.name_prefix}-rag"
  image_tag_mutability = "MUTABLE"
  force_delete         = var.ecr_force_delete

  image_scanning_configuration {
    scan_on_push = true
  }
}

resource "aws_ecr_lifecycle_policy" "rag" {
  repository = aws_ecr_repository.rag.name
  policy = jsonencode({
    rules = [{
      rulePriority = 1
      description  = "Keep last 5 images"
      selection = {
        tagStatus   = "any"
        countType   = "imageCountMoreThan"
        countNumber = 5
      }
      action = { type = "expire" }
    }]
  })
}

# --- S3 (vault + chroma pré-indexado) ---
resource "aws_s3_bucket" "rag" {
  # Inclui região: nome S3 é global; App Runner não existe em sa-east-1
  bucket        = "${local.name_prefix}-rag-${local.account_id}-${var.aws_region}"
  force_destroy = true
}

resource "aws_s3_bucket_versioning" "rag" {
  bucket = aws_s3_bucket.rag.id
  versioning_configuration {
    status = "Enabled"
  }
}

resource "aws_s3_bucket_public_access_block" "rag" {
  bucket                  = aws_s3_bucket.rag.id
  block_public_acls       = true
  block_public_policy     = true
  ignore_public_acls      = true
  restrict_public_buckets = true
}

resource "aws_s3_bucket_server_side_encryption_configuration" "rag" {
  bucket = aws_s3_bucket.rag.id
  rule {
    apply_server_side_encryption_by_default {
      sse_algorithm = "AES256"
    }
  }
}

# --- IAM App Runner ---
resource "aws_iam_role" "apprunner_ecr" {
  name = "${local.name_prefix}-rag-apprunner-ecr"
  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [{
      Effect    = "Allow"
      Principal = { Service = "build.apprunner.amazonaws.com" }
      Action    = "sts:AssumeRole"
    }]
  })
}

resource "aws_iam_role_policy_attachment" "apprunner_ecr" {
  role       = aws_iam_role.apprunner_ecr.name
  policy_arn = "arn:aws:iam::aws:policy/service-role/AWSAppRunnerServicePolicyForECRAccess"
}

resource "aws_iam_role" "apprunner_instance" {
  name = "${local.name_prefix}-rag-apprunner-instance"
  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [{
      Effect    = "Allow"
      Principal = { Service = "tasks.apprunner.amazonaws.com" }
      Action    = "sts:AssumeRole"
    }]
  })
}

resource "aws_iam_role_policy" "apprunner_s3" {
  name = "${local.name_prefix}-rag-s3-read"
  role = aws_iam_role.apprunner_instance.id
  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [{
      Effect = "Allow"
      Action = [
        "s3:GetObject",
        "s3:ListBucket"
      ]
      Resource = [
        aws_s3_bucket.rag.arn,
        "${aws_s3_bucket.rag.arn}/*"
      ]
    }]
  })
}

# --- App Runner ---
resource "aws_apprunner_service" "rag" {
  service_name = "${local.name_prefix}-rag"

  source_configuration {
    authentication_configuration {
      access_role_arn = aws_iam_role.apprunner_ecr.arn
    }
    auto_deployments_enabled = false
    image_repository {
      image_identifier      = local.image_uri
      image_repository_type = "ECR"
      image_configuration {
        port = "8080"
        runtime_environment_variables = {
          RAG_BIND              = "0.0.0.0"
          RAG_PORT              = "8080"
          PORT                  = "8080"
          RAG_CHROMA_PATH       = "/data/chroma"
          RAG_VAULT_PATH        = "/data/vault/fabrica"
          RAG_PROJETOS_PATH     = "/data/vault/projetos"
          RAG_S3_BUCKET         = aws_s3_bucket.rag.bucket
          RAG_S3_CHROMA_PREFIX  = "chroma"
          RAG_API_KEY           = coalesce(var.rag_api_key, random_password.rag_api_key.result)
          AWS_DEFAULT_REGION    = var.aws_region
          RAG_MAX_RESULTS       = tostring(var.rag_max_results)
        }
      }
    }
  }

  instance_configuration {
    cpu               = var.cpu
    memory            = var.memory
    instance_role_arn = aws_iam_role.apprunner_instance.arn
  }

  health_check_configuration {
    protocol            = "HTTP"
    path                = "/health"
    interval            = 10
    timeout             = 5
    healthy_threshold   = 1
    unhealthy_threshold = 20
  }

  tags = {
    Project = local.name_prefix
    Purpose = "fabrica-rag"
  }

  depends_on = [
    aws_iam_role_policy_attachment.apprunner_ecr,
    aws_iam_role_policy.apprunner_s3,
  ]
}
