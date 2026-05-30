"""One-shot rewrite of Site/index3d.html:
- Remove the hardcoded PAPERS array literal.
- Remove the hardcoded BT_TREE object literal.
- Insert a fetch-based loader that produces PAPERS and BT_TREE in the same shape.
- Insert an upload-button handler at the very end of the <script type="module"> block.
Idempotent: a sentinel marker is added so re-runs skip.
"""
from __future__ import annotations
import re
from pathlib import Path

HTML = Path("/Users/likun/Desktop/paper-SciPro/Site/index3d.html")
SENTINEL = "/* paper-scipro-backend-wired */"

src = HTML.read_text(encoding="utf-8")
if SENTINEL in src:
    print("already wired, skipping")
    raise SystemExit(0)

# ---- 1) cut the PAPERS literal ----
m_papers = re.search(
    r"// ==================== Paper data \(q/w\) ====================\nconst PAPERS = \[",
    src,
)
if not m_papers:
    raise SystemExit("could not find PAPERS opener")
papers_start = m_papers.start()
# find matching `];` at the end of the PAPERS array. The literal ends with the line `];`
# followed by `\n\n// ==================== Hierarchical B_t tree`
m_after = re.search(
    r"\];\n\n// ==================== Hierarchical B_t tree \(reflects boundary_tree\.json\) ====================\n",
    src[papers_start:],
)
if not m_after:
    raise SystemExit("could not find PAPERS closer / BT_TREE opener")
bt_anchor = papers_start + m_after.end()  # start of `const BT_TREE = {`

# ---- 2) cut the BT_TREE literal ----
# BT_TREE ends with `};\n\nconst YEARS = [2023, 2024, 2025];`
m_after2 = re.search(r"\n};\n\nconst YEARS = \[2023, 2024, 2025\];", src[bt_anchor:])
if not m_after2:
    raise SystemExit("could not find BT_TREE closer")
bt_end = bt_anchor + m_after2.start() + len("\n};\n")  # include the `};\n` of BT_TREE

# ---- 3) compose new front block ----
new_block = (
    "// ==================== Backend-driven data " + SENTINEL + " ====================\n"
    "const API = window.PAPER_SCIPRO_API || 'http://127.0.0.1:8765';\n"
    "const BOUNDARY_MAP = {'边界内问题':'inside','边界迁移问题':'migrate','边界外问题':'outside'};\n"
    "const DIM_COLORS = { D: 0x34d399, M: 0xa78bfa, E: 0xf59e0b, V: 0xfb7185 };\n"
    "let PAPERS = [];\n"
    "let BT_TREE = {};\n"
    "async function loadFromBackend() {\n"
    "  const apiStatusEl = document.getElementById('api-status');\n"
    "  try {\n"
    "    const idxRes = await fetch(`${API}/api/papers`);\n"
    "    if (!idxRes.ok) throw new Error('papers HTTP ' + idxRes.status);\n"
    "    const idx = await idxRes.json();\n"
    "    const treeRes = await fetch(`${API}/api/boundary-tree`);\n"
    "    if (!treeRes.ok) throw new Error('boundary-tree HTTP ' + treeRes.status);\n"
    "    const tree = await treeRes.json();\n"
    "    const details = await Promise.all(idx.papers.map(p =>\n"
    "      fetch(`${API}/api/papers/${encodeURIComponent(p.paper_id)}`).then(r => r.json())));\n"
    "    PAPERS = details.map((d, i) => ({\n"
    "      id: d.paper_id,\n"
    "      year: d.year,\n"
    "      order: idx.papers[i].order,\n"
    "      title: d.title,\n"
    "      venue: d.venue,\n"
    "      boundary: BOUNDARY_MAP[d.boundary_position] || 'inside',\n"
    "      push_dimensions: d.push_dimensions,\n"
    "      q: d.question || {},\n"
    "      w: d.work || {}\n"
    "    }));\n"
    "    BT_TREE = tree;\n"
    "    for (const k of ['D','M','E','V']) {\n"
    "      if (BT_TREE[k] && DIM_COLORS[k]) BT_TREE[k].color = DIM_COLORS[k];\n"
    "    }\n"
    "    if (apiStatusEl) apiStatusEl.textContent = `${API} · ${PAPERS.length} 篇`;\n"
    "  } catch (e) {\n"
    "    if (apiStatusEl) { apiStatusEl.textContent = '后端无响应: ' + e.message; apiStatusEl.style.color = '#fb7185'; }\n"
    "    throw e;\n"
    "  }\n"
    "}\n"
    "await loadFromBackend();\n"
    "\n"
)

# ---- 4) splice ----
new_src = src[:papers_start] + new_block + src[bt_end:]

# ---- 5) append upload handler at end of <script type=module> ----
upload_handler = """
// ==================== Upload-paper handler (auto-feed) ====================
(() => {
  const btn = document.getElementById('upload-btn');
  const fileEl = document.getElementById('upload-pdf');
  const status = document.getElementById('upload-status');
  if (!btn || !fileEl) return;
  btn.addEventListener('click', async () => {
    if (!fileEl.files || !fileEl.files.length) {
      status.textContent = '请先选择 PDF';
      return;
    }
    const f = fileEl.files[0];
    btn.disabled = true;
    status.textContent = '上传中...';
    const fd = new FormData();
    fd.append('pdf', f);
    let res;
    try {
      res = await fetch(`${API}/api/papers`, { method: 'POST', body: fd });
    } catch (e) { status.textContent = '上传失败: ' + e.message; btn.disabled = false; return; }
    if (!res.ok) { status.textContent = '上传失败 HTTP ' + res.status; btn.disabled = false; return; }
    const { task_id, paper_id } = await res.json();
    status.textContent = `任务 ${task_id} 启动 · ${paper_id}`;
    while (true) {
      await new Promise(s => setTimeout(s, 2500));
      const t = await fetch(`${API}/api/tasks/${task_id}`).then(r => r.json()).catch(() => null);
      if (!t) { status.textContent = '查询任务失败'; break; }
      status.textContent = `${t.status} · ${t.step}`;
      if (t.status === 'done') {
        status.textContent = '完成 · 重新加载...';
        setTimeout(() => location.reload(), 800);
        break;
      }
      if (t.status === 'failed') {
        const head = (t.error || '').split('\\n')[0];
        status.textContent = '失败: ' + head;
        btn.disabled = false;
        break;
      }
    }
  });
})();
"""

# inject before the closing </script> of the module script. There may be multiple
# </script> tags, but the module one is the last big one before </body>. Use last index.
end_tag = "</script>"
last_close = new_src.rfind(end_tag)
if last_close == -1:
    raise SystemExit("no </script> found")
new_src = new_src[:last_close] + upload_handler + new_src[last_close:]

HTML.write_text(new_src, encoding="utf-8")
print("rewired OK; sentinel:", SENTINEL)
