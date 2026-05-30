# SciAcc · 科学边界 B<sub>t</sub> 演化可视化

把一个学科的论文集合**结构化为可演化的认知地图**——不只列出"这领域有哪些论文"，而是回答**这领域的对象 / 方法 / 证据 / 评价规则在哪一年长出哪一片新叶子**，以及**未来空白在哪个方位**。

```
B_t = ( D_t, M_t, E_t, V_t )
       └──┬──┘
          └─ D 对象域 / M 方法域 / E 证据域 / V 评价规则
             每一维都是一棵"系统发育树"（正交轴 → 生态位家族 → 具体叶子）
```

## 核心组件

| 模块 | 内容 |
|---|---|
| `Backend/` | FastAPI 后端 + PDF→文本→Claude API 抽 q/w→合并进 B_t 树的端到端流水线 |
| `Site/index.html` | 2D 列表式可视化，4 张维度卡片 + 时间轴 + 论文 q/w 详情 |
| `Site/index3d.html` | 3D 球形系统发育树（Three.js），可拖动查看四面体生长 |
| `Outputs/` | 唯一事实源：boundary_tree、papers_index、deltas、每篇 q.json + w.json |
| `Papers/` | 用户自己的 PDF（.gitignored，详见 [`Papers/README.md`](Papers/README.md)） |

## 数据 schema

详见 [`Outputs/prompt_boundary_tree.md`](Outputs/prompt_boundary_tree.md)，关键约束：

- 每个叶子带 `year` 与 `papers_introduced`，**只追加不删改**
- 同一生态位的"替代/扩展"通过 sibling-of 关系编码
- 演化通过 `Outputs/deltas.json` 按年记录 add / sibling-of / split

## 快速上手

```bash
# 1. 创建 Python 环境（pymupdf + anthropic SDK + fastapi）
uv venv .venv
.venv/bin/pip install -r Backend/requirements.txt

# 2. 配置 API key
cp Backend/.env.example Backend/.env
# 编辑 Backend/.env 填入 ANTHROPIC_API_KEY

# 3. 起后端（端口 8770，避免与其他项目冲突）
.venv/bin/python -m uvicorn Backend.main:app --port 8770

# 4. 浏览器打开
open Site/index3d.html  # 或 Site/index.html
```

## 核心 API

| 方法 | 路径 | 说明 |
|---|---|---|
| GET | `/api/papers` | 论文索引 + push_dimensions |
| GET | `/api/papers/{paper_id}` | 单篇 q + w + 推动维度 |
| GET | `/api/boundary-tree` | 完整 B_t 树（带 papers_introduced） |
| GET | `/api/deltas` | 按年份分层的演化日志 |
| POST | `/api/papers` | 上传 PDF → 端到端流水线（PyMuPDF → Claude → merge） |
| GET | `/api/tasks/{task_id}` | 流水线进度（pending → extracting → analyzing → merging → done/failed） |

## 当前进度（v1.0）

- ✅ 6 篇示例论文已分析入库（TDHNN / THNN / UniG-Encoder / IMVC_HG / HyperUFG / Self-supervised KT）
- ✅ 端到端流水线跑通（~26 秒/篇 Opus）
- ✅ 2D + 3D 双视图，时间轴动态推导年份
- ⚠️ 已知 bug：见 [`/Users/likun/.claude/plans/`](https://) 下的 v1.1 修复清单（路径穿越、并发竞争、API 错误处理等）
- ⏳ v1.5 计划：tree curation 编辑面板 + merge diff 预览 + 评估闭环

## 写作 / 引用

如果这套 B_t 框架对你的科研工作有用，欢迎引用 `FrontierScience.md` 中描述的方法学（这是我自己整理的"科学问题 P 与科学工作 W 的跨领域论文拆解研究"框架的工程实现）。

---

🤖 Built with [Claude Code](https://claude.com/claude-code)
