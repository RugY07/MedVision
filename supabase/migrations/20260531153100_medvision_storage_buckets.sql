-- MedVision AI: Storage buckets for scan originals and PDF reports
-- Paths: {user_id}/{scan_id}/original.{ext}  |  {user_id}/{scan_id}/report.pdf

insert into storage.buckets (id, name, public, file_size_limit, allowed_mime_types)
values (
  'medical-scans',
  'medical-scans',
  false,
  52428800, -- 50 MiB (matches frontend upload limit intent)
  array[
    'image/png',
    'image/jpeg',
    'image/jpg',
    'application/dicom',
    'application/octet-stream'
  ]
)
on conflict (id) do nothing;

insert into storage.buckets (id, name, public, file_size_limit, allowed_mime_types)
values (
  'medical-reports',
  'medical-reports',
  false,
  10485760, -- 10 MiB PDF cap
  array['application/pdf']
)
on conflict (id) do nothing;

-- medical-scans: users read/write only under their own folder
create policy "medical_scans_select_own"
  on storage.objects
  for select
  to authenticated
  using (
    bucket_id = 'medical-scans'
    and (storage.foldername(name))[1] = auth.uid()::text
  );

create policy "medical_scans_insert_own"
  on storage.objects
  for insert
  to authenticated
  with check (
    bucket_id = 'medical-scans'
    and (storage.foldername(name))[1] = auth.uid()::text
  );

create policy "medical_scans_update_own"
  on storage.objects
  for update
  to authenticated
  using (
    bucket_id = 'medical-scans'
    and (storage.foldername(name))[1] = auth.uid()::text
  )
  with check (
    bucket_id = 'medical-scans'
    and (storage.foldername(name))[1] = auth.uid()::text
  );

create policy "medical_scans_delete_own"
  on storage.objects
  for delete
  to authenticated
  using (
    bucket_id = 'medical-scans'
    and (storage.foldername(name))[1] = auth.uid()::text
  );

-- medical-reports: PDF exports under user folder
create policy "medical_reports_select_own"
  on storage.objects
  for select
  to authenticated
  using (
    bucket_id = 'medical-reports'
    and (storage.foldername(name))[1] = auth.uid()::text
  );

create policy "medical_reports_insert_own"
  on storage.objects
  for insert
  to authenticated
  with check (
    bucket_id = 'medical-reports'
    and (storage.foldername(name))[1] = auth.uid()::text
  );

create policy "medical_reports_update_own"
  on storage.objects
  for update
  to authenticated
  using (
    bucket_id = 'medical-reports'
    and (storage.foldername(name))[1] = auth.uid()::text
  )
  with check (
    bucket_id = 'medical-reports'
    and (storage.foldername(name))[1] = auth.uid()::text
  );

create policy "medical_reports_delete_own"
  on storage.objects
  for delete
  to authenticated
  using (
    bucket_id = 'medical-reports'
    and (storage.foldername(name))[1] = auth.uid()::text
  );
