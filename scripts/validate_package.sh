#!/usr/bin/env bash
set -euo pipefail
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"

required=(
  README.md
  LICENSE
  install.sh
  scripts/install_smoke_test.sh
  scripts/validate_package.sh
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

bash -n "$ROOT/install.sh" "$ROOT/scripts/validate_package.sh" "$ROOT/scripts/install_smoke_test.sh"
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
for forbidden in ['OMI_API_KEY=']:
    assert forbidden not in readme, f'forbidden private/secrets wording found in README: {forbidden}'

forbidden_literals = []
forbidden_patterns = [
    re.compile(r'github_pat_[A-Za-z0-9_]+'),
    re.compile(r'gh[pousr]_[A-Za-z0-9_]+'),
    re.compile(r'sk-[A-Za-z0-9]{20,}'),
    re.compile(r'\b(?:10\.\d{1,3}|192\.168|172\.(?:1[6-9]|2\d|3[0-1]))\.\d{1,3}\.\d{1,3}\b'),
]
skip_dirs = {'.git', '__pycache__', 'node_modules', '.next', 'dist', 'build'}
text_suffixes = {
    '.md', '.txt', '.py', '.sh', '.sql', '.yml', '.yaml', '.json', '.toml', '.ini',
    '.env', '.example', '.dockerignore', '.gitignore', '.license', ''
}
violations = []
for path in root.rglob('*'):
    rel_parts = path.relative_to(root).parts
    if any(part in skip_dirs for part in rel_parts) or not path.is_file():
        continue
    suffixes = {s.lower() for s in path.suffixes}
    if path.name.endswith('.env.example') or path.suffix.lower() in text_suffixes or suffixes & text_suffixes:
        try:
            text = path.read_text(errors='ignore')
        except UnicodeDecodeError:
            continue
        for term in forbidden_literals:
            if term in text:
                violations.append(f'{path.relative_to(root)}: {term}')
        for pattern in forbidden_patterns:
            if pattern.search(text):
                violations.append(f'{path.relative_to(root)}: {pattern.pattern}')
assert not violations, 'forbidden secret/private-environment references found:\n' + '\n'.join(violations)
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
