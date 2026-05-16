# OMI-Tasks-Supabase install test

This file records public-safe release-gate evidence for the installer smoke test.

- Test environment: disposable clean Linux VM
- Source checkout: GitHub repository HEAD
- Branch: `main`
- Test command: `./scripts/install_smoke_test.sh`
- Latest recorded result: PASS

## Scope

The release-gate validation clones a fresh checkout, runs static package validation, installs Postgres plus the Tasks Console web UI and optional n8n container, exercises the authenticated pages and candidate approval workflow, then uninstalls the stack and verifies cleanup.

The test uses synthetic task data only. It does not require or store real Omi conversations, personal tasks, API keys, or private environment details.

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
Created website/taskReviewUi/.env
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

Overall result: PASS
```
