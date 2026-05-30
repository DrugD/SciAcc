"""Claude API wrapper. Generates question.json / work.json / push_dimensions.

Uses prompt caching: the long extracted paper text is sent once and reused
across question/work/push-dimensions calls within a 5-minute window.
"""
from __future__ import annotations
import json
import os
import re
from pathlib import Path
from typing import Any

from anthropic import Anthropic

PROMPTS_DIR = Path(__file__).resolve().parent / "prompts"
DEFAULT_MODEL = os.environ.get("ANTHROPIC_MODEL", "claude-opus-4-7")


def _client() -> Anthropic:
    key = os.environ.get("ANTHROPIC_API_KEY")
    if not key:
        raise RuntimeError("ANTHROPIC_API_KEY not set in environment")
    return Anthropic(api_key=key)


def _read_prompt(name: str) -> str:
    return (PROMPTS_DIR / name).read_text(encoding="utf-8")


def _extract_json(text: str) -> dict:
    """Pull the first {...} block out of a model response, robust to ```json fences."""
    # try fenced first
    m = re.search(r"```(?:json)?\s*(\{.*?\})\s*```", text, re.S)
    if m:
        return json.loads(m.group(1))
    # otherwise greedy braces
    start = text.find("{")
    end = text.rfind("}")
    if start == -1 or end == -1 or end <= start:
        raise ValueError(f"no JSON object found in model output: {text[:200]}...")
    return json.loads(text[start : end + 1])


def _call(system_prompt: str, paper_text: str, user_instruction: str, model: str) -> str:
    """Single Claude call with prompt caching on system + paper text."""
    client = _client()
    resp = client.messages.create(
        model=model,
        max_tokens=4096,
        system=[
            {
                "type": "text",
                "text": system_prompt,
                "cache_control": {"type": "ephemeral"},
            }
        ],
        messages=[
            {
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": f"以下是论文全文（已抽取）：\n\n{paper_text}",
                        "cache_control": {"type": "ephemeral"},
                    },
                    {"type": "text", "text": user_instruction},
                ],
            }
        ],
    )
    # join all text blocks
    return "".join(b.text for b in resp.content if getattr(b, "type", "") == "text")


def generate_question(paper_text: str, model: str = DEFAULT_MODEL) -> dict:
    sys_prompt = _read_prompt("question.md")
    out = _call(
        system_prompt=sys_prompt,
        paper_text=paper_text,
        user_instruction=(
            "请只输出 1 个 JSON 对象，字段名严格为：q_main, q_formal, q_background, "
            "q_boundary_position (取值: 边界内问题|边界迁移问题|边界外问题), "
            "q_boundary_position_reason, required_evidence (string[]), required_evaluation (string[]). "
            "再额外加 paper_title, venue 两个字段。仅输出 JSON，不要 Markdown 解释。"
        ),
        model=model,
    )
    return _extract_json(out)


def generate_work(paper_text: str, model: str = DEFAULT_MODEL) -> dict:
    sys_prompt = _read_prompt("work.md")
    out = _call(
        system_prompt=sys_prompt,
        paper_text=paper_text,
        user_instruction=(
            "请只输出 1 个 JSON 对象，字段名严格为：w_summary, w_type, w_object, w_mechanism, "
            "w_evidence (string[]), w_evaluation (string[]), w_scope, w_failure_scenarios (string[]). "
            "再额外加 paper_title, venue 两个字段。仅输出 JSON，不要 Markdown 解释。"
        ),
        model=model,
    )
    return _extract_json(out)


def generate_push_dimensions(q: dict, w: dict, model: str = DEFAULT_MODEL) -> dict:
    """Use the merge prompt to ask Claude which of D/M/E/V the paper pushes."""
    sys_prompt = _read_prompt("merge.md")
    payload = json.dumps({"question": q, "work": w}, ensure_ascii=False, indent=2)
    out = _call(
        system_prompt=sys_prompt,
        paper_text=payload,
        user_instruction=(
            "基于上面这篇论文的 q.json 与 w.json，请只输出一个 JSON 对象："
            '{"primary": ["D"|"M"|"E"|"V"...], "secondary": [...], '
            '"summary": "<<= 80 字>>", "multi_dim_link": "单维|双维|三维|四维(简短描述)"}. '
            "primary 通常 1–2 个，secondary ≤2 个。仅输出 JSON。"
        ),
        model=model,
    )
    return _extract_json(out)
