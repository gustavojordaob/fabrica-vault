# Lambda: S3 (chroma) → App Runner start-deployment
# Empacotada pelo Terraform (archive_file).

import json
import os
import boto3

apprunner = boto3.client("apprunner")
SERVICE_ARN = os.environ["SERVICE_ARN"]


def handler(event, context):
    """Dispara restart do App Runner quando o índice Chroma sobe no S3."""
    keys = []
    for rec in event.get("Records") or []:
        keys.append(rec.get("s3", {}).get("object", {}).get("key", ""))

    # Evita restart se já estiver deployando
    try:
        svc = apprunner.describe_service(ServiceArn=SERVICE_ARN)["Service"]
        status = svc.get("Status", "")
        if status in ("OPERATION_IN_PROGRESS", "CREATE_FAILED", "DELETE_FAILED"):
            return {
                "ok": False,
                "skipped": True,
                "reason": f"status={status}",
                "keys": keys,
            }
    except Exception as e:
        return {"ok": False, "error": f"describe_service: {e}", "keys": keys}

    resp = apprunner.start_deployment(ServiceArn=SERVICE_ARN)
    return {
        "ok": True,
        "operationId": resp.get("OperationId"),
        "keys": keys,
    }
