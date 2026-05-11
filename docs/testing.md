# Testing

## Static package validation

Run:

```bash
./scripts/validate_package.sh
```

This checks:

- FastAPI app Python syntax
- shell syntax for installer/test scripts
- expected project files
- SQL schema file presence
- Docker Compose file parse, when Docker Compose is available
- optional schema application when `DATABASE_URL` and `psql` are available

## Reproducible fresh-copy smoke test

Run the release-gate smoke test from the repository root:

```bash
./scripts/install_smoke_test.sh
```

The script copies the current working tree into a temporary directory, removes any generated UI `.env`, validates the package, runs `./install.sh install --with-n8n --non-interactive`, waits for the services, checks the main authenticated routes, creates a candidate through the API, approves it through the form endpoint, verifies the approved task appears, and uninstalls the stack. It refuses to start if existing `omi-tasks-supabase` containers are present so it does not remove a running local stack unexpectedly.

To keep a Markdown log:

```bash
SMOKE_LOG_FILE=/tmp/omi-tasks-supabase-smoke.md ./scripts/install_smoke_test.sh
```

## Manual local install smoke test

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
