# ADR-001: FastAPI as Canonical ML Backend

## Status

Accepted

## Date

2026-05-31

## Context

MedVision-AI currently contains two independent ML backends:

1. Flask backend (`backend/`)
2. FastAPI backend (`ml-infrastructure/`)

Both systems provide inference capabilities for:

* Brain MRI
* Chest X-Ray
* Bone X-Ray
* Cardiac Imaging

However, they differ significantly in:

* API contracts
* Model taxonomy
* Persistence strategy
* Training infrastructure
* Deployment architecture

The React frontend does not communicate directly with Flask.

Production analysis currently follows:

```text
React SPA
    ↓
Supabase Edge Function
    ↓
ML_MODEL_SERVER_URL
    ↓
FastAPI ML Server
```

Therefore FastAPI is already the active inference service.

## Decision

FastAPI shall become the single canonical ML backend for MedVision-AI.

All future ML development, training, deployment, and inference will be centered around the FastAPI service.

Flask functionality that remains valuable shall be migrated into FastAPI before Flask is retired.

## Rationale

### Production Alignment

FastAPI is already integrated with Supabase Edge Functions.

No frontend integration currently depends on Flask.

### API Compatibility

FastAPI accepts:

* Base64 JSON
* Multipart uploads

which matches the frontend image handling workflow.

### Scalability

FastAPI is:

* asynchronous
* stateless
* container-friendly

making it suitable for cloud deployment.

### MLOps Support

FastAPI infrastructure already includes:

* Docker Compose
* MLflow
* Prometheus
* Grafana
* Hydra/OmegaConf

Flask does not provide equivalent operational tooling.

### Unified Training

FastAPI supports training pipelines for all scan types.

Flask only provides training support for Brain MRI.

## Consequences

### Positive

* Single inference API
* Reduced maintenance burden
* Elimination of duplicate models
* Unified deployment architecture
* Improved observability

### Negative

* Migration effort required
* Flask-specific features must be ported
* Class taxonomy must be unified

## Features to Migrate

Before Flask retirement:

* Grad-CAM explainability
* XAI overlays
* Demo/simulation mode
* Useful preprocessing logic

## Features to Retire

* Flask REST API
* SQLite persistence
* Duplicate model definitions
* Flask deployment infrastructure

## Review Date

After completion of Phase 6 migration.
