# Inference API Specification

## Overview

This document defines the canonical ML inference API for MedVision-AI.

The API is served by the FastAPI ML infrastructure and accessed through Supabase Edge Functions.

The React frontend must never communicate directly with the ML server in production.

---

# Architecture

```text
React SPA
    │
    ▼
Supabase Edge Function
    │
    ▼
FastAPI ML Server
```

---

# Base URL

Development:

```text
http://localhost:8000
```

Production:

```text
ML_MODEL_SERVER_URL
```

---

# Health Check

## Endpoint

```http
GET /health
```

## Response

```json
{
  "status": "healthy",
  "version": "1.0.0"
}
```

---

# Model Status

## Endpoint

```http
GET /models/status
```

## Response

```json
{
  "brain": true,
  "chest": true,
  "bone": true,
  "cardiac": true
}
```

---

# Prediction Endpoint

## Endpoint

```http
POST /predict
```

## Request

```json
{
  "scan_type": "Brain MRI",
  "image_data": "base64_encoded_image",
  "confidence_threshold": 0.5
}
```

---

# Request Fields

| Field                | Type   | Required |
| -------------------- | ------ | -------- |
| scan_type            | string | Yes      |
| image_data           | string | Yes      |
| confidence_threshold | number | No       |

---

# Supported Scan Types

```text
Brain MRI
Chest/Lungs
Bone X-Ray
Cardiac MRI
```

---

# Prediction Response

```json
{
  "scan_type": "Brain MRI",
  "prediction": "Tumor",
  "confidence": 92.4,
  "predictions": [
    {
      "label": "Tumor",
      "confidence": 92.4
    },
    {
      "label": "Normal",
      "confidence": 7.6
    }
  ],
  "model_version": "1.0.0",
  "processing_time_ms": 1250
}
```

---

# Response Fields

| Field              | Description        |
| ------------------ | ------------------ |
| prediction         | Top prediction     |
| confidence         | Top confidence     |
| predictions        | Ranked results     |
| model_version      | Model version      |
| processing_time_ms | Inference duration |

---

# Explainability (Future)

Optional fields:

```json
{
  "heatmap_url": "...",
  "overlay_url": "..."
}
```

---

# Error Responses

## Invalid Scan Type

```http
400 Bad Request
```

```json
{
  "error": "Unsupported scan type"
}
```

---

## Model Not Loaded

```http
503 Service Unavailable
```

```json
{
  "error": "Model unavailable"
}
```

---

## Internal Error

```http
500 Internal Server Error
```

```json
{
  "error": "Inference failed"
}
```

---

# Versioning

Current version:

```text
v1
```

Future changes must remain backward compatible or introduce a new API version.
