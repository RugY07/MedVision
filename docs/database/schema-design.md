# Supabase Persistence Design

## Overview

MedVision-AI stores medical scans, AI-generated analysis results, and future PDF reports using Supabase Postgres and Supabase Storage.

The schema is designed to support:

* User-owned scans
* Historical analysis retrieval
* PDF report exports
* Storage-backed medical files
* Secure Row Level Security

---

# Entity Relationship Diagram

```text
auth.users
    │
    ▼
scans
    │
    ▼
analysis_results
```

Relationship:

```text
User
  └── Many Scans

Scan
  └── One Analysis Result
```

---

# scans Table

Represents uploaded medical scans.

## Core Fields

| Column          | Type        |
| --------------- | ----------- |
| id              | uuid        |
| user_id         | uuid        |
| scan_type       | text        |
| filename        | text        |
| storage_path    | text        |
| file_size_bytes | bigint      |
| status          | scan_status |
| uploaded_at     | timestamptz |
| updated_at      | timestamptz |

## Supported Scan Types

* Brain MRI
* Chest/Lungs
* Bone X-Ray
* Cardiac MRI

---

# analysis_results Table

Stores inference outputs.

## Core Fields

| Column             | Type    |
| ------------------ | ------- |
| id                 | uuid    |
| scan_id            | uuid    |
| primary_diagnosis  | text    |
| overall_confidence | integer |
| findings           | jsonb   |
| report_snapshot    | jsonb   |
| recommendations    | text    |
| processing_time_ms | integer |

---

# PDF Export Support

Future reporting fields:

| Column           | Type              |
| ---------------- | ----------------- |
| pdf_status       | pdf_export_status |
| pdf_storage_path | text              |
| pdf_generated_at | timestamptz       |

States:

* pending
* generating
* completed
* failed

---

# Storage Buckets

## medical-scans

Private bucket.

Stores:

```text
{userId}/{scanId}/original-file
```

## medical-reports

Private bucket.

Stores:

```text
{userId}/{scanId}/report.pdf
```

---

# Scan History View

Purpose:

Single query endpoint for dashboard history.

View:

```text
scan_history
```

Combines:

* scans
* analysis_results

Supports:

* listing
* sorting
* filtering

without additional joins.

---

# Security Model

Ownership enforced via:

```text
auth.users
    ↓
scans.user_id
    ↓
analysis_results.scan_id
```

Only authenticated users may access their records.

---

# Future Extensions

Planned additions:

* Audit logging
* PDF version history
* Model version tracking
* AI explainability assets
* Multi-language reports
