# Deployment guide (EKS)

Handover notes for the cloud team deploying **aws-bedrock-sanity-service** to EKS.

## Overview

- **Stack:** FastAPI + Uvicorn, Python 3.12+
- **Port:** 8000 (HTTP)
- **Health:** `GET /sanity-app/v1/health` → 200 OK with `{"status":"ok"}`

Use this health URL for Kubernetes **liveness** and **readiness** probes.

---

## Environment variables

Configure these via a ConfigMap in EKS. The app reads them at startup (and for Bedrock calls).

| Variable | Required | Description |
|----------|----------|-------------|
| `AWS_REGION` | Yes | AWS region (e.g. `us-east-1`) |
| `AWS_BEDROCK_DEFAULT_PROMPT_ID` | Yes | Bedrock prompt identifier for default flow |
| `AWS_BEDROCK_DEFAULT_PROMPT_VERSION` | Yes | Version of the default prompt |
| `AWS_BEDROCK_DEFAULT_MODEL_ID` | Yes | Default Bedrock model ID (e.g. `us.anthropic.claude-3-5-sonnet-v2...`) |
| `AWS_BEDROCK_GUARDRAIL_ID` | Yes | Guardrail identifier |
| `AWS_BEDROCK_GUARDRAIL_VERSION` | Yes | Guardrail version |

**AWS credentials:** The service uses the standard AWS SDK (boto3).

---

## Building the image

```bash
docker build -t aws-bedrock-sanity-service:0.1.0 .
```

Run locally (with env from file):

```bash
docker run -p 8000:8000 --env-file .env aws-bedrock-sanity-service:0.1.0
```

Then: `curl http://localhost:8000/sanity-app/v1/health`

---

## Running locally (no Docker)

From repo root:

```bash
poetry install
poetry run uvicorn main.app:app --reload --host 0.0.0.0 --port 8000 --app-dir src
```

Requires a `.env` (or exported env vars) as in `.env.example`.

---

## Kubernetes (EKS)

Example manifests are in `k8s/` as a starting point:

- **Deployment** — app container, probes on `/sanity-app/v1/health`, env from ConfigMap
- **Service** — ClusterIP on port 8000
- **configmap.example.yaml** — copy to `configmap.yaml`, fill in values, then create the ConfigMap

Adjust namespace, image, and resource limits to match your EKS setup.

### Probe configuration

- **Liveness:** `httpGet` on `http://:8000/sanity-app/v1/health`
- **Readiness:** same path

Suggested: `initialDelaySeconds: 10`, `periodSeconds: 15`, `timeoutSeconds: 5`.

---

## API surface

| Method | Path | Description |
|--------|------|-------------|
| GET | `/sanity-app/v1/health` | Health check |
| POST | `/sanity-app/v1/bedrock-router/generate-default-response` | Body: `{"user_prompt": "..."}` |
| POST | `/sanity-app/v1/bedrock-router/generate-response-custom-prompt-id` | Body: `{"user_prompt", "prompt_id", "model_id"}` |
| POST | `/sanity-app/v1/bedrock-router/generate-response-custom-system-prompt` | Body: `{"user_prompt", "system_prompt", "model_id"}` |

All POST endpoints return the model response as plain text or a JSON error with `detail` on failure.