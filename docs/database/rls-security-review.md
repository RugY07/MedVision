# Supabase RLS & Security Review

## Scope

Review of:

* scans table
* analysis_results table
* storage buckets
* scan_history view
* generated TypeScript types

Review performed against PostgreSQL 15 and Supabase platform conventions.

---

# Summary

| Area                 | Status            |
| -------------------- | ----------------- |
| SQL migrations       | Pass              |
| Foreign keys         | Pass              |
| RLS policies         | Pass              |
| Storage policies     | Pass with caveats |
| scan_history view    | Pass              |
| TypeScript types     | Pass              |
| Production readiness | Good              |

---

# Foreign Key Validation

## scans

```text
user_id
    ↓
auth.users(id)
```

Behavior:

```text
ON DELETE CASCADE
```

Result:

Pass.

---

## analysis_results

```text
scan_id
    ↓
scans(id)
```

Behavior:

```text
UNIQUE
ON DELETE CASCADE
```

Result:

Pass.

---

# Row Level Security Review

## scans

Policies:

* select own
* insert own
* update own
* delete own

Condition:

```sql
auth.uid() = user_id
```

Result:

Pass.

---

## analysis_results

Policies validate ownership through parent scan.

Condition:

```sql
EXISTS (
    SELECT 1
    FROM scans
    WHERE scans.id = scan_id
      AND scans.user_id = auth.uid()
)
```

Result:

Pass.

---

# Security Observations

## Service Role

Important:

```text
service_role bypasses RLS
```

Recommendation:

Always derive user_id from JWT.

---

## Anonymous Access

No anonymous policies exist.

Result:

Expected behavior.

Authentication required.

---

# Storage Policy Review

Buckets:

## medical-scans

Private.

## medical-reports

Private.

Folder ownership model:

```text
{userId}/{scanId}/file
```

Policy check:

```sql
(storage.foldername(name))[1]
=
auth.uid()
```

Result:

Pass.

---

# Storage Risks

Potential issues:

1. Existing permissive policies.
2. Incorrect path structure.
3. Unsupported MIME types.
4. Orphan storage objects.

---

# scan_history View

Configuration:

```sql
security_invoker = true
```

Result:

Underlying RLS remains enforced.

Benefits:

* Simple frontend queries.
* User isolation maintained.
* Supports pending scans.

Pass.

---

# TypeScript Review

Schema and generated types are aligned.

Verified:

* enums
* tables
* views
* relationships

Potential runtime caveats:

* jsonb validation
* bigint serialization
* report_snapshot shape

---

# Deployment Checklist

Before production:

* Verify storage policies.
* Verify JWT ownership handling.
* Validate upload MIME types.
* Test scan_history queries.
* Test PDF storage access.

---

# Final Verdict

The persistence implementation satisfies:

* ownership requirements
* history retrieval requirements
* future PDF support
* Supabase security standards

Overall assessment:

Production-ready with minor operational considerations.
