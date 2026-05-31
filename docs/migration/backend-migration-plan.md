# Backend Migration Plan

## Objective

Migrate MedVision-AI from dual ML backends to a single FastAPI-based architecture.

---

# Phase 0 — Stabilization

## Goals

Establish a single source of truth.

### Tasks

* Define canonical class taxonomy.
* Define canonical model storage structure.
* Verify ML_MODEL_SERVER_URL configuration.
* Fix frontend environment references.

### Deliverables

* Taxonomy document
* Deployment configuration validation

---

# Phase 1 — Model & Preprocessing Unification

## Goals

Remove duplicate ML logic.

### Tasks

* Merge preprocessing pipelines.
* Consolidate DICOM support.
* Consolidate NIfTI support.
* Standardize image normalization.

### Model Decisions

#### Brain

Choose:

* EfficientNet-B0
  or
* EfficientNet-B4

#### Chest

Decide between:

* Multi-label classification
* Single-label classification

#### Cardiac

Decide between:

* Segmentation
* Classification

### Deliverables

Unified preprocessing package.

---

# Phase 2 — Port Flask Features

## Goals

Prevent capability regression.

### Tasks

* Port Grad-CAM.
* Port overlay generation.
* Port simulation mode.
* Add multipart parity tests.

### Deliverables

Feature-complete FastAPI service.

---

# Phase 3 — Supabase Persistence

## Goals

Replace SQLite.

### Tasks

Create:

* scans table
* analysis_results table
* storage buckets
* RLS policies

### Deliverables

Production persistence layer.

---

# Phase 4 — Frontend Integration

## Goals

Connect persistence to UI.

### Tasks

* Save scans after analysis.
* Save analysis results.
* Implement history retrieval.
* Connect storage uploads.

### Deliverables

Persistent user history.

---

# Phase 5 — MLOps

## Goals

Production readiness.

### Tasks

* MLflow integration
* Prometheus metrics
* Grafana dashboards
* Health monitoring
* CI/CD deployment

### Deliverables

Production-grade ML infrastructure.

---

# Phase 6 — Flask Retirement

## Goals

Remove duplication.

### Tasks

* Archive Flask backend.
* Update deployment docs.
* Remove references.
* Validate parity.

### Deliverables

Single FastAPI architecture.

---

# Success Criteria

* One backend
* One model taxonomy
* One inference API
* One persistence layer
