# Current Architecture

## Overview

MedVision-AI currently operates with two separate backend systems:

1. Flask Backend (`backend/`)
2. FastAPI ML Infrastructure (`ml-infrastructure/`)

These systems perform overlapping machine learning responsibilities but are not fully integrated.

The frontend primarily communicates with Supabase Edge Functions, which forward requests to the FastAPI inference service.

As a result, FastAPI is already part of the production inference path while Flask remains largely disconnected from user-facing workflows.

---

# Current System Architecture

```text
┌──────────────────────────────┐
│         React SPA            │
└──────────────┬───────────────┘
               │
               ▼
┌──────────────────────────────┐
│      Supabase Platform       │
│  Auth + Edge Functions       │
└──────────────┬───────────────┘
               │
               ▼
┌──────────────────────────────┐
│ analyze-medical-scan         │
│ Edge Function                │
└──────────────┬───────────────┘
               │
               ▼
┌──────────────────────────────┐
│ FastAPI ML Server (:8000)    │
└──────────────┬───────────────┘
               │
               ▼
┌──────────────────────────────┐
│ Medical AI Models            │
└──────────────────────────────┘

Fallback:
OpenAI / Gemini / Demo

Not Connected to Production Flow:

┌──────────────────────────────┐
│ Flask Backend (:5000)        │
│ SQLite + Storage             │
└──────────────────────────────┘
```

---

# Frontend Architecture

## Technology Stack

### Core

* React
* TypeScript
* Vite

### UI

* TailwindCSS
* shadcn/ui
* Lucide Icons

### State & Data

* React Hooks
* Supabase Client

---

# Current Analysis Flow

```text
User Uploads Scan
        │
        ▼
React Frontend
        │
        ▼
Supabase Edge Function
        │
        ▼
FastAPI Predict Endpoint
        │
        ▼
Prediction Response
        │
        ▼
Frontend Findings UI
```

---

# Flask Backend Architecture

## Responsibilities

* Medical image preprocessing
* ML inference
* Grad-CAM generation
* File storage
* SQLite persistence
* Scan history APIs

## Components

```text
backend/
├── app/
├── models/
├── neural_nets/
├── training/
├── storage/
└── database/
```

## Strengths

* Explainability support
* Cardiac segmentation
* Local persistence
* Simulation mode

## Weaknesses

* Not connected to frontend
* SQLite scalability limitations
* Duplicate model implementations

---

# FastAPI Architecture

## Responsibilities

* ML inference
* Model serving
* Unified training pipeline
* API documentation

## Components

```text
ml-infrastructure/
├── src/
│   ├── api/
│   ├── models/
│   ├── training/
│   ├── data/
│   └── utils/
├── config/
├── docker-compose.yml
└── requirements.txt
```

## Strengths

* Production integration
* Async serving
* MLOps tooling
* Containerized deployment

## Weaknesses

* No explainability layer
* No persistence layer
* No simulation mode

---

# Current Persistence State

## Frontend

No permanent scan history.

Analysis results are primarily transient.

## Flask

Uses:

```text
SQLite
storage/uploads
storage/results
```

## Supabase

Currently provides:

* Authentication
* Edge Functions
* Configuration management

Database persistence for scans is not yet implemented.

---

# Current ML Architecture

| Scan Type   | Flask | FastAPI |
| ----------- | ----- | ------- |
| Brain MRI   | Yes   | Yes     |
| Chest X-Ray | Yes   | Yes     |
| Bone X-Ray  | Yes   | Yes     |
| Cardiac MRI | Yes   | Yes     |

Both systems maintain separate model definitions and prediction taxonomies.

---

# Current Operational Challenges

## Duplicate Infrastructure

Two ML backends must be maintained.

## API Drift

Different request and response schemas.

## Model Drift

Different class labels for identical scan types.

## Persistence Fragmentation

SQLite exists only in Flask.

## Explainability Fragmentation

Grad-CAM exists only in Flask.

---

# Architectural Assessment

Current architecture successfully demonstrates ML inference capabilities but introduces unnecessary complexity through duplicated backend systems.

The production path already favors FastAPI through Supabase Edge Functions, making FastAPI the natural candidate for long-term consolidation.

Future architecture should:

1. Adopt FastAPI as the canonical backend.
2. Move persistence into Supabase.
3. Port explainability features from Flask.
4. Eliminate duplicate model implementations.
5. Retire the Flask service after migration completion.
