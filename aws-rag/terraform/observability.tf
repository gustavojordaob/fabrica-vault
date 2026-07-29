# Passo 1 — CloudWatch + SNS
# Passo 2 — S3 chroma.sqlite3 → Lambda → App Runner start-deployment

# --- SNS ---
resource "aws_sns_topic" "rag_alerts" {
  name = "${local.name_prefix}-rag-alerts"
}

resource "aws_sns_topic_subscription" "rag_alerts_email" {
  count     = var.alert_email != "" ? 1 : 0
  topic_arn = aws_sns_topic.rag_alerts.arn
  protocol  = "email"
  endpoint  = var.alert_email
}

# --- CloudWatch Alarms (App Runner) ---
resource "aws_cloudwatch_metric_alarm" "rag_5xx" {
  alarm_name          = "${local.name_prefix}-rag-5xx"
  comparison_operator = "GreaterThanOrEqualToThreshold"
  evaluation_periods  = 2
  metric_name         = "5xxStatusResponses"
  namespace           = "AWS/AppRunner"
  period              = 300
  statistic           = "Sum"
  threshold           = 10
  treat_missing_data  = "notBreaching"
  alarm_description   = "RAG App Runner com muitas respostas 5xx"
  alarm_actions       = [aws_sns_topic.rag_alerts.arn]
  ok_actions          = [aws_sns_topic.rag_alerts.arn]

  dimensions = {
    ServiceName = aws_apprunner_service.rag.service_name
    ServiceId   = aws_apprunner_service.rag.service_id
  }
}

resource "aws_cloudwatch_metric_alarm" "rag_latency" {
  alarm_name          = "${local.name_prefix}-rag-latency-p50"
  comparison_operator = "GreaterThanThreshold"
  evaluation_periods  = 3
  metric_name         = "RequestLatency"
  namespace           = "AWS/AppRunner"
  period              = 300
  statistic           = "Average"
  threshold           = 10000
  treat_missing_data  = "notBreaching"
  alarm_description   = "RAG App Runner latência média alta (>10s)"
  alarm_actions       = [aws_sns_topic.rag_alerts.arn]

  dimensions = {
    ServiceName = aws_apprunner_service.rag.service_name
    ServiceId   = aws_apprunner_service.rag.service_id
  }
}

# --- Lambda: restart após sync do chroma ---
data "archive_file" "restart_lambda" {
  type        = "zip"
  source_dir  = "${path.module}/../lambda/restart_on_chroma"
  output_path = "${path.module}/.build/restart_on_chroma.zip"
}

resource "aws_iam_role" "restart_lambda" {
  name = "${local.name_prefix}-rag-restart-lambda"
  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [{
      Effect    = "Allow"
      Principal = { Service = "lambda.amazonaws.com" }
      Action    = "sts:AssumeRole"
    }]
  })
}

resource "aws_iam_role_policy_attachment" "restart_lambda_basic" {
  role       = aws_iam_role.restart_lambda.name
  policy_arn = "arn:aws:iam::aws:policy/service-role/AWSLambdaBasicExecutionRole"
}

resource "aws_iam_role_policy" "restart_lambda_apprunner" {
  name = "${local.name_prefix}-rag-restart-apprunner"
  role = aws_iam_role.restart_lambda.id
  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [{
      Effect = "Allow"
      Action = [
        "apprunner:StartDeployment",
        "apprunner:DescribeService"
      ]
      Resource = aws_apprunner_service.rag.arn
    }]
  })
}

resource "aws_lambda_function" "restart_on_chroma" {
  function_name    = "${local.name_prefix}-rag-restart-on-chroma"
  role             = aws_iam_role.restart_lambda.arn
  handler          = "handler.handler"
  runtime          = "python3.12"
  filename         = data.archive_file.restart_lambda.output_path
  source_code_hash = data.archive_file.restart_lambda.output_base64sha256
  timeout          = 30
  memory_size      = 128

  environment {
    variables = {
      SERVICE_ARN = aws_apprunner_service.rag.arn
    }
  }

  depends_on = [
    aws_iam_role_policy_attachment.restart_lambda_basic,
    aws_iam_role_policy.restart_lambda_apprunner,
  ]
}

resource "aws_lambda_permission" "s3_invoke" {
  statement_id  = "AllowS3Invoke"
  action        = "lambda:InvokeFunction"
  function_name = aws_lambda_function.restart_on_chroma.function_name
  principal     = "s3.amazonaws.com"
  source_arn    = aws_s3_bucket.rag.arn
}

# Só dispara no sqlite do Chroma (1x por sync, não em cada arquivo do vault)
resource "aws_s3_bucket_notification" "chroma_restart" {
  bucket = aws_s3_bucket.rag.id

  lambda_function {
    lambda_function_arn = aws_lambda_function.restart_on_chroma.arn
    events              = ["s3:ObjectCreated:*"]
    filter_prefix       = "chroma/"
    filter_suffix       = "chroma.sqlite3"
  }

  depends_on = [aws_lambda_permission.s3_invoke]
}
