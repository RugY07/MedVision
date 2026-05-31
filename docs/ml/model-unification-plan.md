
# Model Unification Plan

## Objective

Create a single training and inference ecosystem for MedVision-AI.

---

# Goals

1. Eliminate duplicate model definitions.
2. Standardize class labels.
3. Standardize checkpoints.
4. Standardize preprocessing.
5. Support explainability.

---

# Canonical Model Structure

```text
models/
├── brain/
│   └── brain_best_model.pth
│
├── chest/
│   └── chest_best_model.pth
│
├── bone/
│   └── bone_best_model.pth
│
└── cardiac/
    └── cardiac_best_model.pth
```

---

# Preprocessing Standardization

Merge:

```text
backend/app/preprocessors.py
```

and

```text
ml-infrastructure/src/data/preprocessing.py
```

into:

```text
ml-infrastructure/src/preprocessing/
```

Supported formats:

* PNG
* JPG
* JPEG
* DICOM
* NIfTI

---

# Brain Strategy

## Current Conflict

Flask:

```text
Tumor subtype model
```

FastAPI:

```text
General pathology model
```

## Recommendation

Phase 1:

Adopt FastAPI model.

Phase 2:

Introduce subtype classification as secondary model.

---

# Chest Strategy

## Current Conflict

Flask:

```text
Multi-label
```

FastAPI:

```text
Single-label
```

## Recommendation

Use multi-label architecture.

Reason:

Patients may exhibit multiple findings.

---

# Bone Strategy

Recommendation:

Adopt FastAPI taxonomy.

Benefits:

* More diagnoses
* Future extensibility

---

# Cardiac Strategy

## Current Conflict

Flask:

```text
Segmentation
```

FastAPI:

```text
Classification
```

## Recommendation

Keep both.

Pipeline:

```text
Classification
        +
Segmentation
```

Classification:

* diagnosis

Segmentation:

* measurements
* explainability

---

# Explainability Integration

Port:

```text
Grad-CAM
```

from Flask.

Outputs:

* heatmaps
* overlays
* PDF visualizations

---

# Checkpoint Standard

Required fields:

```json
{
  "model_state_dict": {},
  "scan_type": "",
  "model_version": "",
  "class_names": []
}
```

---

# Success Criteria

* One preprocessing pipeline.
* One model directory.
* One prediction schema.
* One deployment strategy.
