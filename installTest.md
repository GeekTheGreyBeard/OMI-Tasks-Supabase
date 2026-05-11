# OMI-Tasks-Supabase install test

- Test host: temporary full Proxmox VM `9903` / `omi-releasegate-vm-20260511-1114`
- VM IP: `10.0.250.91`
- Test started: 2026-05-11T17:30:27Z
- Test completed: 2026-05-11T17:35:17Z
- Repository working tree: `~/releasegate/OMI-Tasks-Supabase` inside the VM
- Source commit at test start: `b2e4b9096228a0ca1581f6451822835636d57008`
- Test workspace: `/tmp/omi-tasks-supabase-smoke-20260511T173026Z-22863/OMI-Tasks-Supabase`
- Test command: `SMOKE_LOG_FILE=~/releasegate/logs/omi-tasks-supabase-installTest-rerun.md ./scripts/install_smoke_test.sh`

## Scope

Release-gate retest was run inside a dedicated temporary full QEMU VM in the Proxmox cluster. Greydesk only orchestrated over SSH. The smoke test ran the committed static package validation, installed Postgres + web UI + n8n with Docker Compose, exercised the web/API workflow, then uninstalled and verified cleanup.

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
- Test completed: 2026-05-11T17:35:17Z

**Overall result: PASS**
```
