# Papers/

把要分析的论文 PDF 放在这个文件夹里。

## 怎么用

1. 把 PDF 文件拖进 `Papers/`（文件名用什么都行，建议短一点便于命令行操作）。
2. 通过两种方式喂给后端：
   - **网页上传**：打开 [`Site/index.html`](../Site/index.html) 或 [`Site/index3d.html`](../Site/index3d.html)，右上角"自动喂论文"区块选 PDF → 点"上传并分析（端到端）"。
   - **批量命令行**：
     ```bash
     .venv/bin/python Backend/scripts/batch_feed.py --concurrency 1
     # 或先跑 5 篇试水
     .venv/bin/python Backend/scripts/batch_feed.py --limit 5 --concurrency 1
     # 只补失败的
     .venv/bin/python Backend/scripts/batch_feed.py --retry-failed
     ```

## 为什么这个文件夹是空的

PDF 文件被 [`.gitignore`](../.gitignore) 排除：体积大、版权敏感，每个用户应放自己关心的论文。仓库只保留 `Papers/README.md` 维持目录结构。

## 流水线产出

- `Outputs/text/<paper_id>.txt` — PyMuPDF 抽取的纯文本
- `Outputs/question/<paper_id>.json` — 科学问题 q（背景/形式化/边界位置/所需证据）
- `Outputs/work/<paper_id>.json` — 科学工作 w（机制/对象/证据/评价/失败场景）
- `Outputs/papers_index.json` — 全局索引，含 push_dimensions（这篇论文主推 D/M/E/V 的哪几维）
- `Outputs/boundary_tree.json` — 累积的 B_t 边界树（每个叶子带 papers_introduced 反向引用）
- `Outputs/deltas.json` — 按年份分层的 add / sibling-of / split 历史

## 扫描型 PDF

如果某篇 PDF 是扫描件（PyMuPDF 抽不到文本，只有图片），流水线会标记为 `failed: extracted text < 200 chars`。该篇不会进入 `Outputs/`。需要 OCR 时手动跑：

```bash
.venv/bin/python render_thnn.py  # 把每页渲染成 PNG，再人工/Claude 多模态读
```
