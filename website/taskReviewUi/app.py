import html
import json
import os
import secrets
from typing import Any, Optional
from uuid import UUID

import psycopg
from fastapi import Depends, FastAPI, Form, HTTPException, Request
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from pydantic import BaseModel, Field

DATABASE_URL = os.environ["DATABASE_URL"]
UI_USER = os.environ.get("TASK_UI_USER", "admin")
UI_PASSWORD = os.environ["TASK_UI_PASSWORD"]
APP_TITLE = os.environ.get("APP_TITLE", "OMI Tasks Supabase")

PRIORITIES = ["low", "normal", "high", "urgent"]
TASK_STATUSES = ["open", "in_progress", "blocked", "waiting", "done", "cancelled"]
CANDIDATE_STATUSES = ["new", "needs_review", "edited", "approved", "rejected", "ignored"]
PAGE_SIZE = 50

app = FastAPI(title=APP_TITLE)
security = HTTPBasic()


class CandidateIngest(BaseModel):
    source_key: str = Field(default="omi", max_length=64)
    source_event_id: Optional[str] = Field(default=None, max_length=256)
    source_conversation_id: Optional[str] = Field(default=None, max_length=256)
    proposed_title: str = Field(min_length=1, max_length=500)
    proposed_description: Optional[str] = None
    proposed_due_at: Optional[str] = None
    proposed_priority: str = Field(default="normal")
    proposed_tags: list[str] = Field(default_factory=list)
    confidence: Optional[float] = None
    evidence: dict[str, Any] = Field(default_factory=dict)


def auth(creds: HTTPBasicCredentials = Depends(security)):
    ok_user = secrets.compare_digest(creds.username, UI_USER)
    ok_pass = secrets.compare_digest(creds.password, UI_PASSWORD)
    if not (ok_user and ok_pass):
        raise HTTPException(status_code=401, detail="Authentication required", headers={"WWW-Authenticate": "Basic"})
    return creds.username


def q(sql, params=None):
    with psycopg.connect(DATABASE_URL) as conn:
        with conn.cursor(row_factory=psycopg.rows.dict_row) as cur:
            cur.execute(sql, params or {})
            return cur.fetchall()


def one(sql, params=None):
    rows = q(sql, params)
    return rows[0] if rows else None


def exec_sql(sql, params=None):
    with psycopg.connect(DATABASE_URL) as conn:
        with conn.cursor(row_factory=psycopg.rows.dict_row) as cur:
            cur.execute(sql, params or {})
            try:
                row = cur.fetchone()
            except psycopg.ProgrammingError:
                row = None
            conn.commit()
            return row


def esc(v):
    return html.escape("" if v is None else str(v))


def selected(value, current):
    return " selected" if (value or "") == (current or "") else ""


def options(values, current):
    return "".join(f"<option value='{esc(v)}'{selected(v, current)}>{esc(v)}</option>" for v in values)


def clean_tag(tag):
    return " ".join((tag or "").strip().split())[:64]


def parse_tags(tags: Optional[str]):
    out = []
    seen = set()
    for raw in (tags or "").split(","):
        tag = clean_tag(raw)
        if tag and tag.lower() not in seen:
            out.append(tag)
            seen.add(tag.lower())
    if len(out) > 32:
        raise HTTPException(400, "A maximum of 32 tags may be attached to one task")
    return out


def register_tags(tags, actor):
    for tag in tags or []:
        exec_sql(
            "insert into tasks.tag_registry(tag, created_by) values (%s,%s) on conflict (normalized_tag) do nothing",
            (tag, actor),
        )


def tag_text(tags):
    return ", ".join(tags or [])


def audit(actor, action, target_type, target_id=None, after=None, reason=None):
    exec_sql(
        """
        insert into tasks.audit_log(actor, action, target_type, target_id, after_state, reason)
        values (%s,%s,%s,%s,%s::jsonb,%s)
        """,
        (actor, action, target_type, str(target_id) if target_id else None, None if after is None else json.dumps(after), reason),
    )


def source_id(source_key="manual"):
    row = one("select source_system_id from tasks.source_systems where source_key=%s", (source_key,))
    if not row:
        raise HTTPException(500, f"source system {source_key} is missing; apply schema first")
    return row["source_system_id"]


@app.post("/api/candidates")
@app.post("/tasks/api/candidates")
def api_create_candidate(payload: CandidateIngest, user: str = Depends(auth)):
    priority = payload.proposed_priority or "normal"
    if priority not in PRIORITIES:
        raise HTTPException(400, f"priority must be one of: {', '.join(PRIORITIES)}")
    tags = [clean_tag(t) for t in payload.proposed_tags if clean_tag(t)]
    if len(tags) > 32:
        raise HTTPException(400, "A maximum of 32 tags may be attached to one task candidate")
    sid = source_id(payload.source_key or "omi")
    row = exec_sql(
        """
        insert into tasks.task_candidates(
          source_system_id, source_event_id, source_conversation_id,
          proposed_title, proposed_description, proposed_due_at,
          proposed_priority, proposed_tags, confidence, evidence
        ) values (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s::jsonb)
        on conflict (source_system_id, source_event_id, proposed_title)
        do update set
          proposed_description = excluded.proposed_description,
          proposed_due_at = excluded.proposed_due_at,
          proposed_priority = excluded.proposed_priority,
          proposed_tags = excluded.proposed_tags,
          confidence = excluded.confidence,
          evidence = excluded.evidence,
          review_status = 'needs_review',
          updated_at = now()
        returning candidate_id, review_status
        """,
        (
            sid,
            payload.source_event_id,
            payload.source_conversation_id,
            payload.proposed_title.strip(),
            payload.proposed_description,
            payload.proposed_due_at or None,
            priority,
            tags,
            payload.confidence,
            json.dumps(payload.evidence or {}),
        ),
    )
    audit(user, "api_candidate_ingest", "task_candidate", row["candidate_id"], after={"title": payload.proposed_title, "source_key": payload.source_key})
    return {"ok": True, "candidate_id": str(row["candidate_id"]), "review_status": row["review_status"]}


def layout(title, body, user):
    nav = """
    <nav>
      <a href='/tasks/review'>Review</a>
      <a href='/tasks/primary'>Tasks</a>
      <a href='/tasks/new'>New task</a>
      <a href='/tasks/submissions'>Submissions</a>
      <a href='/tasks/trash'>Trash</a>
      <a href='/tasks/status'>Status</a>
    </nav>
    """
    return HTMLResponse(f"""<!doctype html>
<html><head><meta charset='utf-8'><meta name='viewport' content='width=device-width, initial-scale=1'>
<title>{esc(title)} · {esc(APP_TITLE)}</title>
<style>
:root {{ color-scheme: light dark; --border:#9995; --muted:#777; --card:#7771; }}
body {{ font-family: system-ui, -apple-system, Segoe UI, sans-serif; max-width: 1180px; margin: 32px auto; padding: 0 18px; line-height: 1.45; }}
a {{ color: inherit; }} nav {{ display:flex; flex-wrap:wrap; gap: 10px; margin: 0 0 24px; }}
nav a, button, .button {{ border:1px solid var(--border); border-radius:10px; padding:8px 12px; background:var(--card); text-decoration:none; cursor:pointer; }}
.card {{ border:1px solid var(--border); border-radius:14px; padding:16px; margin:14px 0; background:var(--card); }}
.grid {{ display:grid; grid-template-columns: repeat(auto-fit, minmax(220px, 1fr)); gap:12px; }}
input, textarea, select {{ width:100%; box-sizing:border-box; padding:8px; border:1px solid var(--border); border-radius:8px; background:transparent; color:inherit; }}
textarea {{ min-height: 110px; }} .row {{ display:flex; gap:8px; flex-wrap:wrap; align-items:center; }}
.muted {{ color:var(--muted); }} .pill {{ display:inline-block; border:1px solid var(--border); border-radius:999px; padding:2px 8px; margin:2px; font-size:.9em; }}
.danger {{ border-color:#b44; }} table {{ width:100%; border-collapse: collapse; }} td,th {{ border-bottom:1px solid var(--border); padding:8px; text-align:left; vertical-align:top; }}
</style></head><body>
<header><h1>{esc(title)}</h1><p class='muted'>{esc(APP_TITLE)} · signed in as {esc(user)}</p>{nav}</header>
{body}
</body></html>""")


def task_form(action, item=None, candidate=None, submit_label="Save"):
    item = item or {}
    candidate = candidate or {}
    title = item.get("title") or candidate.get("proposed_title") or ""
    description = item.get("description") or candidate.get("proposed_description") or ""
    priority = item.get("priority") or candidate.get("proposed_priority") or "normal"
    due = item.get("due_at") or candidate.get("proposed_due_at") or ""
    due_value = str(due).replace("+00:00", "")[:16] if due else ""
    tags = tag_text(item.get("tags") or candidate.get("proposed_tags") or [])
    status = item.get("status") or "open"
    status_block = "" if candidate else f"""<label>Status<select name='status'>{options(TASK_STATUSES, status)}</select></label>"""
    return f"""
    <form method='post' action='{esc(action)}' class='card'>
      <div class='grid'>
        <label>Title<input name='title' required maxlength='240' value='{esc(title)}'></label>
        <label>Priority<select name='priority'>{options(PRIORITIES, priority)}</select></label>
        <label>Due date/time<input type='datetime-local' name='due_at' value='{esc(due_value)}'></label>
        {status_block}
      </div>
      <label>Description<textarea name='description'>{esc(description)}</textarea></label>
      <label>Tags <span class='muted'>(comma-separated)</span><input name='tags' value='{esc(tags)}'></label>
      <label>Notes / reason<textarea name='notes' placeholder='Optional review note, trash reason, or edit context'></textarea></label>
      <p><button type='submit'>{esc(submit_label)}</button></p>
    </form>
    """


@app.get("/", response_class=HTMLResponse)
def root():
    return RedirectResponse("/tasks/review", status_code=302)


@app.get("/health")
def health():
    return {"ok": True, "service": "omi-tasks-supabase"}


@app.get("/review", response_class=HTMLResponse)
@app.get("/tasks/review", response_class=HTMLResponse)
def review(user: str = Depends(auth), status: str = "new"):
    allowed = CANDIDATE_STATUSES if status != "all" else CANDIDATE_STATUSES
    where = "review_status = %s" if status != "all" else "review_status in ('new','needs_review','edited')"
    rows = q(f"select * from tasks.task_candidates where {where} order by created_at desc limit %s", ((status, PAGE_SIZE) if status != "all" else (PAGE_SIZE,)))
    filters = " ".join(f"<a class='button' href='/tasks/review?status={s}'>{s}</a>" for s in ["all"] + allowed)
    cards = [f"<p class='muted'>No task candidates found for this view.</p>"] if not rows else []
    for r in rows:
        tags = "".join(f"<span class='pill'>{esc(t)}</span>" for t in (r.get("proposed_tags") or []))
        evidence = esc(r.get("evidence") or {})
        cards.append(f"""
        <section class='card'>
          <h2>{esc(r['proposed_title'])}</h2>
          <p>{esc(r.get('proposed_description'))}</p>
          <p class='muted'>priority: {esc(r.get('proposed_priority'))} · due: {esc(r.get('proposed_due_at'))} · confidence: {esc(r.get('confidence'))}</p>
          <p>{tags}</p>
          <details><summary>Evidence</summary><pre>{evidence}</pre></details>
          {task_form('/tasks/candidates/' + str(r['candidate_id']) + '/approve', candidate=r, submit_label='Approve as task')}
          <form method='post' action='/tasks/candidates/{esc(r['candidate_id'])}/reject' class='row'>
            <input name='reason' placeholder='Rejection reason' style='max-width:420px'>
            <button class='danger'>Reject</button>
          </form>
        </section>
        """)
    return layout("Task candidate review", f"<div class='row'>{filters}</div>{''.join(cards)}", user)


@app.post("/candidates/{candidate_id}/approve")
@app.post("/tasks/candidates/{candidate_id}/approve")
def approve_candidate(candidate_id: UUID, user: str = Depends(auth), title: str = Form(...), description: str = Form(""), priority: str = Form("normal"), due_at: str = Form(""), tags: str = Form(""), notes: str = Form("")):
    candidate = one("select * from tasks.task_candidates where candidate_id=%s", (str(candidate_id),))
    if not candidate:
        raise HTTPException(404, "candidate not found")
    clean_tags = parse_tags(tags)
    register_tags(clean_tags, user)
    row = exec_sql(
        """
        insert into tasks.task_items(candidate_id, source_system_id, title, description, priority, due_at, tags, created_by)
        values (%s,%s,%s,%s,%s,nullif(%s,'')::timestamptz,%s,%s)
        returning task_id
        """,
        (str(candidate_id), candidate.get("source_system_id"), title.strip(), description.strip() or None, priority, due_at, clean_tags, user),
    )
    exec_sql("update tasks.task_candidates set review_status='approved', reviewer_notes=%s, reviewed_by=%s, reviewed_at=now() where candidate_id=%s", (notes or None, user, str(candidate_id)))
    audit(user, "approve_candidate", "task_candidate", candidate_id, {"task_id": str(row["task_id"])}, notes or None)
    return RedirectResponse("/tasks/primary", status_code=303)


@app.post("/candidates/{candidate_id}/reject")
@app.post("/tasks/candidates/{candidate_id}/reject")
def reject_candidate(candidate_id: UUID, user: str = Depends(auth), reason: str = Form("")):
    exec_sql("update tasks.task_candidates set review_status='rejected', reviewer_notes=%s, reviewed_by=%s, reviewed_at=now() where candidate_id=%s", (reason or None, user, str(candidate_id)))
    audit(user, "reject_candidate", "task_candidate", candidate_id, reason=reason or None)
    return RedirectResponse("/tasks/review", status_code=303)


@app.get("/tasks", response_class=HTMLResponse)
def tasks(user: str = Depends(auth), status: str = "active"):
    if status == "active":
        rows = q("select * from tasks.task_items where status <> 'trashed' order by due_at nulls last, created_at desc limit %s", (PAGE_SIZE,))
    else:
        rows = q("select * from tasks.task_items where status=%s order by due_at nulls last, created_at desc limit %s", (status, PAGE_SIZE))
    filters = " ".join(f"<a class='button' href='/tasks/primary?status={s}'>{s}</a>" for s in ["active"] + TASK_STATUSES)
    body = [f"<div class='row'>{filters}</div>"]
    if not rows:
        body.append("<p class='muted'>No tasks found.</p>")
    for r in rows:
        tags = "".join(f"<span class='pill'>{esc(t)}</span>" for t in (r.get("tags") or []))
        body.append(f"""
        <section class='card'>
          <h2>{esc(r['title'])}</h2><p>{esc(r.get('description'))}</p>
          <p class='muted'>status: {esc(r['status'])} · priority: {esc(r['priority'])} · due: {esc(r.get('due_at'))}</p><p>{tags}</p>
          {task_form('/tasks/' + str(r['task_id']) + '/edit', item=r, submit_label='Save changes')}
          <form method='post' action='/tasks/{esc(r['task_id'])}/trash' class='row'>
            <input name='reason' placeholder='Trash reason' style='max-width:420px'>
            <button class='danger'>Move to trash</button>
          </form>
        </section>
        """)
    return layout("Tasks", "".join(body), user)


@app.get("/tasks/primary", response_class=HTMLResponse)
def tasks_primary_compat(user: str = Depends(auth), status: str = "active"):
    return tasks(user, status)


@app.post("/tasks/{task_id}/edit")
def edit_task(task_id: UUID, user: str = Depends(auth), title: str = Form(...), description: str = Form(""), status: str = Form("open"), priority: str = Form("normal"), due_at: str = Form(""), tags: str = Form(""), notes: str = Form("")):
    clean_tags = parse_tags(tags)
    register_tags(clean_tags, user)
    exec_sql(
        """
        update tasks.task_items
        set title=%s, description=%s, status=%s, priority=%s, due_at=nullif(%s,'')::timestamptz, tags=%s
        where task_id=%s
        """,
        (title.strip(), description.strip() or None, status, priority, due_at, clean_tags, str(task_id)),
    )
    audit(user, "edit_task", "task", task_id, {"status": status, "priority": priority}, notes or None)
    return RedirectResponse("/tasks/primary", status_code=303)


@app.post("/tasks/{task_id}/trash")
def trash_task(task_id: UUID, user: str = Depends(auth), reason: str = Form("")):
    exec_sql("update tasks.task_items set status='trashed', trash_reason=%s, trashed_at=now() where task_id=%s", (reason or None, str(task_id)))
    audit(user, "trash_task", "task", task_id, reason=reason or None)
    return RedirectResponse("/tasks/primary", status_code=303)


@app.get("/trash", response_class=HTMLResponse)
@app.get("/tasks/trash", response_class=HTMLResponse)
def trash(user: str = Depends(auth)):
    rows = q("select * from tasks.task_items where status='trashed' order by trashed_at desc nulls last limit %s", (PAGE_SIZE,))
    if not rows:
        return layout("Trash", "<p class='muted'>Trash is empty.</p>", user)
    cards = []
    for r in rows:
        cards.append(f"""
        <section class='card'>
          <h2>{esc(r['title'])}</h2><p>{esc(r.get('description'))}</p>
          <p class='muted'>trashed: {esc(r.get('trashed_at'))} · reason: {esc(r.get('trash_reason'))}</p>
          <form method='post' action='/tasks/{esc(r['task_id'])}/restore'><button>Restore</button></form>
        </section>
        """)
    return layout("Trash", "".join(cards), user)


@app.post("/tasks/{task_id}/restore")
def restore_task(task_id: UUID, user: str = Depends(auth)):
    exec_sql("update tasks.task_items set status='open', restored_at=now(), trash_reason=null where task_id=%s", (str(task_id),))
    audit(user, "restore_task", "task", task_id)
    return RedirectResponse("/tasks/trash", status_code=303)


@app.get("/new", response_class=HTMLResponse)
def new_task(user: str = Depends(auth)):
    return layout("Create scratch task", task_form("/tasks/new", submit_label="Create task"), user)


@app.get("/tasks/new", response_class=HTMLResponse)
def new_task_compat(user: str = Depends(auth)):
    return new_task(user)


@app.post("/new")
def create_task(user: str = Depends(auth), title: str = Form(...), description: str = Form(""), priority: str = Form("normal"), due_at: str = Form(""), tags: str = Form(""), notes: str = Form("")):
    clean_tags = parse_tags(tags)
    register_tags(clean_tags, user)
    row = exec_sql(
        """
        insert into tasks.task_items(source_system_id, title, description, priority, due_at, tags, created_by)
        values (%s,%s,%s,%s,nullif(%s,'')::timestamptz,%s,%s)
        returning task_id
        """,
        (source_id("manual"), title.strip(), description.strip() or None, priority, due_at, clean_tags, user),
    )
    audit(user, "create_scratch_task", "task", row["task_id"], reason=notes or None)
    return RedirectResponse("/tasks/primary", status_code=303)


@app.post("/tasks/new")
def create_task_compat(user: str = Depends(auth), title: str = Form(...), description: str = Form(""), priority: str = Form("normal"), due_at: str = Form(""), tags: str = Form(""), notes: str = Form("")):
    return create_task(user, title, description, priority, due_at, tags, notes)


@app.get("/submissions", response_class=HTMLResponse)
@app.get("/tasks/submissions", response_class=HTMLResponse)
def submissions(user: str = Depends(auth)):
    candidates = q("""
      select candidate_id, proposed_title, review_status, confidence, created_at
      from tasks.task_candidates
      order by created_at desc
      limit %s
    """, (PAGE_SIZE,))
    audit_rows = q("""
      select occurred_at, actor, action, target_type, target_id, reason
      from tasks.audit_log
      order by occurred_at desc
      limit %s
    """, (PAGE_SIZE,))
    cand_rows = "".join(
        f"<tr><td>{esc(r['created_at'])}</td><td>{esc(r['review_status'])}</td><td>{esc(r['proposed_title'])}</td><td>{esc(r.get('confidence'))}</td></tr>"
        for r in candidates
    ) or "<tr><td colspan='4' class='muted'>No task candidate submissions yet.</td></tr>"
    audit_table = "".join(
        f"<tr><td>{esc(r['occurred_at'])}</td><td>{esc(r['action'])}</td><td>{esc(r['target_type'])}</td><td>{esc(r.get('reason'))}</td></tr>"
        for r in audit_rows
    ) or "<tr><td colspan='4' class='muted'>No audit events yet.</td></tr>"
    body = f"""
    <section class='card'><h2>Candidate submissions</h2><p class='muted'>Newest task candidates from Omi/workflow/manual import sources.</p>
    <table><tr><th>Created</th><th>Status</th><th>Title</th><th>Confidence</th></tr>{cand_rows}</table></section>
    <section class='card'><h2>Recent task actions</h2><p class='muted'>Audit trail for review, edit, status, trash, restore, and scratch-create actions.</p>
    <table><tr><th>Time</th><th>Action</th><th>Target</th><th>Reason</th></tr>{audit_table}</table></section>
    """
    return layout("Task submissions", body, user)


@app.get("/status", response_class=HTMLResponse)
@app.get("/tasks/status", response_class=HTMLResponse)
def status(user: str = Depends(auth)):
    candidate_counts = q("select review_status as status, count(*) from tasks.task_candidates group by review_status order by review_status")
    task_counts = q("select status, count(*) from tasks.task_items group by status order by status")
    def table(rows):
        return "<table><tr><th>Status</th><th>Count</th></tr>" + "".join(f"<tr><td>{esc(r['status'])}</td><td>{esc(r['count'])}</td></tr>" for r in rows) + "</table>"
    body = f"<div class='grid'><section class='card'><h2>Candidates</h2>{table(candidate_counts)}</section><section class='card'><h2>Tasks</h2>{table(task_counts)}</section></div>"
    return layout("Status", body, user)
