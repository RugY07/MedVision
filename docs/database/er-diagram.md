# Entity Relationship Diagram

## Overview

MedVision-AI persistence is built on Supabase Postgres.

The schema is designed around:

* authenticated users
* uploaded scans
* AI analysis results
* future PDF reports

---

# High-Level ER Diagram

```text
auth.users
     │
     │ 1:N
     ▼
+------------------+
|      scans       |
+------------------+
| id               |
| user_id          |
| scan_type        |
| filename         |
| storage_path     |
| status           |
| uploaded_at      |
| updated_at       |
+------------------+
     │
     │ 1:1
     ▼
+----------------------+
|  analysis_results    |
+----------------------+
| id                   |
| scan_id              |
| diagnosis            |
| confidence           |
| findings             |
| recommendations      |
| report_snapshot      |
| pdf_status           |
| pdf_storage_path     |
+----------------------+
```

---

# User Relationship

```text
User
  │
  ├── Scan
  ├── Scan
  ├── Scan
  └── Scan
```

A user may own many scans.

---

# Scan Relationship

```text
Scan
   │
   ▼
Analysis Result
```

One scan produces one analysis record.

---

# Foreign Keys

## scans

```sql
user_id
REFERENCES auth.users(id)
ON DELETE CASCADE
```

---

## analysis_results

```sql
scan_id
REFERENCES scans(id)
ON DELETE CASCADE
```

---

# Storage Relationships

## medical-scans Bucket

Path:

```text
{userId}/{scanId}/original-file
```

Example:

```text
e3f1.../brain-scan-001/image.jpg
```

---

## medical-reports Bucket

Path:

```text
{userId}/{scanId}/report.pdf
```

---

# Ownership Model

```text
auth.users
      │
      ▼
scans.user_id
      │
      ▼
analysis_results.scan_id
```

Ownership propagates from user → scan → analysis.

---

# Row Level Security Model

## scans

```sql
auth.uid() = user_id
```

---

## analysis_results

```sql
EXISTS (
    SELECT 1
    FROM scans
    WHERE scans.id = scan_id
    AND scans.user_id = auth.uid()
)
```

---

# scan_history View

```text
scans
   LEFT JOIN
analysis_results
```

Purpose:

* dashboard history
* pagination
* filtering
* sorting

without requiring frontend joins.

---

# Future Extensions

Planned entities:

```text
users
 ├── scans
 │     ├── analysis_results
 │     ├── heatmaps
 │     └── overlays
 │
 └── pdf_reports
```

Potential future additions:

* model_versions
* audit_logs
* notifications
* AI explainability assets

---

# Design Goals

1. Strong ownership model.
2. Secure access control.
3. Easy history retrieval.
4. PDF export support.
5. Cloud-native scalability.
