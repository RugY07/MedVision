-- MedVision AI: scan persistence (scans + analysis_results)
-- Apply with: supabase db push  (or run in Supabase SQL editor)

-- ---------------------------------------------------------------------------
-- Extensions
-- ---------------------------------------------------------------------------
create extension if not exists "pgcrypto";

-- ---------------------------------------------------------------------------
-- Enums
-- ---------------------------------------------------------------------------
create type public.scan_status as enum (
  'pending',
  'analyzing',
  'completed',
  'failed'
);

create type public.pdf_export_status as enum (
  'not_requested',
  'pending',
  'ready',
  'failed'
);

-- ---------------------------------------------------------------------------
-- scans
-- ---------------------------------------------------------------------------
create table public.scans (
  id uuid primary key default gen_random_uuid(),
  user_id uuid not null references auth.users (id) on delete cascade,
  scan_type text not null,
  original_filename text not null,
  storage_path text,
  content_type text,
  file_size_bytes bigint check (file_size_bytes is null or file_size_bytes >= 0),
  status public.scan_status not null default 'pending',
  created_at timestamptz not null default timezone('utc', now()),
  updated_at timestamptz not null default timezone('utc', now()),
  constraint scans_scan_type_check check (
    scan_type in ('Brain', 'Chest/Lungs', 'Cardiac', 'Bone')
  )
);

comment on table public.scans is 'User-uploaded medical scans; one row per upload session.';
comment on column public.scans.storage_path is 'Supabase Storage object path, e.g. {user_id}/{scan_id}/original.dcm';
comment on column public.scans.status is 'Lifecycle: pending → analyzing → completed | failed';

create index scans_user_id_created_at_idx
  on public.scans (user_id, created_at desc);

create index scans_user_id_status_idx
  on public.scans (user_id, status);

-- ---------------------------------------------------------------------------
-- analysis_results (1:1 with scans)
-- ---------------------------------------------------------------------------
create table public.analysis_results (
  id uuid primary key default gen_random_uuid(),
  scan_id uuid not null unique references public.scans (id) on delete cascade,
  findings jsonb not null default '[]'::jsonb,
  overall_confidence integer not null,
  scan_type text not null,
  model_type text,
  processing_time_ms integer check (processing_time_ms is null or processing_time_ms >= 0),
  model_used text,
  is_valid_medical_scan boolean not null default true,
  hindi_translation text,
  report_snapshot jsonb not null default '{}'::jsonb,
  pdf_storage_path text,
  pdf_status public.pdf_export_status not null default 'not_requested',
  pdf_generated_at timestamptz,
  created_at timestamptz not null default timezone('utc', now()),
  updated_at timestamptz not null default timezone('utc', now()),
  constraint analysis_results_overall_confidence_check check (
    overall_confidence >= 0 and overall_confidence <= 100
  ),
  constraint analysis_results_scan_type_check check (
    scan_type in ('Brain', 'Chest/Lungs', 'Cardiac', 'Bone')
  ),
  constraint analysis_results_findings_is_array check (jsonb_typeof(findings) = 'array')
);

comment on table public.analysis_results is 'AI analysis output for a scan; aligns with frontend AnalysisResults shape.';
comment on column public.analysis_results.findings is 'Array of findings: id, title, severity, confidence, description, location?';
comment on column public.analysis_results.report_snapshot is 'Full analysis payload for PDF regeneration and audit';
comment on column public.analysis_results.pdf_storage_path is 'Supabase Storage path to generated PDF report';
comment on column public.analysis_results.hindi_translation is 'Optional Hindi report text from translate-to-hindi';

create index analysis_results_scan_id_idx on public.analysis_results (scan_id);

create index analysis_results_pdf_status_idx
  on public.analysis_results (pdf_status)
  where pdf_status in ('pending', 'ready');

-- ---------------------------------------------------------------------------
-- updated_at trigger
-- ---------------------------------------------------------------------------
create or replace function public.set_updated_at()
returns trigger
language plpgsql
as $$
begin
  new.updated_at = timezone('utc', now());
  return new;
end;
$$;

create trigger scans_set_updated_at
  before update on public.scans
  for each row
  execute function public.set_updated_at();

create trigger analysis_results_set_updated_at
  before update on public.analysis_results
  for each row
  execute function public.set_updated_at();

-- ---------------------------------------------------------------------------
-- History view (list scans with latest analysis metadata)
-- ---------------------------------------------------------------------------
create or replace view public.scan_history
with (security_invoker = true)
as
select
  s.id as scan_id,
  s.user_id,
  s.scan_type,
  s.original_filename,
  s.storage_path,
  s.status as scan_status,
  s.created_at as uploaded_at,
  s.updated_at as scan_updated_at,
  ar.id as analysis_id,
  ar.overall_confidence,
  ar.model_type,
  ar.processing_time_ms,
  ar.model_used,
  ar.pdf_storage_path,
  ar.pdf_status,
  ar.pdf_generated_at,
  ar.created_at as analyzed_at
from public.scans s
left join public.analysis_results ar on ar.scan_id = s.id;

comment on view public.scan_history is 'Per-user scan history list; filter with user_id = auth.uid() via RLS on underlying tables.';

-- ---------------------------------------------------------------------------
-- Row Level Security
-- ---------------------------------------------------------------------------
alter table public.scans enable row level security;
alter table public.analysis_results enable row level security;

-- scans: owner-only CRUD
create policy "scans_select_own"
  on public.scans
  for select
  to authenticated
  using (auth.uid() = user_id);

create policy "scans_insert_own"
  on public.scans
  for insert
  to authenticated
  with check (auth.uid() = user_id);

create policy "scans_update_own"
  on public.scans
  for update
  to authenticated
  using (auth.uid() = user_id)
  with check (auth.uid() = user_id);

create policy "scans_delete_own"
  on public.scans
  for delete
  to authenticated
  using (auth.uid() = user_id);

-- analysis_results: access only when parent scan is owned
create policy "analysis_results_select_own"
  on public.analysis_results
  for select
  to authenticated
  using (
    exists (
      select 1
      from public.scans s
      where s.id = analysis_results.scan_id
        and s.user_id = auth.uid()
    )
  );

create policy "analysis_results_insert_own"
  on public.analysis_results
  for insert
  to authenticated
  with check (
    exists (
      select 1
      from public.scans s
      where s.id = analysis_results.scan_id
        and s.user_id = auth.uid()
    )
  );

create policy "analysis_results_update_own"
  on public.analysis_results
  for update
  to authenticated
  using (
    exists (
      select 1
      from public.scans s
      where s.id = analysis_results.scan_id
        and s.user_id = auth.uid()
    )
  )
  with check (
    exists (
      select 1
      from public.scans s
      where s.id = analysis_results.scan_id
        and s.user_id = auth.uid()
    )
  );

create policy "analysis_results_delete_own"
  on public.analysis_results
  for delete
  to authenticated
  using (
    exists (
      select 1
      from public.scans s
      where s.id = analysis_results.scan_id
        and s.user_id = auth.uid()
    )
  );

-- ---------------------------------------------------------------------------
-- Grants
-- ---------------------------------------------------------------------------
grant usage on schema public to authenticated;
grant select, insert, update, delete on public.scans to authenticated;
grant select, insert, update, delete on public.analysis_results to authenticated;
grant select on public.scan_history to authenticated;
grant usage on type public.scan_status to authenticated;
grant usage on type public.pdf_export_status to authenticated;
