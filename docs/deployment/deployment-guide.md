# Deployment Guide

## Overview

This document describes the deployment architecture for MedVision-AI.

The deployment strategy follows a cloud-native architecture based on:

* React SPA
* Supabase
* FastAPI ML Server
* Docker
* MLflow
* Monitoring stack

---

# Deployment Architecture

```text id="u1lq4v"
Users
  │
  ▼
React SPA
  │
  ▼
Supabase
(Auth + Edge Functions + Database + Storage)
  │
  ▼
FastAPI ML Server
  │
  ▼
Medical AI Models
```

---

# Components

## Frontend

Technology:

* React
* TypeScript
* Vite

Deployment Targets:

* Vercel
* Netlify
* Cloudflare Pages

---

## Backend

Technology:

* FastAPI
* Uvicorn

Deployment Targets:

* Docker
* VPS
* Cloud Run
* Kubernetes

---

## Database

Technology:

* Supabase Postgres

Responsibilities:

* User management
* Scan history
* Analysis results
* Audit records

---

## Storage

Buckets:

```text id="o2hn40"
medical-scans
medical-reports
```

Responsibilities:

* Original uploads
* Generated PDFs
* Explainability assets

---

# Environment Variables

## Frontend

```env id="d8wz34"
VITE_SUPABASE_URL=
VITE_SUPABASE_ANON_KEY=
```

---

## Edge Functions

```env id="gobxfr"
ML_MODEL_SERVER_URL=
OPENAI_API_KEY=
GEMINI_API_KEY=
```

---

## ML Server

```env id="5pof9w"
MODEL_PATH=
MODEL_VERSION=
DEMO_MODE=false
```

---

# Docker Deployment

## Start Services

```bash id="5y4g79"
docker compose up -d
```

---

## Stop Services

```bash id="6zjlwm"
docker compose down
```

---

# Deployment Workflow

```text id="sj70ri"
Code Push
    │
    ▼
GitHub
    │
    ▼
CI/CD Pipeline
    │
    ▼
Build Containers
    │
    ▼
Deploy Services
```

---

# Verification Checklist

## Frontend

* Site accessible
* Authentication working
* Scan upload working

---

## Edge Functions

* Function deployed
* Secrets configured
* Logs healthy

---

## ML Server

* Health endpoint active
* Models loaded
* Inference successful

---

## Database

* Migrations applied
* RLS enabled
* Storage buckets created

---

# Disaster Recovery

## Database

Supabase backups enabled.

---

## Models

Store versioned checkpoints externally.

Recommended:

* S3
* Cloud Storage
* MLflow Registry

---

# Deployment Success Criteria

* Frontend reachable
* Edge Functions operational
* ML inference functioning
* Persistence working
* Monitoring active
