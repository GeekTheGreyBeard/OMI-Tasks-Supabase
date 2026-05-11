import html
import json
import os
import secrets
import urllib.error
import urllib.parse
import urllib.request
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
OMI_API_BASE = os.environ.get("OMI_API_BASE", "https://api.omi.me").rstrip("/")
OMI_API_KEY = os.environ.get("OMI_API_KEY", "")
HOME_LINK_URL = os.environ.get("HOME_LINK_URL", "").strip()
HOME_LINK_TEXT = os.environ.get("HOME_LINK_TEXT", "Back to Home").strip() or "Back to Home"

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


def omi_request_action_items(limit=50, offset=0, completed="false"):
    if not OMI_API_KEY:
        raise HTTPException(500, "OMI_API_KEY is not configured for this task UI")
    params = {"limit": str(max(1, min(int(limit or 50), 100))), "offset": str(max(0, int(offset or 0)))}
    if completed in ("true", "false"):
        params["completed"] = completed
    url = f"{OMI_API_BASE}/v1/dev/user/action-items?{urllib.parse.urlencode(params)}"
    req = urllib.request.Request(url, headers={"Authorization": f"Bearer {OMI_API_KEY}", "Accept": "application/json"})
    try:
        with urllib.request.urlopen(req, timeout=30) as res:
            raw = res.read().decode("utf-8")
            data = json.loads(raw or "[]")
            if not isinstance(data, list):
                raise HTTPException(502, "Omi action-items response was not a list")
            return data
    except urllib.error.HTTPError as e:
        detail = e.read().decode("utf-8", errors="replace")[:500]
        raise HTTPException(e.code, f"Omi action-items request failed: {detail}")
    except urllib.error.URLError as e:
        raise HTTPException(502, f"Omi action-items request failed: {e.reason}")
    except TimeoutError:
        raise HTTPException(504, "Omi action-items request timed out")


def candidate_from_omi_action_item(item, user):
    description = str(item.get("description") or "").strip()
    if not description:
        return None, "missing description"
    title = description.splitlines()[0].strip()[:240]
    if len(title) < len(description):
        title = title.rstrip(" .") + "…"
    evidence = {
        "provider": "omi",
        "type": "action_item",
        "action_item_id": item.get("id"),
        "conversation_id": item.get("conversation_id"),
        "completed": item.get("completed"),
        "created_at": item.get("created_at"),
        "updated_at": item.get("updated_at"),
        "completed_at": item.get("completed_at"),
        "raw": item,
    }
    payload = CandidateIngest(
        source_key="omi",
        source_event_id=str(item.get("id") or ""),
        source_conversation_id=item.get("conversation_id"),
        proposed_title=title,
        proposed_description=description,
        proposed_due_at=item.get("due_at"),
        proposed_priority="normal",
        proposed_tags=["omi", "action-item"],
        confidence=None,
        evidence=evidence,
    )
    row = api_create_candidate(payload, user)
    return row, None


def load_omi_form(result_html=""):
    configured = "Configured" if OMI_API_KEY else "Missing OMI_API_KEY"
    return f"""
    <section class='card'>
      <h2>Load tasks from Omi</h2>
      <p class='muted'>Fetch Omi Developer API action items and stage them as task candidates for review. Nothing is promoted to the primary task list until you approve it.</p>
      <p><span class='pill'>Omi API: {esc(configured)}</span><span class='pill'>Source: action items</span><span class='pill'>Review required</span></p>
      <form method='post' action='/tasks/load-omi'>
        <div class='grid'>
          <label>Completed filter<select name='completed'><option value='false'>Open only</option><option value='true'>Completed only</option><option value='all'>All</option></select></label>
          <label>Limit<input name='limit' type='number' min='1' max='100' value='50'></label>
          <label>Offset<input name='offset' type='number' min='0' value='0'></label>
        </div>
        <p><button type='submit'>Load Omi action items</button></p>
      </form>
    </section>
    {result_html}
    """


def layout(title, body, user):
    nav = """
    <nav>
      <a href='/tasks/home'>Home</a>
      <a href='/tasks/review'>Review</a>
      <a href='/tasks/primary'>Tasks</a>
      <a href='/tasks/new'>New task</a>
      <a href='/tasks/load-omi'>Load from Omi</a>
      <a href='/tasks/submissions'>Submissions</a>
      <a href='/tasks/trash'>Trash</a>
      <a href='/tasks/status'>Status</a>
    </nav>
    """
    return HTMLResponse(f"""<!doctype html>
<html><head><meta charset='utf-8'><meta name='viewport' content='width=device-width, initial-scale=1'>
<title>{esc(title)} · {esc(APP_TITLE)}</title>
<style>
:root {{ --bg:#080b18; --panel:rgba(18,25,48,.78); --panel2:rgba(30,39,76,.72); --text:#edf3ff; --muted:#9fb0d0; --accent:#8a5cff; --accent2:#20e3b2; --danger:#ff5c8a; --warn:#ffcc66; --ok:#42f59b; --border:rgba(255,255,255,.11); --shadow:0 20px 70px rgba(0,0,0,.34), inset 0 1px rgba(255,255,255,.08); }}
* {{ box-sizing:border-box; }}
body {{ margin:0; min-height:100vh; font-family:Inter, ui-sans-serif, system-ui, -apple-system, Segoe UI, sans-serif; color:var(--text); background: radial-gradient(circle at 18% 8%, #31206a 0, transparent 29rem), radial-gradient(circle at 82% 0%, #0a6b70 0, transparent 24rem), linear-gradient(135deg,#070914,#101427 55%,#080b18); overflow-x:hidden; line-height:1.5; padding:36px 20px 72px; }}
body:before {{ content:""; position:fixed; inset:0; pointer-events:none; background-image:linear-gradient(rgba(255,255,255,.035) 1px, transparent 1px), linear-gradient(90deg, rgba(255,255,255,.025) 1px, transparent 1px); background-size:56px 56px; mask-image:linear-gradient(to bottom, rgba(0,0,0,.7), transparent 75%); }}
body > * {{ max-width:1180px; margin-left:auto; margin-right:auto; position:relative; }}
a {{ color:#9bdcff; text-decoration:none; }}
header {{ padding:28px; margin-bottom:18px; background:linear-gradient(180deg,var(--panel),rgba(10,14,32,.82)); border:1px solid var(--border); border-radius:28px; box-shadow:var(--shadow); backdrop-filter:blur(18px); }}
h1 {{ margin:0 0 10px; font-size:clamp(34px, 6vw, 68px); line-height:.9; letter-spacing:-.06em; background:linear-gradient(90deg,var(--accent2),#d6c7ff,var(--accent)); -webkit-background-clip:text; color:transparent; }}
h2 {{ margin:8px 0 10px; font-size:23px; letter-spacing:-.03em; }}
h3 {{ margin:6px 0 10px; color:#d6c7ff; }}
p {{ color:var(--muted); }}
nav {{ display:flex; flex-wrap:wrap; gap:10px; margin-top:20px; }}
nav a, button, .button, input[type='submit'] {{ border:0; border-radius:15px; padding:10px 14px; color:#07111d; background:linear-gradient(90deg,var(--accent2),#9bdcff); font-weight:800; box-shadow:0 10px 24px rgba(32,227,178,.18); text-decoration:none; cursor:pointer; }}
nav a:nth-child(n+2), .button, button.secondary {{ color:var(--text); background:rgba(255,255,255,.10); box-shadow:none; border:1px solid rgba(255,255,255,.12); }}
button.danger, .danger button, button[name='action'][value='reject'] {{ color:#fff; background:linear-gradient(90deg,var(--danger),#ff8fb0); }}
.card {{ border:1px solid var(--border); border-radius:24px; padding:18px; margin:16px 0; background:linear-gradient(180deg,var(--panel),rgba(10,14,32,.82)); box-shadow:var(--shadow); backdrop-filter:blur(18px); }}
.card:hover {{ border-color:rgba(138,92,255,.44); }}
.grid {{ display:grid; grid-template-columns:repeat(auto-fit,minmax(230px,1fr)); gap:14px; }}
.row {{ display:flex; gap:10px; flex-wrap:wrap; align-items:center; }}
input, textarea, select {{ width:100%; box-sizing:border-box; padding:10px 11px; border:1px solid rgba(255,255,255,.14); border-radius:13px; background:rgba(255,255,255,.075); color:var(--text); outline:none; }}
textarea {{ min-height:110px; }}
select option {{ background:#101427; color:var(--text); }}
label {{ display:block; color:#d7e3ff; font-weight:650; margin:10px 0; }}
.muted {{ color:var(--muted); }}
.pill {{ display:inline-flex; width:max-content; gap:8px; align-items:center; border:1px solid rgba(255,255,255,.12); border-radius:999px; padding:5px 9px; margin:2px; color:#d7e3ff; background:rgba(255,255,255,.075); font-size:.9em; }}
table {{ width:100%; border-collapse:separate; border-spacing:0; overflow:hidden; border-radius:18px; border:1px solid rgba(255,255,255,.10); background:rgba(255,255,255,.045); }}
td,th {{ border-bottom:1px solid rgba(255,255,255,.08); padding:10px; text-align:left; vertical-align:top; }}
th {{ color:#d6c7ff; background:rgba(138,92,255,.10); }}
tr:last-child td {{ border-bottom:0; }}
code {{ color:#20e3b2; }}
@media(max-width:760px){{ body{{padding:22px 12px 48px}} header{{padding:22px}} table{{display:block; overflow-x:auto}} }}
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


def task_home_body():
    candidates = one("select count(*) as c from tasks.task_candidates where review_status in ('new','needs_review','edited')") or {"c": 0}
    active = one("select count(*) as c from tasks.task_items where status not in ('done','cancelled','trashed')") or {"c": 0}
    queued = one("select count(*) as c from tasks.audit_log where action in ('api_candidate_ingest','create_task')") or {"c": 0}
    trashed = one("select count(*) as c from tasks.task_items where status='trashed'") or {"c": 0}
    home_link = f"<a class='button' href='{esc(HOME_LINK_URL)}'>{esc(HOME_LINK_TEXT)}</a>" if HOME_LINK_URL else ""
    return f"""
    <section class='card' style='padding:28px; margin-bottom:20px'>
      <div class='muted' style='text-transform:uppercase; letter-spacing:.16em; font-weight:800'>Omi Task Management</div>
      <h1 style='margin-top:8px'>Omi <span style='background:linear-gradient(90deg,var(--accent2),#d6c7ff,var(--accent)); -webkit-background-clip:text; color:transparent'>Tasks Console</span></h1>
      <p class='muted' style='font-size:18px; max-width:780px'>A focused starting point for reviewing Omi-derived task evidence, promoting real work, creating direct tasks, and auditing submissions.</p>
      <div class='row' style='margin-top:18px'>
        <a class='button' href='/tasks/review'>Review task candidates</a>
        <a class='button' href='/tasks/primary'>Primary tasks</a>
        <a class='button' href='/tasks/new'>Create task</a>
        <a class='button' href='/tasks/load-omi'>Load tasks from Omi</a>
        {home_link}
      </div>
    </section>
    <section class='grid'>
      <a class='card' href='/tasks/review'><h2>{esc(candidates['c'])}</h2><p class='muted'>Candidates needing review</p></a>
      <a class='card' href='/tasks/primary'><h2>{esc(active['c'])}</h2><p class='muted'>Active primary tasks</p></a>
      <a class='card' href='/tasks/new'><h2>+</h2><p class='muted'>Create a direct task</p></a>
      <a class='card' href='/tasks/load-omi'><h2>⇣</h2><p class='muted'>Load Omi action items</p></a>
      <a class='card' href='/tasks/submissions'><h2>{esc(queued['c'])}</h2><p class='muted'>Submission/audit events</p></a>
      <a class='card' href='/tasks/trash'><h2>{esc(trashed['c'])}</h2><p class='muted'>Trashed tasks</p></a>
    </section>
    """


@app.get("/", response_class=HTMLResponse)
@app.get("/tasks/home", response_class=HTMLResponse)
def root(user: str = Depends(auth)):
    return layout("Omi Tasks Console", task_home_body(), user)


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


@app.get("/load-omi", response_class=HTMLResponse)
@app.get("/tasks/load-omi", response_class=HTMLResponse)
def load_omi_page(user: str = Depends(auth)):
    return layout("Load tasks from Omi", load_omi_form(), user)


@app.post("/load-omi", response_class=HTMLResponse)
@app.post("/tasks/load-omi", response_class=HTMLResponse)
def load_omi_submit(user: str = Depends(auth), completed: str = Form("false"), limit: int = Form(50), offset: int = Form(0)):
    completed_param = completed if completed in ("true", "false") else "all"
    items = omi_request_action_items(limit=limit, offset=offset, completed=completed_param)
    loaded = 0
    skipped = []
    for item in items:
        row, reason = candidate_from_omi_action_item(item, user)
        if row:
            loaded += 1
        else:
            skipped.append({"id": item.get("id"), "reason": reason})
    audit(user, "load_omi_action_items", "omi_action_items", after={"requested": len(items), "loaded": loaded, "skipped": skipped})
    preview_rows = "".join(
        f"<tr><td>{esc(i.get('id'))}</td><td>{esc(i.get('completed'))}</td><td>{esc(i.get('due_at'))}</td><td>{esc(i.get('description'))}</td></tr>"
        for i in items[:25]
    ) or "<tr><td colspan='4' class='muted'>No Omi action items returned.</td></tr>"
    result = f"""
    <section class='card'>
      <h2>Loaded {esc(loaded)} of {esc(len(items))} Omi action items</h2>
      <p class='muted'>Loaded items are staged as review candidates. Approve them from the review queue before they become primary tasks.</p>
      <p class='row'><a class='button' href='/tasks/review'>Review loaded candidates</a><a class='button' href='/tasks/submissions'>View submissions</a></p>
      <table><tr><th>Omi ID</th><th>Completed</th><th>Due</th><th>Description</th></tr>{preview_rows}</table>
    </section>
    """
    return layout("Load tasks from Omi", load_omi_form(result), user)


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
