# Training Guide

## Overview

This document defines the standardized training workflow for all MedVision-AI machine learning models.

The objective is to ensure:

* Reproducible experiments
* Consistent preprocessing
* Standardized checkpoints
* Comparable evaluation metrics
* Simplified deployment

---

# Supported Models

| Scan Type   | Task                          |
| ----------- | ----------------------------- |
| Brain MRI   | Classification                |
| Chest X-Ray | Multi-label Classification    |
| Bone X-Ray  | Classification                |
| Cardiac MRI | Classification + Segmentation |

---

# Dataset Structure

## Standard Layout

```text
datasets/
├── brain/
│   ├── train/
│   ├── val/
│   └── test/
│
├── chest/
│   ├── train/
│   ├── val/
│   └── test/
│
├── bone/
│   ├── train/
│   ├── val/
│   └── test/
│
└── cardiac/
    ├── train/
    ├── val/
    └── test/
```

---

# Data Sources

## Brain MRI

Potential sources:

* Brain Tumor MRI Dataset
* RSNA Brain Hemorrhage
* OpenNeuro

---

## Chest X-Ray

Potential sources:

* ChestX-ray14
* CheXpert
* COVIDx

---

## Bone X-Ray

Potential sources:

* MURA
* FracAtlas

---

## Cardiac MRI

Potential sources:

* ACDC Dataset
* M&Ms Challenge

---

# Preprocessing Pipeline

Supported formats:

```text
PNG
JPG
JPEG
DICOM
NIfTI
```

---

## Common Operations

1. Resize
2. Normalize
3. Contrast enhancement
4. Noise reduction

---

## Brain MRI

Target size:

```text
224 × 224
```

---

## Cardiac MRI

Target size:

```text
256 × 256
```

---

# Training Configuration

Configuration stored in:

```text
config/
```

Example:

```yaml
batch_size: 16
learning_rate: 0.0001
epochs: 50
optimizer: adam
```

---

# Training Command

Example:

```bash
python trainer.py --scan-type brain
```

---

# Evaluation Metrics

## Classification

Metrics:

* Accuracy
* Precision
* Recall
* F1 Score
* ROC-AUC

---

## Multi-Label Classification

Metrics:

* Micro F1
* Macro F1
* Average Precision

---

## Segmentation

Metrics:

* Dice Score
* IoU
* Pixel Accuracy

---

# Experiment Tracking

## MLflow

Track:

* Hyperparameters
* Metrics
* Artifacts
* Checkpoints

---

## Weights & Biases

Optional integration for:

* Training curves
* Experiment comparison
* Model monitoring

---

# Model Export

Successful models are exported as:

```text
models/{scan_type}/{scan_type}_best_model.pth
```

---

# Validation Checklist

Before deployment:

* Validation accuracy acceptable
* No overfitting detected
* Model version assigned
* Metrics recorded
* Checkpoint exported

---

# Training Workflow

```text
Dataset
    │
    ▼
Preprocessing
    │
    ▼
Training
    │
    ▼
Validation
    │
    ▼
Evaluation
    │
    ▼
Checkpoint Export
    │
    ▼
Deployment
```

---

# Success Criteria

A model is deployment-ready when:

* Validation metrics meet requirements
* Checkpoint passes loading tests
* Metadata is complete
* Version is assigned
