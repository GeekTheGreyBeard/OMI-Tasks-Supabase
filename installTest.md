# OMI-Tasks-Supabase install test

- Test host: Proxmox VM `9903` / `omi-releasegate-vm-20260511-1114`
- Test VM IP: `10.0.250.91`
- Proxmox node: `pm3`
- Source template: `9501` / `Ubuntu-resolute-NFS`
- Test started: 2026-05-11T17:41:00Z
- Test completed: 2026-05-11T17:44:17Z
- Repository: https://github.com/GeekTheGreyBeard/OMI-Tasks-Supabase.git
- Branch: `main`
- Source checkout: GitHub HEAD cloned inside the test VM
- Source commit: `c1f3b6f94811c94d09df65754f23b775b8e1e756`
- Test command: `./scripts/install_smoke_test.sh`

## Scope

Fresh release-gate validation was run in a disposable full Proxmox VM, not on greydesk. The test cloned GitHub HEAD inside the VM, ran static package validation, installed Postgres + Tasks Console web UI + n8n, exercised routes and the candidate approval workflow, then uninstalled and verified cleanup.

The repository is private, so the VM clone used a GitHub token retrieved point-of-use through the PatriciAI Vaultwarden wrapper. The token was not printed into logs or stored in the repository.

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
Created /tmp/omi-tasks-supabase-smoke-20260511T174059Z-2274/OMI-Tasks-Supabase/website/taskReviewUi/.env
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
- Test completed: 2026-05-11T17:44:17Z

**Overall result: PASS**
```
