# Import guide

OMI-Tasks-Supabase expects task extraction systems to write proposed work into `tasks.task_candidates`. The review UI is the human gate between raw Omi evidence and canonical tasks.

## Minimal candidate insert

```sql
insert into tasks.task_candidates (
  source_system_id,
  source_event_id,
  source_conversation_id,
  proposed_title,
  proposed_description,
  proposed_priority,
  proposed_tags,
  confidence,
  evidence
)
select
  source_system_id,
  $1,
  $2,
  $3,
  $4,
  coalesce($5, 'normal'),
  coalesce($6, '{}'::text[]),
  $7,
  coalesce($8, '{}'::jsonb)
from tasks.source_systems
where source_key = 'omi';
```

## Recommended fields

- `source_event_id`: stable idempotency key from a webhook/event/memory.
- `source_conversation_id`: source conversation or transcript id, if available.
- `proposed_title`: short action title.
- `proposed_description`: supporting detail, ideally concise.
- `proposed_due_at`: inferred due date only when evidence is strong.
- `proposed_priority`: one of `low`, `normal`, `high`, `urgent`.
- `proposed_tags`: small list of routing tags.
- `confidence`: extraction confidence from `0.000` to `1.000`.
- `evidence`: JSON object containing snippets, timestamps, and source metadata.

## Review states

Candidates start as `new` or `needs_review`. The UI can move them to:

- `approved`
- `rejected`
- `edited`
- `ignored`

Approved candidates create rows in `tasks.task_items`.

## Privacy guidance

Store the smallest evidence payload that is useful for review. Avoid retaining raw transcripts in the task candidate table if a short snippet or source reference is enough.
