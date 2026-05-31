# Target Architecture

## Overview

The target MedVision-AI architecture uses a cloud-native, service-oriented design built around:

* React SPA
* Supabase
* FastAPI ML Infrastructure
* Medical AI Models
* Object Storage
* Monitoring Stack

The Flask backend is removed from the production architecture.

---

# High-Level Architecture

```text
┌──────────────────────────────┐
│         React SPA            │
└──────────────┬───────────────┘
               │
               ▼
┌──────────────────────────────┐
│       Supabase Auth          │
└──────────────┬───────────────┘
               │ JWT
               ▼
┌──────────────────────────────┐
│  Supabase Edge Function      │
│ analyze-medical-scan         │
└──────────────┬───────────────┘
               │
      ┌────────┴─────────┐
      ▼                  ▼
┌──────────────┐   ┌──────────────┐
│ FastAPI ML   │   │ OpenAI/Gemini│
│ Server       │   │ Fallback     │
└──────┬───────┘   └──────────────┘
       │
       ▼
┌──────────────────────────────┐
│ PyTorch Medical Models       │
└──────────────────────────────┘
```

---

# Persistence Layer

```text
User
  │
  ▼
Supabase Auth
  │
  ▼
scans
  │
  ▼
analysis_results
```

Storage:

```text
medical-scans
medical-reports
```

---

# ML Layer

Supported models:

* Brain MRI
* Chest X-Ray
* Bone X-Ray
* Cardiac MRI

Responsibilities:

* preprocessing
* inference
* confidence scoring
* explainability
* report generation

---

# Explainability Layer

Future architecture includes:

```text
Prediction
    │
    ▼
Grad-CAM
    │
    ▼
Heatmap Generation
    │
    ▼
Storage
```

Outputs:

* heatmaps
* overlays
* PDF attachments

---

# MLOps Layer

Infrastructure:

* Docker Compose
* MLflow
* Prometheus
* Grafana

Responsibilities:

* model tracking
* monitoring
* deployment
* alerting

---

# Deployment Architecture

```text
Frontend
    │
    ▼
Vercel
    │
    ▼
Supabase
    │
    ▼
FastAPI ML Server
    │
    ▼
Docker Infrastructure
```

---

# Architectural Principles

1. Stateless inference.
2. User data stored in Supabase.
3. Frontend never directly accesses ML server.
4. FastAPI is the single ML gateway.
5. Explainability is optional enrichment.
6. Storage is private by default.
7. Authentication required for persistence.
