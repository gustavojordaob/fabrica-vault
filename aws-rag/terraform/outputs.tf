output "service_url" {
  description = "URL pública do RAG (use no MCP)"
  value       = "https://${aws_apprunner_service.rag.service_url}"
}

output "buscar_url" {
  value = "https://${aws_apprunner_service.rag.service_url}/buscar"
}

output "health_url" {
  value = "https://${aws_apprunner_service.rag.service_url}/health"
}

output "ecr_repository_url" {
  value = aws_ecr_repository.rag.repository_url
}

output "s3_bucket" {
  description = "Bucket do índice Chroma (sync-push sobe aqui)"
  value       = aws_s3_bucket.rag.bucket
}

output "rag_api_key" {
  description = "Header X-RAG-Key para /buscar"
  value       = coalesce(var.rag_api_key, random_password.rag_api_key.result)
  sensitive   = true
}

output "aws_region" {
  value = var.aws_region
}
