# MedVision Supabase Migrations

## Apply locally

```bash
supabase link --project-ref lassmjhayhgstpiskcid
supabase db push
```

## Apply in dashboard

Run each file in order in the Supabase SQL Editor:

1. `20260531153000_medvision_scans_persistence.sql` — tables, RLS, history view
2. `20260531153100_medvision_storage_buckets.sql` — storage buckets and policies

## Regenerate TypeScript types

```bash
npx supabase gen types typescript --project-id lassmjhayhgstpiskcid > src/integrations/supabase/types.ts
```

After regeneration, re-apply convenience exports at the bottom of `types.ts` if the CLI overwrites them.

## Schema overview

| Object | Purpose |
|--------|---------|
| `scans` | One row per user upload; `user_id` → `auth.users` |
| `analysis_results` | 1:1 AI output; `findings` JSONB matches frontend findings |
| `scan_history` | View for history lists (join scans + analysis) |
| `medical-scans` bucket | Original images at `{user_id}/{scan_id}/...` |
| `medical-reports` bucket | PDF exports at `{user_id}/{scan_id}/report.pdf` |

## Example queries (authenticated client)

```typescript
// List history (newest first)
const { data } = await supabase
  .from("scan_history")
  .select("*")
  .order("uploaded_at", { ascending: false });

// Insert scan then analysis (after edge function returns)
const { data: scan } = await supabase.from("scans").insert({
  user_id: user.id,
  scan_type: "Brain",
  original_filename: file.name,
  status: "analyzing",
}).select().single();

await supabase.from("analysis_results").insert({
  scan_id: scan.id,
  findings: results.findings,
  overall_confidence: results.overallConfidence,
  scan_type: results.scanType,
  model_type: results.modelType,
  processing_time_ms: Math.round((results.processingTime ?? 0) * 1000),
  report_snapshot: results,
  is_valid_medical_scan: true,
});
```
