"""Apply the same backend wiring + dynamic-year handling to Site/index.html (2D page).

Differences from wire_frontend.py (which targeted index3d.html):
- index.html uses a classic <script>, not <script type="module">. We wrap the
  body in an async IIFE so top-level await works.
- We move the YEARS / setupYears / yearShell helpers in front of the rest of
  the script so they are defined before any consumer runs.
- Same cache-busting + no-store fetch wrapper.

Idempotent via SENTINEL.
"""
from __future__ import annotations
import re
from pathlib import Path

HTML = Path("/Users/likun/Desktop/paper-SciPro/Site/index.html")
SENTINEL = "/* paper-scipro-backend-wired-2d */"

src = HTML.read_text(encoding="utf-8")
if SENTINEL in src:
    print("already wired, skipping")
    raise SystemExit(0)

# ---- 1) timeline labels & slider become empty placeholders ----
labels_old = (
    '      <div class="timeline-labels">\n'
    '        <span data-year="2023">t₁ · 2023</span>\n'
    '        <span data-year="2024">t₂ · 2024</span>\n'
    '        <span data-year="2025">t₃ · 2025</span>\n'
    '      </div>\n'
    '      <input type="range" min="0" max="2" step="1" value="2" id="timeline" />\n'
)
labels_new = (
    '      <div class="timeline-labels" id="timeline-labels"></div>\n'
    '      <input type="range" min="0" max="0" step="1" value="0" id="timeline" />\n'
)
if labels_old not in src:
    raise SystemExit("could not find timeline-labels block in index.html")
src = src.replace(labels_old, labels_new, 1)

# ---- 2) inject upload-paper UI into the header controls strip ----
toggles_anchor = '    <div class="toggles">\n'
upload_block = (
    '    <div class="toggles" style="margin-left:auto;">\n'
    '      <input type="file" id="upload-pdf" accept=".pdf" style="font-size:11px;color:var(--muted);" />\n'
    '      <button id="upload-btn" style="padding:4px 10px;background:rgba(122,162,255,0.18);color:var(--text);border:1px solid var(--border);border-radius:3px;cursor:pointer;font-size:11px;">上传并分析</button>\n'
    '      <span id="upload-status" style="font-size:11px;color:var(--muted);">就绪 · 后端 <code id="api-status">未连接</code></span>\n'
    '    </div>\n'
    + toggles_anchor
)
if toggles_anchor not in src:
    raise SystemExit("could not find toggles div")
src = src.replace(toggles_anchor, upload_block, 1)

# ---- 3) replace the entire embedded-data + script body ----
# Find the literal `const PAPERS = [` ... up to and including the closing `];`
# of the BT_TREE object. The simplest cut is the comment line after <script>.
script_open_marker = "<script>\n// ===== Data embedded directly so the page opens without a server =====\nconst PAPERS = ["
i = src.find(script_open_marker)
if i == -1:
    raise SystemExit("could not find script open + PAPERS literal")
script_open_end = i + len("<script>\n")  # leave the literal <script> tag in place

# Find the end of `const BT_TREE = { ... };`
# strategy: start scanning at `const BT_TREE = {` and balance braces.
bt_start_re = re.compile(r"const BT_TREE = \{", re.M)
m_bt = bt_start_re.search(src, script_open_end)
if not m_bt:
    raise SystemExit("could not find BT_TREE literal")
bt_brace_pos = m_bt.end() - 1  # the opening `{`
depth = 0
end_pos = -1
for j in range(bt_brace_pos, len(src)):
    ch = src[j]
    if ch == "{":
        depth += 1
    elif ch == "}":
        depth -= 1
        if depth == 0:
            end_pos = j + 1
            break
if end_pos == -1:
    raise SystemExit("could not balance BT_TREE braces")
# also consume the trailing `;\n`
if src[end_pos:end_pos + 2] == ";\n":
    end_pos += 2
elif src[end_pos:end_pos + 1] == ";":
    end_pos += 1

# Now also drop the `const YEARS = [2023, 2024, 2025];` line (we replace it
# with the dynamic variant inside loadFromBackend).
years_decl = "const YEARS = [2023, 2024, 2025];\n"
years_at = src.find(years_decl, end_pos)
if years_at == -1:
    raise SystemExit("could not find legacy YEARS declaration")

# Build replacement block: backend loader + dynamic year axis helpers.
loader_block = (
    "// ===== Backend-driven data " + SENTINEL + " =====\n"
    "const API = window.PAPER_SCIPRO_API || 'http://127.0.0.1:8765';\n"
    "const BOUNDARY_MAP = {'边界内问题':'inside','边界迁移问题':'migrate','边界外问题':'outside'};\n"
    "let PAPERS = [];\n"
    "let BT_TREE = {};\n"
    "let YEARS = [];\n"
    "async function loadFromBackend() {\n"
    "  const apiStatusEl = document.getElementById('api-status');\n"
    "  const bust = () => `?t=${Date.now()}`;\n"
    "  const opts = { cache: 'no-store' };\n"
    "  try {\n"
    "    const idx = await fetch(`${API}/api/papers${bust()}`, opts).then(r => { if (!r.ok) throw new Error('papers HTTP ' + r.status); return r.json(); });\n"
    "    const tree = await fetch(`${API}/api/boundary-tree${bust()}`, opts).then(r => { if (!r.ok) throw new Error('tree HTTP ' + r.status); return r.json(); });\n"
    "    const details = await Promise.all(idx.papers.map(p =>\n"
    "      fetch(`${API}/api/papers/${encodeURIComponent(p.paper_id)}${bust()}`, opts).then(r => r.json())));\n"
    "    PAPERS = details.map((d, i) => ({\n"
    "      id: d.paper_id, year: d.year, order: idx.papers[i].order,\n"
    "      title: d.title, venue: d.venue,\n"
    "      boundary: BOUNDARY_MAP[d.boundary_position] || 'inside',\n"
    "      push_dimensions: d.push_dimensions,\n"
    "      q: d.question || {},\n"
    "      w: d.work || {}\n"
    "    }));\n"
    "    BT_TREE = tree;\n"
    "    if (apiStatusEl) apiStatusEl.textContent = `${API} · ${PAPERS.length} 篇`;\n"
    "  } catch (e) {\n"
    "    if (apiStatusEl) { apiStatusEl.textContent = '后端无响应: ' + e.message; apiStatusEl.style.color = '#fb7185'; }\n"
    "    throw e;\n"
    "  }\n"
    "}\n"
    "function setupYears() {\n"
    "  YEARS = [...new Set(PAPERS.map(p => p.year).filter(Number.isFinite))].sort((a, b) => a - b);\n"
    "  if (YEARS.length === 0) YEARS = [new Date().getFullYear()];\n"
    "  const subs = '₁₂₃₄₅₆₇₈₉';\n"
    "  document.getElementById('timeline-labels').innerHTML =\n"
    "    YEARS.map((y, i) => `<span data-year=\"${y}\">t${subs[i] || ('('+(i+1)+')')} · ${y}</span>`).join('');\n"
    "  const slider = document.getElementById('timeline');\n"
    "  slider.min = '0'; slider.max = String(Math.max(0, YEARS.length - 1)); slider.value = slider.max;\n"
    "  document.getElementById('year-label').textContent = String(YEARS[YEARS.length - 1]);\n"
    "}\n"
)

# Inline upload handler for 2D page.
upload_handler = (
    "// ===== Upload handler =====\n"
    "(() => {\n"
    "  const btn = document.getElementById('upload-btn');\n"
    "  const fileEl = document.getElementById('upload-pdf');\n"
    "  const status = document.getElementById('upload-status');\n"
    "  if (!btn || !fileEl) return;\n"
    "  btn.addEventListener('click', async () => {\n"
    "    if (!fileEl.files || !fileEl.files.length) { status.textContent = '请先选择 PDF'; return; }\n"
    "    const f = fileEl.files[0]; btn.disabled = true; status.textContent = '上传中...';\n"
    "    const fd = new FormData(); fd.append('pdf', f);\n"
    "    let res; try { res = await fetch(`${API}/api/papers`, { method: 'POST', body: fd }); }\n"
    "    catch (e) { status.textContent = '上传失败: ' + e.message; btn.disabled = false; return; }\n"
    "    if (!res.ok) { status.textContent = '上传失败 HTTP ' + res.status; btn.disabled = false; return; }\n"
    "    const { task_id, paper_id } = await res.json();\n"
    "    status.textContent = `任务 ${task_id} 启动 · ${paper_id}`;\n"
    "    while (true) {\n"
    "      await new Promise(s => setTimeout(s, 2500));\n"
    "      const t = await fetch(`${API}/api/tasks/${task_id}`).then(r => r.json()).catch(() => null);\n"
    "      if (!t) { status.textContent = '查询失败'; break; }\n"
    "      status.textContent = `${t.status} · ${t.step}`;\n"
    "      if (t.status === 'done') { status.textContent = '完成 · 重新加载...'; setTimeout(() => location.reload(), 800); break; }\n"
    "      if (t.status === 'failed') { status.textContent = '失败: ' + ((t.error || '').split('\\n')[0]); btn.disabled = false; break; }\n"
    "    }\n"
    "  });\n"
    "})();\n"
)

# Splice: remove `// ===== Data embedded ... ===== const PAPERS = [...]; const BT_TREE = {...}; const YEARS = [...];`
# and replace with `(async () => { try { await loadFromBackend(); setupYears(); /* original rest */ } catch(e) { console.error(e); } })();`
#
# But the "original rest" runs the whole script body. We can't trivially wrap
# everything; instead, we (a) inject `await loadFromBackend(); setupYears();`
# inside an async IIFE that wraps the rest of the <script> tag, and (b) keep
# the rest of the script verbatim *inside* the IIFE.

# Carve up:
# pre = src up to and including the literal "<script>\n"
# middle = everything after <script>\n up to and including end_pos (the literal data block)
# rest = everything from end_pos to the closing </script>
pre = src[:script_open_end]                            # up to and including "<script>\n"
# skip the comment line "// ===== Data embedded ... =====\n" too
embedded_comment = "// ===== Data embedded directly so the page opens without a server =====\n"
if src[script_open_end:script_open_end + len(embedded_comment)] == embedded_comment:
    skip_start = script_open_end + len(embedded_comment)
else:
    skip_start = script_open_end
# years_at points at the start of `const YEARS = [...]`
# We want to drop everything from skip_start through `years_at + len(years_decl)`.
years_end = years_at + len(years_decl)
rest = src[years_end:]                                 # everything after legacy YEARS line

# Find closing </script>
close_at = rest.rfind("</script>")
if close_at == -1:
    raise SystemExit("could not find </script>")
script_body = rest[:close_at]
post = rest[close_at:]                                 # "</script>...\n</body>\n</html>"

new_script = (
    pre
    + loader_block
    + "(async () => {\n"
    + "  try {\n"
    + "    await loadFromBackend();\n"
    + "    setupYears();\n"
    + script_body
    + upload_handler
    + "  } catch (e) { console.error('init failed:', e); }\n"
    + "})();\n"
    + post
)

HTML.write_text(new_script, encoding="utf-8")
print("rewired index.html OK; sentinel:", SENTINEL)
