"""Boundary-tree merger.

Given a paper's q+w+push_dimensions, ask Claude to propose a list of leaf
operations against the existing boundary_tree.json, then apply them
idempotently (only-add / sibling-of / split, never delete or rewrite).
"""
from __future__ import annotations
import json
import os
import re
from typing import Any

from Backend import store
from Backend.analyzer import _call, _extract_json, _read_prompt, DEFAULT_MODEL

DIMS = ("D", "M", "E", "V")


def _walk_leaves(node: dict, path: list[str]):
    """Yield (path_to_parent, leaf_dict) for every leaf-ish node carrying a 'year'."""
    label = node.get("label")
    children = node.get("children")
    if not children:
        yield path, node
        return
    for c in children:
        yield from _walk_leaves(c, path + [label] if label else path)


def _find_node_by_path(root: dict, path: list[str]) -> dict | None:
    """Walk children by exact label match."""
    cur = root
    for label in path:
        if not cur.get("children"):
            return None
        match = next((c for c in cur["children"] if c.get("label") == label), None)
        if match is None:
            return None
        cur = match
    return cur


def _add_leaf_at(root: dict, parent_path: list[str], leaf: dict) -> bool:
    """Insert/merge a leaf under parent_path. Returns True if newly added,
    False if leaf already existed (papers_introduced merged in either case)."""
    parent = _find_node_by_path(root, parent_path)
    if parent is None:
        # parent path doesn't exist: create the chain at the dimension root
        cur = root
        for label in parent_path:
            children = cur.setdefault("children", [])
            nxt = next((c for c in children if c.get("label") == label), None)
            if nxt is None:
                nxt = {"label": label, "children": []}
                children.append(nxt)
            cur = nxt
        parent = cur
    children = parent.setdefault("children", [])
    existing = next((c for c in children if c.get("label") == leaf["label"]), None)
    if existing:
        # merge papers_introduced as set
        intro = set(existing.get("papers_introduced") or [])
        intro.update(leaf.get("papers_introduced") or [])
        existing["papers_introduced"] = sorted(intro)
        # keep year as min
        if leaf.get("year") and (not existing.get("year") or leaf["year"] < existing["year"]):
            existing["year"] = leaf["year"]
        return False
    children.append(leaf)
    return True


def propose_operations(q: dict, w: dict, push: dict, current_tree: dict, model: str = DEFAULT_MODEL) -> list[dict]:
    """Ask Claude for a list of {dim, parent_path, item, op, sibling_of?} operations."""
    sys_prompt = _read_prompt("merge.md")
    payload = json.dumps(
        {
            "current_tree": current_tree,
            "incoming_paper": {"question": q, "work": w, "push_dimensions": push},
        },
        ensure_ascii=False,
        indent=2,
    )
    instruction = (
        "请你扮演 boundary tree merger。基于 prompt_boundary_tree.md 的 6 步流程，"
        "对照 current_tree 和 incoming_paper，输出一个 JSON 对象："
        '{"operations": [{"dim": "D|M|E|V", "parent_path": ["...","..."], '
        '"item": "<新叶子标签>", "op": "add|sibling-of|split", '
        '"sibling_of": "<可空，仅当 op=sibling-of>"}, ...]}. '
        "约束：不要重写已有叶子；同义叶子要复用；parent_path 必须是 current_tree 中已有路径或合理新增路径；"
        "operations 通常 5–15 个。仅输出 JSON。"
    )
    out = _call(system_prompt=sys_prompt, paper_text=payload, user_instruction=instruction, model=model)
    parsed = _extract_json(out)
    return parsed.get("operations", [])


def apply_operations(operations: list[dict], paper_id: str, year: int) -> list[dict]:
    """Apply ops to boundary_tree.json + deltas.json. Idempotent.

    Returns the list of applied delta entries.
    """
    applied: list[dict] = []
    with store.lock("boundary_tree"):
        tree = store.read_boundary_tree()
        for op_entry in operations:
            dim = op_entry.get("dim")
            if dim not in DIMS:
                continue
            parent_path = op_entry.get("parent_path") or []
            item = op_entry.get("item")
            op = op_entry.get("op", "add")
            if not item:
                continue
            dim_root = tree.get(dim)
            if not dim_root:
                continue
            leaf = {"label": item, "year": year, "papers_introduced": [paper_id]}
            newly_added = _add_leaf_at(dim_root, parent_path, leaf)
            applied.append(
                {
                    "dim": dim,
                    "path": parent_path,
                    "item": item,
                    "op": "add" if newly_added else "merge",
                    "sibling_of": op_entry.get("sibling_of"),
                    "papers": [paper_id],
                }
            )
        store._write_json(store.BOUNDARY_TREE, tree)

    # write deltas
    for entry in applied:
        if entry["op"] == "merge":
            # an idempotent re-add is not a delta event
            continue
        delta = {k: v for k, v in entry.items() if v is not None}
        if not delta.get("sibling_of"):
            delta.pop("sibling_of", None)
        store.append_delta(year, delta)
    return applied


def merge_paper(paper_id: str, year: int, q: dict, w: dict, push: dict, model: str = DEFAULT_MODEL) -> list[dict]:
    """High-level entry: propose + apply."""
    tree = store.read_boundary_tree()
    ops = propose_operations(q, w, push, tree, model=model)
    return apply_operations(ops, paper_id, year)
