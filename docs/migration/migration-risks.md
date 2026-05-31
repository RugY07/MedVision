# Migration Risks

## Purpose

This document identifies technical, architectural, operational, and product risks associated with migrating MedVision-AI to a unified FastAPI architecture.

---

# Risk Matrix

| Risk                            | Severity | Likelihood |
| ------------------------------- | -------- | ---------- |
| Class taxonomy mismatch         | High     | High       |
| Cardiac architecture conflict   | High     | Medium     |
| Missing trained weights         | High     | Medium     |
| Storage policy misconfiguration | High     | Medium     |
| Service-role misuse             | High     | Medium     |
| API contract drift              | Medium   | Medium     |
| Migration downtime              | Medium   | Low        |

---

# Risk 1: Class Taxonomy Mismatch

## Description

Flask and FastAPI use different labels.

Example:

### Flask

```text
glioma
meningioma
pituitary
notumor
```

### FastAPI

```text
tumor
stroke
hemorrhage
atrophy
normal
```

## Impact

* Incorrect diagnosis mapping
* UI inconsistencies
* Historical data conflicts

## Mitigation

Create a canonical taxonomy document before migration.

---

# Risk 2: Cardiac Model Conflict

## Description

Flask uses segmentation.

FastAPI uses classification.

## Impact

Different clinical outputs.

## Mitigation

Product decision required before implementation.

---

# Risk 3: Missing Production Weights

## Description

Repository currently does not contain production-ready model weights.

## Impact

Inference unavailable.

## Mitigation

* Retrain models
* Import checkpoints
* Enable DEMO_MODE

---

# Risk 4: Storage Security

## Description

Legacy storage policies may remain active.

## Impact

Unauthorized file access.

## Mitigation

Audit all storage policies before deployment.

---

# Risk 5: Service Role Misuse

## Description

Supabase service role bypasses RLS.

## Impact

Cross-user data exposure.

## Mitigation

Always derive ownership from authenticated JWT.

---

# Risk 6: API Drift

## Description

Frontend contracts may diverge from ML responses.

## Impact

Runtime failures.

## Mitigation

Version API responses.

---

# Risk 7: Migration Downtime

## Description

Schema migration may temporarily affect production.

## Impact

Unavailable history.

## Mitigation

Use staging validation before production rollout.

---

# Success Criteria

Migration is successful when:

* FastAPI is sole backend.
* Flask is archived.
* Persistence is operational.
* Monitoring is active.
* No API contract regressions occur.
