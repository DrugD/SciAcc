"""FastAPI entry point.

Run:
    cd /Users/likun/Desktop/paper-SciPro
    .venv/bin/python -m uvicorn Backend.main:app --port 8000 --reload
"""
from __future__ import annotations
import asyncio
import sys
import uuid
from datetime import datetime, timezone
from pathlib import Path
from typing import Optional

# Make Backend/ importable when run via `python -m uvicorn Backend.main:app`
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

# Load Backend/.env so ANTHROPIC_API_KEY etc. are available without a manual `export`.
from dotenv import load_dotenv

load_dotenv(Path(__file__).resolve().parent / ".env")

from fastapi import FastAPI, File, Form, HTTPException, UploadFile, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from Backend import store
from Backend.schemas import (
    BoundaryTree,
    DeltasFile,
    PaperDetail,
    PapersIndex,
    TaskState,
    UploadResponse,
)

app = FastAPI(title="Paper-SciPro Backend", version="1.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # local dev: file:// + http://localhost:*
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.middleware("http")
async def no_store(request, call_next):
    """Force browsers to never cache JSON responses — the boundary tree and
    papers index change after every upload, and Chrome's heuristic cache will
    otherwise serve stale data even after location.reload()."""
    response = await call_next(request)
    if request.url.path.startswith("/api/"):
        response.headers["Cache-Control"] = "no-store, max-age=0"
        response.headers["Pragma"] = "no-cache"
    return response


def _now() -> str:
    return datetime.now(timezone.utc).isoformat()


@app.get("/api/health")
async def health() -> dict:
    return {"status": "ok", "time": _now()}


@app.get("/api/boundary-tree")
async def get_boundary_tree() -> dict:
    tree = store.read_boundary_tree()
    if not tree:
        raise HTTPException(404, "boundary_tree.json not found")
    return tree


@app.get("/api/papers", response_model=PapersIndex)
async def list_papers() -> dict:
    return store.read_papers_index()


@app.get("/api/papers/{paper_id}", response_model=PaperDetail)
async def get_paper(paper_id: str) -> dict:
    idx = store.read_papers_index()
    entry = next((p for p in idx.get("papers", []) if p["paper_id"] == paper_id), None)
    if not entry:
        raise HTTPException(404, f"paper {paper_id} not in papers_index")
    q = store.read_question(paper_id) or {}
    w = store.read_work(paper_id) or {}
    return {
        "paper_id": paper_id,
        "title": entry.get("title", ""),
        "venue": entry.get("venue", ""),
        "year": entry.get("year", 0),
        "boundary_position": entry.get("boundary_position"),
        "push_dimensions": entry.get("push_dimensions"),
        "question": q,
        "work": w,
    }


@app.get("/api/deltas")
async def get_deltas() -> dict:
    return store.read_deltas()


@app.get("/api/tasks/{task_id}")
async def get_task(task_id: str) -> dict:
    t = store.read_task(task_id)
    if not t:
        raise HTTPException(404, f"task {task_id} not found")
    return t


def _slug(name: str) -> str:
    safe = "".join(c if c.isalnum() or c in "-_" else "_" for c in name)
    return safe.strip("_") or f"paper-{uuid.uuid4().hex[:8]}"


@app.post("/api/papers", response_model=UploadResponse)
async def upload_paper(
    background: BackgroundTasks,
    pdf: UploadFile = File(...),
    paper_id: Optional[str] = Form(default=None),
    year: Optional[int] = Form(default=None),
    title: Optional[str] = Form(default=None),
    venue: Optional[str] = Form(default=None),
) -> dict:
    if not pdf.filename or not pdf.filename.lower().endswith(".pdf"):
        raise HTTPException(400, "expected a .pdf upload")
    pdf_bytes = await pdf.read()
    if not pdf_bytes:
        raise HTTPException(400, "empty pdf upload")
    pid = paper_id or _slug(Path(pdf.filename).stem)
    task_id = f"task-{uuid.uuid4().hex[:12]}"
    state = {
        "task_id": task_id,
        "paper_id": pid,
        "status": "pending",
        "step": "queued",
        "started_at": _now(),
        "updated_at": _now(),
    }
    store.write_task(state)
    # save the pdf to Papers/<pid>.pdf right away so it's persisted even if pipeline fails
    pdf_path = store.PAPERS_DIR / f"{pid}.pdf"
    pdf_path.write_bytes(pdf_bytes)

    # Run pipeline in background to keep request fast
    from Backend.pipeline import run_pipeline_async

    background.add_task(
        run_pipeline_async,
        task_id=task_id,
        paper_id=pid,
        pdf_path=str(pdf_path),
        year=year,
        title=title,
        venue=venue,
    )
    return {"task_id": task_id, "paper_id": pid, "status": "pending"}
