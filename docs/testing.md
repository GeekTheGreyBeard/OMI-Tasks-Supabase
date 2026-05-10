# Testing

## Static package validation

Run:

```bash
./scripts/validate_package.sh
```

This checks:

- FastAPI app Python syntax
- expected project files
- SQL schema file presence
- Docker Compose file parse, when Docker Compose is available
- optional schema application when `DATABASE_URL` and `psql` are available

## Local install smoke test

```bash
./install.sh install --non-interactive
./install.sh status
```

Then open:

```text
http://localhost:8098/review
```

The generated password is in `website/taskReviewUi/.env`.

## Seed a candidate manually

With the local installer database running:

```bash
docker exec -i omi-tasks-supabase-test-db psql -U postgres -d postgres <<'SQL'
insert into tasks.task_candidates (
  source_system_id,
  source_event_id,
  proposed_title,
  proposed_description,
  proposed_priority,
  proposed_tags,
  confidence,
  evidence
)
select source_system_id,
       'demo-001',
       'Review the demo task candidate',
       'This row verifies the review queue can approve a candidate into a task.',
       'normal',
       array['demo','review'],
       0.900,
       '{"snippet":"Please review this demo task."}'::jsonb
from tasks.source_systems
where source_key='omi';
SQL
```

Refresh `/review`, approve the candidate, then check `/tasks`, `/status`, and `/trash`.

## Cleanup

```bash
./install.sh uninstall --yes
```
