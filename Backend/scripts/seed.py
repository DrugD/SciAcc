"""One-shot data migration.

Idempotent. Re-running produces the same outputs:
  - Outputs/papers_index.json
  - Outputs/deltas.json
  - Outputs/question/<paper_id>.json (renamed/copied from 0X_*.json + push_dimensions)
  - Outputs/work/<paper_id>.json
  - Outputs/boundary_tree.json (each leaf gains papers_introduced)

Mapping comes from the previous turn's per-paper boundary analysis (D/M/E/V).
"""
from __future__ import annotations
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent))

from Backend import store

PROJECT_ROOT = store.PROJECT_ROOT
OUTPUTS = store.OUTPUTS

# ----- 5 papers, in chronological order -----
PAPERS_META = [
    {
        "paper_id": "TDHNN",
        "order": 1,
        "year": 2023,
        "title": "Totally Dynamic Hypergraph Neural Network",
        "venue": "IJCAI-23",
        "boundary_position": "边界迁移问题",
        "src_question": "02_Totally_Dynamic_Hypergraph_Neural_Network.json",
        "src_work": "02_Totally_Dynamic_Hypergraph_Neural_Network.json",
        "pdf_filename": "Totally Dynamic Hypergraph Neural Network.pdf",
        "push_dimensions": {
            "primary": ["M"],
            "secondary": ["D"],
            "summary": "主推 M_t（动态结构 + 离散采样数自适应）；次推 D_t（把 m 与 P(X_e|X_v) 抬升为学习对象）。",
            "multi_dim_link": "双维（D-M）",
        },
    },
    {
        "paper_id": "THNN",
        "order": 2,
        "year": 2024,
        "title": "Tensorized Hypergraph Neural Networks",
        "venue": "SIAM SDM 2024",
        "boundary_position": "边界迁移问题",
        "src_question": "01_Tensorized_Hypergraph_Neural_Networks.json",
        "src_work": "01_Tensorized_Hypergraph_Neural_Networks.json",
        "pdf_filename": "Tensorized Hypergraph Neural Networks.pdf",
        "push_dimensions": {
            "primary": ["M"],
            "secondary": ["D", "V"],
            "summary": "主推 M_t（张量代数 + 对称 CP 分解进入合法工具箱）；次推 D_t（m-均匀超图）、V_t（加入「阶数表达能力」判据）。",
            "multi_dim_link": "三维（D-M-V）",
        },
    },
    {
        "paper_id": "UniG-Encoder",
        "order": 3,
        "year": 2024,
        "title": "UniG-Encoder: A universal feature encoder for graph and hypergraph node classification",
        "venue": "Pattern Recognition 2024",
        "boundary_position": "边界迁移问题",
        "src_question": "03_UniG-Encoder.json",
        "src_work": "03_UniG-Encoder.json",
        "pdf_filename": "UniG-Encoder Auniversalfeatureencoderforgraphandhypergraphnode classification.pdf",
        "push_dimensions": {
            "primary": ["D", "M", "E", "V"],
            "secondary": [],
            "summary": "四维全推：把「图/超图 × 同质/异质」四象限合并为同一对象域，给出统一编码器，重写跨范式联合优越的成功标准。",
            "multi_dim_link": "四维全联动（D-M-E-V）",
        },
    },
    {
        "paper_id": "IMVC_HG",
        "order": 4,
        "year": 2025,
        "title": "Incomplete multi-view clustering based on hypergraph (IMVC_HG)",
        "venue": "Information Fusion 2025",
        "boundary_position": "边界内问题",
        "src_question": "04_IMVC_HG.json",
        "src_work": "04_IMVC_HG.json",
        "pdf_filename": "Unifying multimodalinteractions for rumordiffusion prediction with global hypergraphmodeling.pdf",
        "push_dimensions": {
            "primary": ["M"],
            "secondary": ["D"],
            "summary": "主推 M_t（超图重建 + ONMF + 张量 Schatten p-范数三组件整合为一步式优化）；次推 D_t（超图作为结构先验输出到不完备多视图聚类邻域）。",
            "multi_dim_link": "双维（D-M）",
        },
    },
    {
        "paper_id": "HyperUFG",
        "order": 5,
        "year": 2025,
        "title": "When Hypergraph Meets Heterophily: New Benchmark Datasets and Baseline (HyperUFG)",
        "venue": "AAAI-25",
        "boundary_position": "边界外问题",
        "src_question": "05_When_Hypergraph_Meets_Heterophily.json",
        "src_work": "05_When_Hypergraph_Meets_Heterophily.json",
        "pdf_filename": "When Hypergraph Meets Heterophily New Benchmark Datasets and Baseline.pdf",
        "push_dimensions": {
            "primary": ["D", "E"],
            "secondary": ["M", "V"],
            "summary": "主推 D_t（新开异质子域 + 新度量 Hedge/Hnode）和 E_t（新基准 + MLP 强制对照）；次推 M_t（framelet 双通道）和 V_t（「≥ MLP 底线」成功规则）。",
            "multi_dim_link": "四维全联动（D-M-E-V），以 D 与 E 最强",
        },
    },
]

# ----- Per-leaf attribution: which papers introduced each leaf in the existing tree -----
# Leaves are addressed by (dim, parent_path_tuple, label).
LEAF_PAPERS = {
    # ---- D ----
    ("D", ("对象域", "超图结构类型"), "静态超图 (V, E, H 给定)"): ["TDHNN"],
    ("D", ("对象域", "超图结构类型"), "动态超图 (H 可学)"): ["TDHNN"],
    ("D", ("对象域", "超图结构类型"), "m-均匀超图 (m 阶邻接张量 A^(m))"): ["THNN"],
    ("D", ("对象域", "超图结构类型"), "图 ∪ 超图 · 统一对象空间"): ["UniG-Encoder"],
    ("D", ("对象域", "同质性谱"), "同质超图 (默认假设)"): ["TDHNN", "THNN"],
    ("D", ("对象域", "同质性谱"), "异质超图 (HHL)"): ["HyperUFG"],
    ("D", ("对象域", "同质性谱", "异质超图 (HHL)"), "连续同质率 Hedge / Hnode"): ["HyperUFG"],
    ("D", ("对象域", "数据完备性"), "单视图 · 完备"): ["TDHNN", "THNN", "UniG-Encoder", "HyperUFG"],
    ("D", ("对象域", "数据完备性"), "多视图 · 随机缺失"): ["IMVC_HG"],
    ("D", ("对象域", "下游任务"), "节点 / 物体分类"): ["TDHNN", "THNN", "UniG-Encoder", "HyperUFG"],
    ("D", ("对象域", "下游任务"), "聚类"): ["IMVC_HG"],
    ("D", ("对象域", "下游任务"), "缺失视图重建"): ["IMVC_HG"],
    ("D", ("对象域", "现象 / 设定"), '"初始 H 不可信" 设定'): ["TDHNN"],
    ("D", ("对象域", "现象 / 设定"), '"MLP 能超 HGNN" 现象'): ["UniG-Encoder", "HyperUFG"],
    ("D", ("对象域", "现象 / 设定"), '超图作为 "缺失重建工具"'): ["IMVC_HG"],
    # ---- M ----
    ("M", ("方法域", "架构范式", "两阶段 MPNN (node↔edge↔node)"), "HGNN / HGNN+"): ["TDHNN"],
    ("M", ("方法域", "架构范式", "两阶段 MPNN (node↔edge↔node)"), "HNHN"): ["TDHNN"],
    ("M", ("方法域", "架构范式", "两阶段 MPNN (node↔edge↔node)"), "HyperGCN"): ["TDHNN"],
    ("M", ("方法域", "架构范式", "两阶段 MPNN (node↔edge↔node)"), "UniGNN 族 (UniGCN/UniGAT/UniSAGE/UniGCNII)"): ["UniG-Encoder", "HyperUFG"],
    ("M", ("方法域", "架构范式", "张量代数范式"), "m 阶邻接张量的对称 CP 分解"): ["THNN"],
    ("M", ("方法域", "架构范式", "张量代数范式"), "m 阶多项式回归视角 (HGNN = 2 阶特例)"): ["THNN"],
    ("M", ("方法域", "架构范式", "投影展开范式"), "归一化投影矩阵 P = [P_V; P_E]"): ["UniG-Encoder"],
    ("M", ("方法域", "架构范式", "投影展开范式"), "P^T 反投影聚合"): ["UniG-Encoder"],
    ("M", ("方法域", "架构范式", "投影展开范式"), "可学习 Line / Star 展开"): ["UniG-Encoder"],
    ("M", ("方法域", "架构范式", "简化主干范式 (替代两阶段 MPNN)"), "纯 MLP 主干"): ["UniG-Encoder"],
    ("M", ("方法域", "架构范式", "简化主干范式 (替代两阶段 MPNN)"), "Transformer 主干"): ["UniG-Encoder"],
    ("M", ("方法域", "结构学习策略"), "静态 H (给定)"): ["THNN", "UniG-Encoder", "HyperUFG"],
    ("M", ("方法域", "结构学习策略", "动态 H (可学)"), "连接权重重排 (经典 DHGNN 做法)"): ["TDHNN"],
    ("M", ("方法域", "结构学习策略", "动态 H (可学)"), "Reparameterized 超边采样"): ["TDHNN"],
    ("M", ("方法域", "结构学习策略", "动态 H (可学)"), "超边数量自适应 · 饱和率 S_H"): ["TDHNN"],
    ("M", ("方法域", "信号与滤波设计"), "单一低通 (默认 HGNN 卷积)"): ["TDHNN", "THNN", "UniG-Encoder"],
    ("M", ("方法域", "信号与滤波设计"), "低通 + 高通双通道 · Framelet"): ["HyperUFG"],
    ("M", ("方法域", "注意力机制"), "Transformer 风格双向 top-k 注意力"): ["TDHNN"],
    ("M", ("方法域", "约束与正则"), "监督 L_s (同类节点→同超边)"): ["TDHNN"],
    ("M", ("方法域", "约束与正则"), "无监督 L_u (同超边节点→相似特征)"): ["TDHNN"],
    ("M", ("方法域", "约束与正则"), "张量低秩约束 · Schatten p-范数"): ["IMVC_HG"],
    ("M", ("方法域", "联合优化 · 外部目标驱动"), "ONMF ≡ K-means 联合优化"): ["IMVC_HG"],
    ("M", ("方法域", "联合优化 · 外部目标驱动"), "超图 Laplacian 引导的缺失重建"): ["IMVC_HG"],
    ("M", ("方法域", "联合优化 · 外部目标驱动"), "外部任务目标 (聚类/重建) 驱动的超图学习"): ["IMVC_HG"],
    # ---- E ----
    ("E", ("证据域", "实证证据"), "真实基准精度 mean ± std"): ["TDHNN", "THNN", "UniG-Encoder", "IMVC_HG", "HyperUFG"],
    ("E", ("证据域", "实证证据", "受控合成探针"), "k-uniform (k=2..5) 阶数扫描"): ["THNN"],
    ("E", ("证据域", "实证证据", "受控合成探针"), "同质率扫描"): ["HyperUFG"],
    ("E", ("证据域", "实证证据"), "大规模统一比较 (18+ 基准)"): ["UniG-Encoder"],
    ("E", ("证据域", "理论证据", "退化一致性"), "THNN ⊃ HGNN (2 阶特例)"): ["THNN"],
    ("E", ("证据域", "理论证据", "退化一致性"), "2-uniform 度量 ⊃ 经典图同质率"): ["HyperUFG"],
    ("E", ("证据域", "理论证据"), "双射构造 (UniG Theorem 1)"): ["UniG-Encoder"],
    ("E", ("证据域", "理论证据"), "等价性推导 (ONMF ≡ K-means)"): ["IMVC_HG"],
    ("E", ("证据域", "鲁棒性证据"), "低训练比例扫描 (2%–44%)"): ["TDHNN"],
    ("E", ("证据域", "鲁棒性证据"), "不完备率扫描"): ["IMVC_HG"],
    ("E", ("证据域", "鲁棒性证据"), "跨 regime 稳定性"): ["UniG-Encoder", "HyperUFG"],
    ("E", ("证据域", "可复现与可检验"), "组件级 ablation"): ["TDHNN", "THNN", "IMVC_HG", "HyperUFG"],
    ("E", ("证据域", "可复现与可检验"), "超参灵敏度 (m, K, p, β, γ)"): ["TDHNN", "THNN", "IMVC_HG"],
    ("E", ("证据域", "可复现与可检验"), "公开 Repository + 数据"): ["HyperUFG"],
    ("E", ("证据域", "基准与度量作为证据"), "继承基准 (Cora/ModelNet40/NTU/CiteSeer/…)"): ["TDHNN", "THNN", "UniG-Encoder"],
    ("E", ("证据域", "基准与度量作为证据"), "新基准 HHL 集"): ["HyperUFG"],
    ("E", ("证据域", "基准与度量作为证据"), "新度量 Hedge / Hnode"): ["HyperUFG"],
    # ---- V ----
    ("V", ("评价规则", "精度性评价"), "≥ 2 代表基准超 SOTA"): ["TDHNN", "THNN", "UniG-Encoder", "IMVC_HG"],
    ("V", ("评价规则", "精度性评价"), "跨 regime 稳定性 > 单基准登顶"): ["UniG-Encoder", "HyperUFG"],
    ("V", ("评价规则", "结构性评价"), "组件消融不可或缺"): ["TDHNN", "IMVC_HG", "HyperUFG"],
    ("V", ("评价规则", "结构性评价"), "对抗 MLP baseline 不应被超越"): ["UniG-Encoder", "HyperUFG"],
    ("V", ("评价规则", "理论性评价"), "统一性理论本身构成贡献"): ["UniG-Encoder"],
    ("V", ("评价规则", "理论性评价"), "可退化到已有特例 (概念一致性)"): ["THNN", "HyperUFG"],
    ("V", ("评价规则", "范式性评价"), "新问题 + 新度量 + 新基准 + baseline 即完整贡献"): ["HyperUFG"],
    ("V", ("评价规则", "范式性评价"), "Baseline 定位合法"): ["HyperUFG"],
    ("V", ("评价规则", "工程性评价"), "简洁 / 可解释"): ["UniG-Encoder"],
    ("V", ("评价规则", "工程性评价"), "|E| ≫ |V| 计算友好"): ["UniG-Encoder"],
    ("V", ("评价规则", "工程性评价"), "端任务评价 > 中间指标"): ["IMVC_HG"],
}

# ----- delta entries derived from LEAF_PAPERS, grouped by year -----
SIBLING_OF = {
    # leaf -> the older leaf it explicitly replaces/extends
    "低通 + 高通双通道 · Framelet": "单一低通 (默认 HGNN 卷积)",
    "异质超图 (HHL)": "同质超图 (默认假设)",
    "纯 MLP 主干": "HGNN / HGNN+",
    "Transformer 主干": "HGNN / HGNN+",
    "m 阶邻接张量的对称 CP 分解": "HGNN / HGNN+",
}


def _walk_and_attribute(node: dict, dim: str, parent_path: tuple[str, ...]) -> None:
    """Annotate every leaf with papers_introduced based on LEAF_PAPERS."""
    children = node.get("children")
    if children:
        for c in children:
            label = c.get("label")
            sub_path = parent_path + (node["label"],) if node.get("label") else parent_path
            # if c has no children -> it's a leaf
            if not c.get("children"):
                key = (dim, sub_path, label)
                papers = LEAF_PAPERS.get(key)
                if papers is not None:
                    c["papers_introduced"] = list(papers)
            else:
                _walk_and_attribute(c, dim, sub_path)
                # also attribute the c node itself if it's listed (some entries
                # like "受控合成探针" carry a year and can be treated as leaf-ish)
                key = (dim, sub_path, label)
                papers = LEAF_PAPERS.get(key)
                if papers is not None:
                    c["papers_introduced"] = list(papers)


def annotate_boundary_tree() -> None:
    tree = store.read_boundary_tree()
    for dim in ("D", "M", "E", "V"):
        if dim not in tree:
            continue
        _walk_and_attribute(tree[dim], dim, parent_path=())
    store.write_boundary_tree(tree)


def write_per_paper_files() -> None:
    """Copy 0X_*.json -> {paper_id}.json and inject push_dimensions."""
    # Source files were originally produced as Outputs/question/0X_*.json and
    # Outputs/work/0X_*.json. After the first seed run we moved them to
    # Outputs/_archive/{question,work}/ to keep the live dirs deduplicated.
    # Look in both locations so the migration stays reproducible.
    candidates_q = [OUTPUTS / "_archive" / "question", OUTPUTS / "question"]
    candidates_w = [OUTPUTS / "_archive" / "work", OUTPUTS / "work"]
    for p in PAPERS_META:
        # question
        q_src = next((d / p["src_question"] for d in candidates_q if (d / p["src_question"]).exists()), None)
        if q_src is not None:
            q = json.loads(q_src.read_text(encoding="utf-8"))
            q["push_dimensions"] = p["push_dimensions"]
            store.write_question(p["paper_id"], q)
        # work
        w_src = next((d / p["src_work"] for d in candidates_w if (d / p["src_work"]).exists()), None)
        if w_src is not None:
            w = json.loads(w_src.read_text(encoding="utf-8"))
            w["push_dimensions"] = p["push_dimensions"]
            store.write_work(p["paper_id"], w)


def write_papers_index() -> None:
    papers = []
    for p in PAPERS_META:
        pdf_rel = f"Papers/{p['pdf_filename']}"
        entry = {
            "paper_id": p["paper_id"],
            "order": p["order"],
            "year": p["year"],
            "title": p["title"],
            "venue": p["venue"],
            "boundary_position": p["boundary_position"],
            "pdf_path": pdf_rel,
            "question_path": f"Outputs/question/{p['paper_id']}.json",
            "work_path": f"Outputs/work/{p['paper_id']}.json",
            "push_dimensions": p["push_dimensions"],
        }
        papers.append(entry)
    store.write_papers_index({"schema_version": "1.0", "papers": papers})


def write_deltas() -> None:
    """Generate delta records from LEAF_PAPERS:
    For each leaf, the year it was 'add'-ed = min year over its papers_introduced.
    """
    paper_year = {p["paper_id"]: p["year"] for p in PAPERS_META}
    deltas: dict[str, list[dict]] = {}
    for (dim, parent_path, label), papers in LEAF_PAPERS.items():
        years = sorted({paper_year[pid] for pid in papers if pid in paper_year})
        if not years:
            continue
        first_year = years[0]
        first_papers = sorted([pid for pid in papers if paper_year.get(pid) == first_year])
        op = "sibling-of" if label in SIBLING_OF else "add"
        delta = {
            "dim": dim,
            "path": list(parent_path[1:]) if parent_path and parent_path[0] in ("对象域", "方法域", "证据域", "评价规则") else list(parent_path),
            "item": label,
            "op": op,
            "papers": first_papers,
        }
        if op == "sibling-of":
            delta["sibling_of"] = SIBLING_OF[label]
        deltas.setdefault(str(first_year), []).append(delta)

        # subsequent years where the leaf got new contributors -> "merge" record (not a structural delta, skipped)
    # sort each bucket for stable output
    for y in deltas:
        deltas[y].sort(key=lambda d: (d["dim"], "/".join(d["path"]), d["item"]))
    store._write_json(store.DELTAS, deltas)


def main() -> None:
    print("[1/4] write per-paper q.json + w.json with push_dimensions")
    write_per_paper_files()
    print("[2/4] write papers_index.json")
    write_papers_index()
    print("[3/4] annotate boundary_tree.json with papers_introduced")
    annotate_boundary_tree()
    print("[4/4] write deltas.json")
    write_deltas()
    print("done.")


if __name__ == "__main__":
    main()
