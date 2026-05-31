# Model Taxonomy Comparison

## Purpose

This document compares the prediction taxonomies currently implemented in Flask and FastAPI and defines the challenges associated with unifying them.

---

# Brain MRI

## Flask

Classes:

```text
glioma
meningioma
pituitary
notumor
```

Architecture:

```text
EfficientNet-B0
```

Clinical Focus:

* Tumor subtype classification

---

## FastAPI

Classes:

```text
normal
tumor
stroke
hemorrhage
atrophy
```

Architecture:

```text
EfficientNet-B4
```

Clinical Focus:

* General neurological abnormality detection

---

## Difference

Flask:

```text
Specific tumor categories
```

FastAPI:

```text
General pathology categories
```

These outputs are not directly compatible.

---

# Chest Imaging

## Flask

Classes:

```text
pneumonia
infiltration
covid
pneumothorax
tuberculosis
lung_cancer
```

Prediction Type:

```text
Multi-label
```

Architecture:

```text
DenseNet-121
```

---

## FastAPI

Classes:

```text
normal
pneumonia
covid
tuberculosis
lung_cancer
pneumothorax
```

Prediction Type:

```text
Single-label classification
```

Architecture:

```text
EfficientNet
```

---

## Difference

Flask can predict multiple diseases simultaneously.

FastAPI predicts a single dominant diagnosis.

---

# Bone Imaging

## Flask

Classes:

```text
normal
fracture
```

---

## FastAPI

Classes:

```text
normal
fracture
osteoporosis
arthritis
tumor
```

---

## Difference

FastAPI provides broader diagnostic coverage.

---

# Cardiac Imaging

## Flask

Output:

```text
Segmentation
```

Classes:

```text
background
left_ventricle
right_ventricle
myocardium
```

Architecture:

```text
U-Net
```

---

## FastAPI

Output:

```text
Classification
```

Classes:

```text
normal
cardiomyopathy
valvular_disease
coronary_disease
arrhythmia
```

Architecture:

```text
ResNet50
```

---

## Difference

Fundamentally different ML tasks.

Segmentation ≠ Classification.

---

# Summary Table

| Scan Type | Flask          | FastAPI               | Compatible |
| --------- | -------------- | --------------------- | ---------- |
| Brain     | Tumor Subtypes | Neurological Diseases | No         |
| Chest     | Multi-label    | Single-label          | No         |
| Bone      | Binary         | Multi-class           | Partial    |
| Cardiac   | Segmentation   | Classification        | No         |

---

# Key Finding

The two systems are not drop-in replacements.

A canonical taxonomy must be established before migration can be completed.
