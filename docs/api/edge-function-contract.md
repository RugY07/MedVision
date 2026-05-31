# Edge Function Contract

## Purpose

Defines the contract between:

```text
React Frontend
        ↔
Supabase Edge Function
        ↔
FastAPI ML Server
```

---

# Frontend → Edge Function

## Endpoint

```http
POST /functions/v1/analyze-medical-scan
```

---

# Request Payload

```json
{
  "scanType": "Brain MRI",
  "fileName": "scan.jpg",
  "imageData": "base64_image"
}
```

---

# Request Fields

| Field     | Type   |
| --------- | ------ |
| scanType  | string |
| fileName  | string |
| imageData | string |

---

# Edge Function Responsibilities

1. Validate request.
2. Verify user authentication.
3. Call FastAPI server.
4. Transform ML response.
5. Persist results.
6. Return frontend response.

---

# Edge Function → FastAPI

## Request

```json
{
  "scan_type": "Brain MRI",
  "image_data": "base64_image"
}
```

---

# FastAPI Response

```json
{
  "prediction": "Tumor",
  "confidence": 91.3,
  "predictions": []
}
```

---

# Response Mapping

FastAPI:

```json
{
  "prediction": "Tumor",
  "confidence": 91.3
}
```

Frontend:

```json
{
  "findings": [
    {
      "name": "Tumor",
      "confidence": 91.3
    }
  ]
}
```

---

# Persistence Workflow

```text
Upload Scan
      │
      ▼
Store Original File
      │
      ▼
Create Scan Record
      │
      ▼
Run Inference
      │
      ▼
Create Analysis Record
      │
      ▼
Return Results
```

---

# Scan Creation

Insert:

```sql
scans
```

Required:

* user_id
* scan_type
* storage_path

---

# Analysis Creation

Insert:

```sql
analysis_results
```

Required:

* scan_id
* diagnosis
* findings
* confidence

---

# Error Handling

## ML Server Failure

Fallback:

```text
OpenAI
Gemini
Demo Response
```

---

## Storage Failure

Return:

```http
500
```

and log error.

---

# Security Requirements

The Edge Function must:

* Verify JWT.
* Extract authenticated user.
* Never trust client user_id.
* Write ownership from JWT.

---

# Ownership Flow

```text
JWT
 │
 ▼
Authenticated User
 │
 ▼
user_id
 │
 ▼
scans.user_id
```

This guarantees compatibility with Row Level Security policies.
