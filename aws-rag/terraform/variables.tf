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
  description = "CPU App Runner: 1024 = 1 vCPU"
  default     = "1024"
}

variable "memory" {
  type        = string
  description = "RAM App Runner: 2048 ou 4096 (recomendado 4096 p/ MiniLM+Chroma)"
  default     = "4096"
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

variable "ecr_force_delete" {
  type        = bool
  description = "Permite apagar ECR mesmo com imagens (cuidado)"
  default     = false
}
