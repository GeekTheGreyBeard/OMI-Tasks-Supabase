-- OMI-Tasks-Supabase complete setup SQL
-- Fresh Postgres/Supabase-compatible schema for reviewing Omi-derived task candidates.
-- Safe to re-run for additive objects. No secrets or private task data are included.

create extension if not exists pgcrypto;
create schema if not exists tasks;

create table if not exists tasks.source_systems (
  source_system_id uuid primary key default gen_random_uuid(),
  source_key text not null unique,
  display_name text not null,
  source_type text not null check (source_type in ('api','webhook','manual','import','other')),
  notes text,
  created_at timestamptz not null default now(),
  updated_at timestamptz not null default now()
);

create table if not exists tasks.task_candidates (
  candidate_id uuid primary key default gen_random_uuid(),
  source_system_id uuid references tasks.source_systems(source_system_id),
  source_event_id text,
  source_conversation_id text,
  proposed_title text not null,
  proposed_description text,
  proposed_due_at timestamptz,
  proposed_priority text not null default 'normal' check (proposed_priority in ('low','normal','high','urgent')),
  proposed_tags text[] not null default '{}',
  confidence numeric(4,3),
  evidence jsonb not null default '{}'::jsonb,
  review_status text not null default 'new' check (review_status in ('new','needs_review','approved','rejected','edited','ignored','deleted')),
  reviewer_notes text,
  reviewed_by text,
  reviewed_at timestamptz,
  created_at timestamptz not null default now(),
  updated_at timestamptz not null default now(),
  unique(source_system_id, source_event_id, proposed_title)
);

create table if not exists tasks.task_items (
  task_id uuid primary key default gen_random_uuid(),
  candidate_id uuid references tasks.task_candidates(candidate_id),
  source_system_id uuid references tasks.source_systems(source_system_id),
  title text not null,
  description text,
  status text not null default 'open' check (status in ('open','in_progress','blocked','waiting','done','cancelled','trashed')),
  priority text not null default 'normal' check (priority in ('low','normal','high','urgent')),
  due_at timestamptz,
  tags text[] not null default '{}',
  created_by text not null default 'system',
  assigned_to text,
  external_ref text,
  trash_reason text,
  trashed_at timestamptz,
  restored_at timestamptz,
  created_at timestamptz not null default now(),
  updated_at timestamptz not null default now()
);

create table if not exists tasks.tag_registry (
  tag text primary key,
  normalized_tag text generated always as (lower(tag)) stored unique,
  active boolean not null default true,
  created_by text,
  created_at timestamptz not null default now()
);

create table if not exists tasks.audit_log (
  audit_id uuid primary key default gen_random_uuid(),
  occurred_at timestamptz not null default now(),
  actor text not null default 'system',
  action text not null,
  target_type text not null,
  target_id uuid,
  before_state jsonb,
  after_state jsonb,
  reason text,
  meta jsonb
);

create index if not exists task_candidates_review_idx on tasks.task_candidates(review_status, created_at desc);
create index if not exists task_candidates_source_idx on tasks.task_candidates(source_system_id, source_event_id);
create index if not exists task_items_status_idx on tasks.task_items(status, due_at nulls last, priority, created_at desc);
create index if not exists task_items_due_idx on tasks.task_items(due_at) where status <> 'trashed';
create index if not exists task_items_tags_idx on tasks.task_items using gin(tags);
create index if not exists audit_log_target_idx on tasks.audit_log(target_type, target_id, occurred_at desc);

insert into tasks.source_systems(source_key, display_name, source_type, notes)
values
  ('omi', 'Omi conversations and memories', 'webhook', 'Omi-derived task evidence from webhook, transcript, or memory extraction workflows.'),
  ('manual', 'Manual task entry', 'manual', 'Tasks created directly in the review UI.'),
  ('import', 'Generic import', 'import', 'CSV, JSON, or workflow-generated task candidate imports.')
on conflict (source_key) do update set
  display_name = excluded.display_name,
  source_type = excluded.source_type,
  notes = excluded.notes,
  updated_at = now();

create or replace function tasks.touch_updated_at()
returns trigger language plpgsql as $$
begin
  new.updated_at = now();
  return new;
end;
$$;

do $$
begin
  if not exists (select 1 from pg_trigger where tgname = 'task_candidates_touch_updated_at') then
    create trigger task_candidates_touch_updated_at before update on tasks.task_candidates
    for each row execute function tasks.touch_updated_at();
  end if;
  if not exists (select 1 from pg_trigger where tgname = 'task_items_touch_updated_at') then
    create trigger task_items_touch_updated_at before update on tasks.task_items
    for each row execute function tasks.touch_updated_at();
  end if;
end $$;
