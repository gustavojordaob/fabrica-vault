variable "aws_region" {
  type        = string
  description = "Região AWS (sa-east-1 = São Paulo, us-east-1 = mais barato)"
  default     = "us-east-1"
}

variable "project_name" {
  type        = string
  description = "Prefixo dos recursos"
  default     = "fabrica"
}

variable "image_tag" {
  type        = string
  description = "Tag da imagem no ECR (após build-push)"
  default     = "latest"
}

variable "cpu" {
  type        = string
  description = "CPU App Runner: 1024 = 1 vCPU, 2048 = 2 vCPU (recomendado c/ rerank)"
  default     = "2048"
}

variable "memory" {
  type        = string
  description = "RAM: com rerank use 8192 (2 vCPU). 4096 estoura no warmup do bge."
  default     = "8192"
}

variable "rag_api_key" {
  type        = string
  description = "Chave X-RAG-Key. Vazio = Terraform gera aleatória"
  default     = ""
  sensitive   = true
}

variable "rag_max_results" {
  type    = number
  default = 5
}

variable "rag_rerank" {
  type        = string
  description = "1 = CrossEncoder lazy na 1ª busca. 0 = só híbrido."
  default     = "1"
}

variable "rag_rerank_model" {
  type        = string
  description = "Modelo CrossEncoder. No App Runner use bge-reranker-base (mais leve que v2-m3)."
  default     = "BAAI/bge-reranker-base"
}

variable "rag_rerank_pool" {
  type        = number
  description = "Quantos candidatos passam pelo rerank (menor = menos RAM/CPU)."
  default     = 12
}

variable "ecr_force_delete" {
  type        = bool
  description = "Permite apagar ECR mesmo com imagens (cuidado)"
  default     = false
}

variable "alert_email" {
  type        = string
  description = "E-mail para alarmes CloudWatch (SNS). Vazio = tópico sem subscription."
  default     = ""
}
