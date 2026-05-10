#!/usr/bin/env bash
set -euo pipefail
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"

required=(
  README.md
  LICENSE
  install.sh
  supabase/sql/001_omi_tasks_supabase_setup.sql
  website/docker-compose.test-postgres.yml
  website/docker-compose.website.yml
  website/taskReviewUi/app.py
  website/taskReviewUi/Dockerfile
  website/taskReviewUi/requirements.txt
  website/taskReviewUi/.env.example
  docs/importGuide.md
  docs/testing.md
  docs/visualDocumentation.md
  docs/assets/screenshots/task-review-queue.png
  docs/assets/screenshots/primary-tasks.png
)

for rel in "${required[@]}"; do
  [[ -f "$ROOT/$rel" ]] || { echo "missing_required_file $rel" >&2; exit 1; }
done

PYTHONDONTWRITEBYTECODE=1 python3 -m py_compile "$ROOT/website/taskReviewUi/app.py"
rm -rf "$ROOT/website/taskReviewUi/__pycache__"

python3 - <<PY
import pathlib, re
root = pathlib.Path('$ROOT')
readme = (root / 'README.md').read_text()
sql = (root / 'supabase/sql/001_omi_tasks_supabase_setup.sql').read_text()
assert 'OMI-Tasks-Supabase' in readme
assert 'create schema if not exists tasks' in sql.lower()
assert 'tasks.task_candidates' in sql
assert 'tasks.task_items' in sql
for forbidden in ['OMI_API_KEY=', 'Rodney_Voice', 'vault.splat-i.io']:
    assert forbidden not in readme, f'forbidden private/secrets wording found: {forbidden}'
print('static_content_ok')
PY

if command -v docker >/dev/null 2>&1 && docker compose version >/dev/null 2>&1; then
  docker compose -f "$ROOT/website/docker-compose.test-postgres.yml" config >/dev/null
  tmp_env_created=false
  if [[ ! -f "$ROOT/website/taskReviewUi/.env" ]]; then
    cp "$ROOT/website/taskReviewUi/.env.example" "$ROOT/website/taskReviewUi/.env"
    tmp_env_created=true
  fi
  docker compose -f "$ROOT/website/docker-compose.website.yml" config >/dev/null
  if [[ "$tmp_env_created" == "true" ]]; then
    rm -f "$ROOT/website/taskReviewUi/.env"
  fi
  docker compose -f "$ROOT/website/docker-compose.n8n.yml" config >/dev/null
  echo 'compose_config_ok'
else
  echo 'compose_config_skipped'
fi

if command -v psql >/dev/null 2>&1 && [[ -n "${DATABASE_URL:-}" ]]; then
  psql "$DATABASE_URL" -v ON_ERROR_STOP=1 -f "$ROOT/supabase/sql/001_omi_tasks_supabase_setup.sql"
  echo 'schema_apply_ok'
else
  echo 'schema_apply_skipped'
fi

echo 'package_validation_ok'
