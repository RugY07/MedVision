# Flask vs FastAPI ML Infrastructure Comparison

## Overview

MedVision-AI currently operates two separate machine learning backends:

* Flask (`backend/`)
* FastAPI (`ml-infrastructure/`)

Both perform medical image analysis but expose different APIs, deployment models, and operational capabilities.

---

# Production Path Today

```text
React SPA
    │
    ▼
Supabase Edge Function
(analyze-medical-scan)
    │
    ▼
ML_MODEL_SERVER_URL
    │
    ▼
FastAPI ML Server (:8000)
    │
    ▼
Prediction Results

Fallback:
OpenAI / Gemini / Demo

Not Connected:
Flask Backend (:5000)
```

---

# Overlapping Functionality

| Area             | Flask | FastAPI |
| ---------------- | ----- | ------- |
| Brain Analysis   | Yes   | Yes     |
| Chest Analysis   | Yes   | Yes     |
| Bone Analysis    | Yes   | Yes     |
| Cardiac Analysis | Yes   | Yes     |
| PyTorch Models   | Yes   | Yes     |
| DICOM Support    | Yes   | Yes     |
| NIfTI Support    | Yes   | Yes     |
| Health Endpoints | Yes   | Yes     |
| Model Status     | Yes   | Yes     |

---

# Features Unique to Flask

## Persistence

* SQLite database
* Scan history
* File storage
* Media serving

## Explainability

* Grad-CAM
* Overlay generation
* Visualization assets

## Specialized Models

* DenseNet chest model
* U-Net cardiac segmentation

## Development Features

* Simulation mode
* Missing-weight fallback

---

# Features Unique to FastAPI

## Production Integration

* Supabase Edge Function support
* Base64 JSON API

## Serving

* Async architecture
* Typed schemas
* OpenAPI docs

## Training

* Unified training pipeline
* MLflow integration
* Hydra configuration

## Monitoring

* Prometheus
* Grafana

---

# Class Taxonomy Differences

| Scan Type | Flask          | FastAPI               |
| --------- | -------------- | --------------------- |
| Brain     | Tumor Subtypes | Neurological Diseases |
| Chest     | Multi-label    | Single-label          |
| Bone      | Binary         | Multi-class           |
| Cardiac   | Segmentation   | Classification        |

---

# Side-by-Side Comparison

| Dimension            | Flask      | FastAPI            |
| -------------------- | ---------- | ------------------ |
| Port                 | 5000       | 8000               |
| Production Connected | No         | Yes                |
| Input Format         | Multipart  | Base64 + Multipart |
| Persistence          | SQLite     | Stateless          |
| Explainability       | Yes        | No                 |
| Training Scope       | Brain Only | All Scan Types     |
| Monitoring           | Minimal    | Full MLOps         |
| Scalability          | Limited    | High               |
| Async Support        | No         | Yes                |
| Deployment Readiness | Medium     | High               |

---

# Key Findings

1. Both backends duplicate inference functionality.
2. FastAPI already serves production traffic.
3. Flask contains valuable explainability logic.
4. Model taxonomies are incompatible.
5. Maintaining both systems increases complexity.

---

# Conclusion

FastAPI is the preferred long-term architecture because it aligns with:

* frontend integration
* cloud deployment
* scalability requirements
* MLOps objectives

Flask should be retained only as a temporary migration reference until explainability and remaining functionality are fully ported.
