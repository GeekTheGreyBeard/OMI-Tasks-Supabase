#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
PROJECT_NAME="omi-tasks-supabase"
WORKDIR="${TMPDIR:-/tmp}/${PROJECT_NAME}-smoke-$(date -u +%Y%m%dT%H%M%SZ)-$$"
LOG_FILE="${SMOKE_LOG_FILE:-}"
PASSED=0
FAILED=0
CLEANED=false

log() {
  printf '%s\n' "$*"
}

record_pass() {
  PASSED=$((PASSED + 1))
  log "- PASS: $*"
}

record_fail() {
  FAILED=$((FAILED + 1))
  log "- FAIL: $*"
}

need_cmd() {
  command -v "$1" >/dev/null 2>&1 || { log "Missing required command: $1"; exit 2; }
}

cleanup() {
  local status=$?
  if [[ -d "$WORKDIR/OMI-Tasks-Supabase" ]]; then
    (
      cd "$WORKDIR/OMI-Tasks-Supabase"
      ./install.sh uninstall --yes >/tmp/${PROJECT_NAME}-smoke-cleanup.log 2>&1 || true
    )
    CLEANED=true
  fi
  rm -rf "$WORKDIR"
  if [[ $status -ne 0 ]]; then
    log "Smoke test aborted with exit status $status"
  fi
}
trap cleanup EXIT

curl_code() {
  local url="$1"
  curl -fsS -u "$TASK_UI_USER:$TASK_UI_PASSWORD" -o /tmp/${PROJECT_NAME}-curl.out -w '%{http_code}' "$url"
}

check_route() {
  local label="$1"
  local url="$2"
  local expected="${3:-200}"
  local code
  if code="$(curl_code "$url")" && [[ "$code" == "$expected" ]]; then
    record_pass "$label returns $expected"
  else
    record_fail "$label expected $expected, got ${code:-curl_error}"
  fi
}

wait_for_url() {
  local url="$1"
  local auth_flag="${2:-auth}"
  for _ in {1..60}; do
    if [[ "$auth_flag" == "auth" ]]; then
      curl -fs -u "$TASK_UI_USER:$TASK_UI_PASSWORD" -o /dev/null "$url" && return 0
    else
      curl -fs -o /dev/null "$url" && return 0
    fi
    sleep 1
  done
  return 1
}

main() {
  need_cmd git
  need_cmd docker
  need_cmd curl
  docker compose version >/dev/null 2>&1 || { log "Docker Compose plugin is required."; exit 2; }

  if docker ps -a --filter "name=${PROJECT_NAME}" --format '{{.Names}}' | grep -q .; then
    log "Refusing to run while existing ${PROJECT_NAME} containers are present. Run ./install.sh uninstall --yes first if they are disposable."
    exit 2
  fi

  mkdir -p "$WORKDIR/OMI-Tasks-Supabase"
  tar -C "$ROOT" \
    --exclude='.git' \
    --exclude='website/taskReviewUi/.env' \
    --exclude='website/taskReviewUi/__pycache__' \
    -cf - . | tar -x -C "$WORKDIR/OMI-Tasks-Supabase"
  cd "$WORKDIR/OMI-Tasks-Supabase"
  rm -f website/taskReviewUi/.env

  log "# OMI-Tasks-Supabase smoke test"
  log ""
  log "- Test started: $(date -u +%Y-%m-%dT%H:%M:%SZ)"
  log "- Source commit: $(git -C "$ROOT" rev-parse --short HEAD 2>/dev/null || echo unknown)"
  log "- Test workspace: $WORKDIR/OMI-Tasks-Supabase"
  log ""

  log "## Static validation"
  if ./scripts/validate_package.sh; then
    record_pass "static package validation"
  else
    record_fail "static package validation"
  fi
  log ""

  log "## Install"
  if ./install.sh install --with-n8n --non-interactive; then
    record_pass "installer completed"
  else
    record_fail "installer completed"
  fi
  TASK_UI_USER=$(awk -F= '$1 == "TASK_UI_USER" {print substr($0, index($0, "=") + 1)}' website/taskReviewUi/.env)
  TASK_UI_PASSWORD=$(awk -F= '$1 == "TASK_UI_PASSWORD" {print substr($0, index($0, "=") + 1)}' website/taskReviewUi/.env)
  export TASK_UI_USER TASK_UI_PASSWORD
  wait_for_url "http://localhost:8098/health" noauth || true
  wait_for_url "http://localhost:5679/" noauth || true
  log ""

  log "## Page and API checks"
  check_route "health" "http://localhost:8098/health"
  check_route "home" "http://localhost:8098/"
  check_route "review" "http://localhost:8098/review"
  check_route "task review alias" "http://localhost:8098/tasks/review"
  check_route "primary tasks" "http://localhost:8098/tasks/primary"
  check_route "new task" "http://localhost:8098/tasks/new"
  check_route "submissions" "http://localhost:8098/tasks/submissions"
  check_route "trash" "http://localhost:8098/tasks/trash"
  check_route "status" "http://localhost:8098/tasks/status"

  if curl -fsS -o /tmp/${PROJECT_NAME}-n8n.out -w '%{http_code}' http://localhost:5679/ | grep -Eq '^(200|301|302|307|308)$'; then
    record_pass "n8n route reachable"
  else
    record_fail "n8n route reachable"
  fi

  local payload response candidate_id title
  title="Smoke test candidate $(date -u +%s)"
  payload=$(python3 - <<PY
import json
print(json.dumps({
  "source_key": "omi",
  "source_event_id": "smoke-test",
  "proposed_title": "$title",
  "proposed_description": "Created by scripts/install_smoke_test.sh",
  "proposed_priority": "normal",
  "proposed_tags": ["smoke", "release-gate"],
  "confidence": 0.99,
  "evidence": {"test": "install_smoke_test"}
}))
PY
)
  if response=$(curl -fsS -u "$TASK_UI_USER:$TASK_UI_PASSWORD" -H 'Content-Type: application/json' -d "$payload" http://localhost:8098/api/candidates); then
    candidate_id=$(python3 - <<PY
import json
print(json.loads('''$response''')["candidate_id"])
PY
)
    record_pass "candidate API ingest returned candidate_id"
  else
    candidate_id=""
    record_fail "candidate API ingest returned candidate_id"
  fi

  if [[ -n "$candidate_id" ]] && curl -fsS -u "$TASK_UI_USER:$TASK_UI_PASSWORD" http://localhost:8098/review | grep -Fq "$title"; then
    record_pass "candidate appears in review queue"
  else
    record_fail "candidate appears in review queue"
  fi

  if [[ -n "$candidate_id" ]] && curl -fsS -u "$TASK_UI_USER:$TASK_UI_PASSWORD" -X POST \
      --data-urlencode "title=$title" \
      --data-urlencode "description=Created by scripts/install_smoke_test.sh" \
      --data-urlencode "priority=normal" \
      --data-urlencode "tags=smoke, release-gate" \
      "http://localhost:8098/tasks/candidates/$candidate_id/approve" >/tmp/${PROJECT_NAME}-approve.out; then
    record_pass "candidate approval form submits"
  else
    record_fail "candidate approval form submits"
  fi

  if curl -fsS -u "$TASK_UI_USER:$TASK_UI_PASSWORD" http://localhost:8098/tasks/primary | grep -Fq "$title"; then
    record_pass "approved task appears in primary task list"
  else
    record_fail "approved task appears in primary task list"
  fi
  log ""

  log "## Uninstall"
  if ./install.sh uninstall --yes; then
    record_pass "uninstall completed"
  else
    record_fail "uninstall completed"
  fi
  if ! docker ps -a --filter "name=${PROJECT_NAME}" --format '{{.Names}}' | grep -q .; then
    record_pass "no project containers remain"
  else
    record_fail "no project containers remain"
  fi
  if ! docker volume ls -q --filter "name=${PROJECT_NAME}" | grep -q .; then
    record_pass "no project volumes remain"
  else
    record_fail "no project volumes remain"
  fi
  if [[ ! -f website/taskReviewUi/.env ]]; then
    record_pass "generated env removed"
  else
    record_fail "generated env removed"
  fi
  log ""

  log "## Result"
  log ""
  log "- Passed checks: $PASSED"
  log "- Failed checks: $FAILED"
  log "- Test completed: $(date -u +%Y-%m-%dT%H:%M:%SZ)"
  log ""
  if [[ $FAILED -eq 0 ]]; then
    log "**Overall result: PASS**"
  else
    log "**Overall result: FAIL**"
    exit 1
  fi
}

if [[ -n "$LOG_FILE" ]]; then
  main 2>&1 | tee "$LOG_FILE"
else
  main
fi
