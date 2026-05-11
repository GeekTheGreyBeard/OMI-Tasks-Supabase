# OMI-Tasks-Supabase install test

- Test host: greydesk
- Test started: 2026-05-11T16:05:04Z
- Repository working tree: `/run/media/gtgb/GTGB-Files/Projects/personal/OMI-Tasks-Supabase`
- Source commit at test start: `5216fee` (`Remove private branding from OMI task package`)
- Test workspace: `/tmp/omi-tasks-supabase-smoke-20260511T160504Z-240348/OMI-Tasks-Supabase`
- Test command: `SMOKE_LOG_FILE=/tmp/omi-smoke-final2.md ./scripts/install_smoke_test.sh`

## Scope

No Proxmox VM release-gate script exists in this repository, so the strongest practical validation available from this host was a fresh temporary working-tree copy using local Docker Compose. The smoke test removed generated UI env from the copy, ran static package validation, installed Postgres + web UI + n8n, exercised routes and candidate workflow, then uninstalled and verified cleanup.

## Static validation

```text
static_content_ok
compose_config_ok
schema_apply_skipped
package_validation_ok
- PASS: static package validation
```

## Install

```text
Created .../website/taskReviewUi/.env
Waiting for Postgres...
Applying database schema...
CREATE EXTENSION
CREATE SCHEMA
CREATE TABLE
CREATE TABLE
CREATE TABLE
CREATE TABLE
CREATE TABLE
CREATE INDEX
CREATE INDEX
CREATE INDEX
CREATE INDEX
CREATE INDEX
CREATE INDEX
INSERT 0 3
CREATE FUNCTION
DO
Image omi-tasks-supabase-omi-tasks-supabase-web Built
omi-tasks-supabase-web Started
omi-tasks-supabase-n8n Started
Install complete.
- PASS: installer completed
```

## Page and API checks

```text
- PASS: health returns 200
- PASS: home returns 200
- PASS: review returns 200
- PASS: task review alias returns 200
- PASS: primary tasks returns 200
- PASS: new task returns 200
- PASS: submissions returns 200
- PASS: trash returns 200
- PASS: status returns 200
- PASS: n8n route reachable
- PASS: candidate API ingest returned candidate_id
- PASS: candidate appears in review queue
- PASS: candidate approval form submits
- PASS: approved task appears in primary task list
```

## Uninstall

```text
Uninstall complete. Only repository files should remain.
- PASS: uninstall completed
- PASS: no project containers remain
- PASS: no project volumes remain
- PASS: generated env removed
```

## Result

```text
- Passed checks: 20
- Failed checks: 0
- Test completed: 2026-05-11T16:05:13Z

**Overall result: PASS**
```
