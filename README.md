# AI Studio HQ

A modular, API-first control plane for GPU-backed image, video, and model-training workflows. Vast.ai is the initial compute provider. GPU workers are ephemeral; the control plane and metadata remain persistent.

## Phase 1 status

This branch adds the FastAPI foundation, Bootstrap dashboard, PostgreSQL/Redis services, HTTP Basic authentication for the UI and API, audit/job tables, and initial Vast.ai and ComfyUI adapters.

## Quick start

1. Copy `.env.example` to `.env`.
2. Set a long random `SECRET_KEY` and a strong `ADMIN_PASSWORD`.
3. Set `POSTGRES_PASSWORD` in the shell or compose environment and use the same password in `DATABASE_URL`.
4. Run `docker compose up --build -d`.
5. Open `http://localhost:8000` and sign in with the configured admin credentials.

Do not expose this development deployment directly to the internet. Put it behind TLS and a trusted reverse proxy before remote use.

## Vast.ai safety

Provisioning is disabled by default. Set `VAST_API_KEY`, set `VAST_PROVISIONING_ENABLED=true` only when ready, and configure `VAST_MAX_HOURLY_PRICE`. Never commit secrets. The create endpoint also enforces the configured hourly price ceiling.

## API

All API routes are under `/api/v1` and require HTTP Basic authentication. Initial routes cover health, Vast offer/instance operations, and ComfyUI status, prompt submission, and history.

## Architecture

Adapters isolate provider APIs from application services. Additional compute providers and trainer backends can be added without changing the dashboard's public API contract. Pinokio is intended as a Windows-side launcher, not as the Linux GPU worker runtime.

## Current limitations

This is the Phase 1 foundation, not a production-ready AI factory. Trainer execution, model downloads, dataset processing, durable workflow scheduling, worker registration, object storage, MFA, CSRF protection for browser-authenticated state-changing actions, and comprehensive tests are still planned. Validate Vast lifecycle request schemas against the current API before enabling paid provisioning.
