"""End-to-end pipeline: PDF -> text -> q.json -> w.json -> push_dimensions -> merge tree."""
from __future__ import annotations
import asyncio
import os
import sys
import traceback
from datetime import datetime, timezone
from pathlib import Path
from typing import Optional

import pymupdf

from Backend import store
from Backend import analyzer, merger


def _now() -> str:
    return datetime.now(timezone.utc).isoformat()


def _update(task: dict, **kw) -> None:
    task.update(kw)
    task["updated_at"] = _now()
    store.write_task(task)


def extract_text(pdf_path: str, paper_id: str) -> str:
    doc = pymupdf.open(pdf_path)
    chunks = []
    for i, page in enumerate(doc):
        chunks.append(f"\n\n===== PAGE {i+1} =====\n" + page.get_text())
    doc.close()
    text = "".join(chunks)
    out = store.TEXT_DIR / f"{paper_id}.txt"
    out.write_text(text, encoding="utf-8")
    return text


def _detect_year(q: dict, w: dict, fallback: int) -> int:
    venue = (w.get("venue") or q.get("venue") or "").strip()
    import re

    m = re.search(r"(20\d{2})", venue)
    if m:
        return int(m.group(1))
    return fallback


def run_pipeline(
    task_id: str,
    paper_id: str,
    pdf_path: str,
    year: Optional[int],
    title: Optional[str],
    venue: Optional[str],
) -> None:
    task = store.read_task(task_id) or {
        "task_id": task_id,
        "paper_id": paper_id,
        "started_at": _now(),
    }
    try:
        _update(task, status="extracting", step="pymupdf text extraction")
        text = extract_text(pdf_path, paper_id)
        if len(text.strip()) < 200:
            _update(
                task,
                status="failed",
                step="extraction",
                error="extracted text < 200 chars; PDF likely scanned. Use the OCR fallback path.",
            )
            return

        _update(task, status="analyzing", step="claude: question.json")
        q = analyzer.generate_question(text)
        if title:
            q.setdefault("paper_title", title)
        if venue:
            q.setdefault("venue", venue)
        store.write_question(paper_id, q)

        _update(task, status="analyzing", step="claude: work.json")
        w = analyzer.generate_work(text)
        if title:
            w.setdefault("paper_title", title)
        if venue:
            w.setdefault("venue", venue)
        store.write_work(paper_id, w)

        _update(task, status="analyzing", step="claude: push_dimensions")
        push = analyzer.generate_push_dimensions(q, w)

        # propagate push_dimensions into q/w files for the front-end
        q["push_dimensions"] = push
        w["push_dimensions"] = push
        store.write_question(paper_id, q)
        store.write_work(paper_id, w)

        # paper-index entry
        resolved_year = year or _detect_year(q, w, fallback=datetime.now().year)
        idx = store.read_papers_index()
        existing_count = len(idx.get("papers", []))
        entry = {
            "paper_id": paper_id,
            "order": existing_count + 1,
            "year": resolved_year,
            "title": title or q.get("paper_title") or paper_id,
            "venue": venue or q.get("venue") or "",
            "boundary_position": q.get("q_boundary_position"),
            "pdf_path": str(Path(pdf_path).relative_to(store.PROJECT_ROOT)),
            "question_path": f"Outputs/question/{paper_id}.json",
            "work_path": f"Outputs/work/{paper_id}.json",
            "push_dimensions": push,
        }
        store.upsert_paper(entry)

        _update(task, status="merging", step="boundary-tree merge")
        applied = merger.merge_paper(paper_id, resolved_year, q, w, push)

        _update(
            task,
            status="done",
            step="complete",
            result={"applied_ops": applied, "paper_entry": entry},
        )
    except Exception as e:
        _update(
            task,
            status="failed",
            step=task.get("step", "unknown"),
            error=f"{type(e).__name__}: {e}\n{traceback.format_exc()}",
        )


async def run_pipeline_async(*args, **kwargs) -> None:
    """Run the sync pipeline in a thread so we don't block the event loop."""
    await asyncio.to_thread(run_pipeline, *args, **kwargs)
