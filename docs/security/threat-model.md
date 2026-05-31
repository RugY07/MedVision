# Threat Model

## Overview

This document identifies security risks and mitigation strategies for MedVision-AI.

---

# System Assets

Critical assets:

* User accounts
* Medical images
* Analysis reports
* PDF exports
* ML models
* Supabase database

---

# Trust Boundaries

```text id="f3lpkx"
User Browser
      │
      ▼
React Frontend
      │
      ▼
Supabase
      │
      ▼
FastAPI ML Server
```

---

# Threat Categories

## Authentication Threats

### Risk

Unauthorized account access.

### Mitigation

* Supabase Auth
* Secure JWT validation
* Session expiration

---

## Authorization Threats

### Risk

User accesses another user's scans.

### Mitigation

* Row Level Security
* Ownership validation
* Storage policies

---

## Storage Threats

### Risk

Unauthorized file downloads.

### Mitigation

Private buckets:

```text id="vifvok"
medical-scans
medical-reports
```

RLS-enforced access.

---

## API Abuse

### Risk

Excessive requests.

### Mitigation

* Rate limiting
* Request validation
* Logging

---

## File Upload Threats

### Risk

Malicious file uploads.

### Mitigation

* MIME validation
* File size limits
* Virus scanning (future)

---

## ML-Specific Threats

### Risk

Adversarial inputs.

### Mitigation

* Input validation
* Confidence thresholds
* Monitoring

---

## Data Leakage

### Risk

Medical data exposed publicly.

### Mitigation

* Private storage
* HTTPS
* Secure access policies

---

# Threat Matrix

| Threat                   | Severity |
| ------------------------ | -------- |
| Account Compromise       | High     |
| Unauthorized Scan Access | High     |
| Storage Misconfiguration | High     |
| API Abuse                | Medium   |
| Adversarial Inputs       | Medium   |
| Denial of Service        | Medium   |
| Model Theft              | Low      |

---

# Security Controls

## Authentication

* JWT-based auth
* Supabase Auth

---

## Authorization

* RLS policies
* Ownership checks

---

## Encryption

* HTTPS in transit
* Cloud encryption at rest

---

## Logging

* Authentication events
* Storage events
* Inference events

---

# Future Improvements

* MFA
* Security audits
* Penetration testing
* WAF integration
* Virus scanning

---

# Success Criteria

Security is successful when:

* Users access only their own data.
* Medical files remain private.
* Storage buckets remain protected.
* Audit trails are available.
