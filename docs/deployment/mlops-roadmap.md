# MLOps Roadmap

## Objective

Build a production-ready machine learning lifecycle for MedVision-AI.

---

# Current State

Current deployment:

```text
React
 ↓
Supabase Edge Function
 ↓
FastAPI
```

Limited monitoring.

No automated model lifecycle.

---

# Phase 1 — Model Management

## Goals

Centralized model storage.

### Tasks

* Standardize checkpoints.
* Version all models.
* Store metadata.

### Deliverables

```text
models/
```

repository structure.

---

# Phase 2 — Experiment Tracking

## MLflow

Track:

* metrics
* artifacts
* checkpoints

Benefits:

* reproducibility
* auditing

---

# Phase 3 — Training Automation

Pipeline:

```text
Dataset
    ↓
Training
    ↓
Validation
    ↓
Checkpoint Export
```

Tools:

* Hydra
* OmegaConf
* MLflow

---

# Phase 4 — Monitoring

## Prometheus

Collect:

* inference latency
* throughput
* error rates
* model status

---

## Grafana

Visualize:

* uptime
* latency
* prediction volume
* model health

---

# Phase 5 — CI/CD

Pipeline:

```text
GitHub Actions
       ↓
Training
       ↓
Evaluation
       ↓
Artifact Export
       ↓
Deployment
```

---

# Phase 6 — Production Operations

## Health Checks

Endpoints:

```text
/health
/models/status
```

---

## Alerting

Alert on:

* model failures
* inference errors
* elevated latency
* missing checkpoints

---

# Container Architecture

```text
FastAPI
Redis
MLflow
Prometheus
Grafana
```

Managed through Docker Compose.

---

# Future Enhancements

* Kubernetes
* GPU autoscaling
* Model registry
* Canary deployments
* A/B testing

---

# Success Criteria

* Reproducible training.
* Automated deployment.
* Production monitoring.
* Observable ML infrastructure.
