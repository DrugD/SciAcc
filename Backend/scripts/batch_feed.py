"""Batch-feed all PDFs in Papers/ through the pipeline.

Idempotent: papers already in papers_index.json are skipped.
Concurrent: up to N papers analyzed in parallel.
Resumable: each paper writes its task state to Outputs/.tasks/, so you can
restart this script and only the unfinished/failed ones will be retried.

Usage:
    .venv/bin/python Backend/scripts/batch_feed.py [--limit N] [--concurrency 3]
                                                   [--retry-failed] [--dry-run]
"""
from __future__ import annotations
import argparse
import asyncio
import json
import re
import sys
import unicodedata
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent))

from dotenv import load_dotenv

load_dotenv(Path(__file__).resolve().parent.parent / ".env")

from Backend import store
from Backend.pipeline import run_pipeline


def slugify(name: str) -> str:
    """Stable, filename-safe paper_id derived from PDF stem."""
    s = unicodedata.normalize("NFKC", name)
    s = re.sub(r"[^A-Za-z0-9]+", "_", s).strip("_")
    return s[:60] or "paper"


def already_done(paper_id: str, pdf_filename: str) -> bool:
    """Skip a PDF if either:
      - its slug-derived paper_id is already indexed, OR
      - any existing entry's pdf_path basename matches this PDF.
    The second check covers the original 5 papers that were seeded
    with hand-picked paper_ids (TDHNN, THNN, ...) different from the
    slug derived from their filename.
    """
    idx = store.read_papers_index()
    for p in idx.get("papers", []):
        if p.get("paper_id") == paper_id:
            return True
        existing_pdf = p.get("pdf_path", "")
        if existing_pdf and Path(existing_pdf).name == pdf_filename:
            return True
    return False


def task_for(paper_id: str) -> dict | None:
    """Find the most recent task for this paper_id."""
    candidates = sorted(store.TASKS_DIR.glob("task-*.json"))
    best = None
    for tp in candidates:
        try:
            t = json.loads(tp.read_text())
        except Exception:
            continue
        if t.get("paper_id") == paper_id:
            best = t
    return best


async def run_one(pdf_path: Path, retry_failed: bool, sem: asyncio.Semaphore) -> tuple[str, str, str]:
    """Returns (paper_id, status, note). Honors the semaphore for concurrency."""
    paper_id = slugify(pdf_path.stem)
    if already_done(paper_id, pdf_path.name):
        return paper_id, "skipped", "already in papers_index"

    if not retry_failed:
        prev = task_for(paper_id)
        if prev and prev.get("status") == "failed":
            return paper_id, "skipped-failed", prev.get("error", "").split("\n")[0]

    async with sem:
        # copy/save the PDF into Papers/<paper_id>.pdf if not already there
        canonical = store.PAPERS_DIR / f"{paper_id}.pdf"
        if not canonical.exists():
            # symlink to the original to avoid duplicating bytes
            try:
                canonical.symlink_to(pdf_path.resolve())
            except FileExistsError:
                pass

        task_id = f"task-batch-{paper_id[:24]}"
        from datetime import datetime, timezone

        store.write_task(
            {
                "task_id": task_id,
                "paper_id": paper_id,
                "status": "pending",
                "step": "queued",
                "started_at": datetime.now(timezone.utc).isoformat(),
                "updated_at": datetime.now(timezone.utc).isoformat(),
            }
        )

        # Pipeline is sync + LLM-bound: hand to a thread.
        await asyncio.to_thread(
            run_pipeline,
            task_id=task_id,
            paper_id=paper_id,
            pdf_path=str(canonical),
            year=None,
            title=pdf_path.stem,
            venue=None,
        )
        t = store.read_task(task_id) or {}
        status = t.get("status", "unknown")
        note = t.get("step", "") if status == "done" else (t.get("error", "") or "").split("\n")[0]
        return paper_id, status, note


async def main_async(args: argparse.Namespace) -> None:
    pdfs = sorted(p for p in store.PAPERS_DIR.glob("*.pdf"))
    if args.limit:
        pdfs = pdfs[: args.limit]
    print(f"[batch] {len(pdfs)} PDFs queued · concurrency={args.concurrency}")

    if args.dry_run:
        for p in pdfs:
            pid = slugify(p.stem)
            done = "done" if already_done(pid, p.name) else "pending"
            print(f"  [{done:7s}] {pid}  ({p.name})")
        return

    sem = asyncio.Semaphore(args.concurrency)
    tasks = [asyncio.create_task(run_one(p, args.retry_failed, sem)) for p in pdfs]

    n_done, n_skip, n_fail = 0, 0, 0
    for fut in asyncio.as_completed(tasks):
        pid, status, note = await fut
        marker = {"done": "✓", "skipped": "○", "skipped-failed": "○", "failed": "✗"}.get(status, "?")
        if status == "done":
            n_done += 1
        elif status.startswith("skipped"):
            n_skip += 1
        else:
            n_fail += 1
        print(f"  {marker} [{status:14s}] {pid}  {note[:80]}")
    print(f"[batch] done={n_done} skipped={n_skip} failed={n_fail}")


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--limit", type=int, default=0, help="cap the number of PDFs (0 = all)")
    ap.add_argument("--concurrency", type=int, default=3)
    ap.add_argument("--retry-failed", action="store_true", help="re-run papers that previously failed")
    ap.add_argument("--dry-run", action="store_true")
    args = ap.parse_args()
    asyncio.run(main_async(args))


if __name__ == "__main__":
    main()
