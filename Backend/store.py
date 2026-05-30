"""File-system JSON store. Single source of truth = ../Outputs/."""
from __future__ import annotations
import json
import os
from contextlib import contextmanager
from pathlib import Path
from typing import Any
from filelock import FileLock

PROJECT_ROOT = Path(__file__).resolve().parent.parent
OUTPUTS = PROJECT_ROOT / "Outputs"
PAPERS_DIR = PROJECT_ROOT / "Papers"

BOUNDARY_TREE = OUTPUTS / "boundary_tree.json"
PAPERS_INDEX = OUTPUTS / "papers_index.json"
DELTAS = OUTPUTS / "deltas.json"
QUESTION_DIR = OUTPUTS / "question"
WORK_DIR = OUTPUTS / "work"
TEXT_DIR = OUTPUTS / "text"
TASKS_DIR = OUTPUTS / ".tasks"
LOCK_DIR = OUTPUTS / ".locks"

for d in (QUESTION_DIR, WORK_DIR, TEXT_DIR, TASKS_DIR, LOCK_DIR, PAPERS_DIR):
    d.mkdir(parents=True, exist_ok=True)


def _read_json(p: Path, default: Any = None) -> Any:
    if not p.exists():
        return default
    with p.open("r", encoding="utf-8") as f:
        return json.load(f)


def _write_json(p: Path, data: Any) -> None:
    p.parent.mkdir(parents=True, exist_ok=True)
    tmp = p.with_suffix(p.suffix + ".tmp")
    with tmp.open("w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    os.replace(tmp, p)


@contextmanager
def lock(name: str):
    with FileLock(str(LOCK_DIR / f"{name}.lock"), timeout=30):
        yield


# ---- boundary_tree ----
def read_boundary_tree() -> dict:
    return _read_json(BOUNDARY_TREE, default={})


def write_boundary_tree(tree: dict) -> None:
    with lock("boundary_tree"):
        _write_json(BOUNDARY_TREE, tree)


# ---- papers_index ----
def read_papers_index() -> dict:
    return _read_json(PAPERS_INDEX, default={"schema_version": "1.0", "papers": []})


def write_papers_index(idx: dict) -> None:
    with lock("papers_index"):
        _write_json(PAPERS_INDEX, idx)


def upsert_paper(entry: dict) -> None:
    with lock("papers_index"):
        idx = _read_json(PAPERS_INDEX, default={"schema_version": "1.0", "papers": []})
        papers = idx.get("papers", [])
        replaced = False
        for i, p in enumerate(papers):
            if p.get("paper_id") == entry.get("paper_id"):
                papers[i] = {**p, **entry}
                replaced = True
                break
        if not replaced:
            papers.append(entry)
        # keep stable order by year then order
        papers.sort(key=lambda p: (p.get("year", 9999), p.get("order", 9999)))
        idx["papers"] = papers
        _write_json(PAPERS_INDEX, idx)


# ---- deltas ----
def read_deltas() -> dict:
    return _read_json(DELTAS, default={})


def append_delta(year: int, entry: dict) -> None:
    with lock("deltas"):
        deltas = _read_json(DELTAS, default={})
        bucket = deltas.setdefault(str(year), [])
        # idempotent: dedup by (dim, path, item, op)
        sig = (entry["dim"], tuple(entry["path"]), entry["item"], entry["op"])
        for ex in bucket:
            ex_sig = (ex["dim"], tuple(ex["path"]), ex["item"], ex["op"])
            if ex_sig == sig:
                # merge papers
                existing = set(ex.get("papers", []))
                existing.update(entry.get("papers", []))
                ex["papers"] = sorted(existing)
                _write_json(DELTAS, deltas)
                return
        bucket.append(entry)
        _write_json(DELTAS, deltas)


# ---- per-paper files ----
def write_question(paper_id: str, q: dict) -> Path:
    p = QUESTION_DIR / f"{paper_id}.json"
    _write_json(p, q)
    return p


def write_work(paper_id: str, w: dict) -> Path:
    p = WORK_DIR / f"{paper_id}.json"
    _write_json(p, w)
    return p


def read_question(paper_id: str) -> dict | None:
    # try {paper_id}.json then any file matching paper_title prefix
    p = QUESTION_DIR / f"{paper_id}.json"
    if p.exists():
        return _read_json(p)
    return None


def read_work(paper_id: str) -> dict | None:
    p = WORK_DIR / f"{paper_id}.json"
    if p.exists():
        return _read_json(p)
    return None


# ---- task state ----
def task_path(task_id: str) -> Path:
    return TASKS_DIR / f"{task_id}.json"


def read_task(task_id: str) -> dict | None:
    return _read_json(task_path(task_id))


def write_task(task: dict) -> None:
    _write_json(task_path(task["task_id"]), task)
