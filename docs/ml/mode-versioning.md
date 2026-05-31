# Model Versioning Strategy

## Overview

This document defines how machine learning models are versioned, stored, and deployed within MedVision-AI.

The goal is to ensure:

* Reproducibility
* Traceability
* Rollback capability
* Safe deployment

---

# Version Format

Format:

```text
MAJOR.MINOR.PATCH
```

Example:

```text
1.0.0
1.1.0
1.2.3
2.0.0
```

---

# Version Rules

## Major

Increment when:

* Architecture changes
* Class labels change
* Prediction schema changes

Example:

```text
1.0.0 → 2.0.0
```

---

## Minor

Increment when:

* New training data added
* Accuracy improvements
* Hyperparameter improvements

Example:

```text
1.0.0 → 1.1.0
```

---

## Patch

Increment when:

* Metadata fixes
* Deployment fixes
* Non-functional changes

Example:

```text
1.1.0 → 1.1.1
```

---

# Storage Structure

```text
models/
├── brain/
│   ├── v1.0.0/
│   ├── v1.1.0/
│   └── latest/
│
├── chest/
│   ├── v1.0.0/
│   └── latest/
│
├── bone/
│   ├── v1.0.0/
│   └── latest/
│
└── cardiac/
    ├── v1.0.0/
    └── latest/
```

---

# Checkpoint Format

Required structure:

```python
{
    "model_state_dict": {},
    "model_version": "1.0.0",
    "scan_type": "brain",
    "class_names": [],
    "training_date": "",
    "metrics": {}
}
```

---

# Metadata Requirements

Every model must contain:

| Field         | Required |
| ------------- | -------- |
| model_version | Yes      |
| scan_type     | Yes      |
| class_names   | Yes      |
| training_date | Yes      |
| metrics       | Yes      |

---

# Deployment Policy

## Development

May use:

```text
latest
```

tag.

---

## Production

Must use:

```text
Explicit Version
```

Example:

```text
brain:v1.2.0
```

---

# Rollback Strategy

Example:

```text
v1.3.0
   ↓
Issue Detected
   ↓
Rollback
   ↓
v1.2.0
```

Rollback should require configuration only.

No retraining required.

---

# MLflow Integration

Each version should store:

* Metrics
* Hyperparameters
* Artifacts
* Training logs

---

# API Exposure

Prediction responses should include:

```json
{
  "model_version": "1.0.0"
}
```

This enables result traceability.

---

# Version Lifecycle

```text
Training
    │
    ▼
Validation
    │
    ▼
Version Assignment
    │
    ▼
Checkpoint Export
    │
    ▼
Deployment
    │
    ▼
Monitoring
```

---

# Retirement Policy

Models may be retired when:

* Replaced by newer versions
* Clinically obsolete
* Performance degraded

Retired models should remain archived.

---

# Success Criteria

Every prediction must be traceable to:

* Dataset
* Training run
* Metrics
* Model version
* Deployment date
