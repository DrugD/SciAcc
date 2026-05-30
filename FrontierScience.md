# 科学工作何时构成科学贡献与科学边界突破

## 执行摘要

本文给出一个可操作的最终判据：**科学工作 $w$** 对科学的贡献，首先表现为它对某个科学问题 $q$ 的未决空间 $\Delta_q$ 的压缩、重组或验收标准 $\tau_q$ 的推进；而 **scientific-boundary breakthrough** 则是更强的情形：在一个回顾窗口 $h$ 内，$w$ 不仅推进了问题求解，还使边界状态

$$
B_t=(D_t,M_t,E_t,V_t,C_t)
$$

中的至少一个规范性分量 $D,M,E,V$ 发生了稳定改变，并通过了共同体采纳门槛 $C_t$。这里：

- $D_t$ 是合法对象域
- $M_t$ 是合法方法族
- $E_t$ 是合法证据标准
- $V_t$ 是合法评价准则
- $C_t$ 是实际承认并稳定该变化的共同体与制度配置

这个定义综合了以下理论传统：

- Kuhn：常规科学以 puzzle-solving 为主，异常可累积为危机
- Laudan：科学进步以问题求解有效性为核心
- Lakatos：进步性研究程序要求 novel facts 与 corroboration
- Gieryn：科学边界通过 boundary-work 被不断重画
- Ziman：科学主张的意义依赖共同体交流与公共批评

本文的最终类型学只保留四个**实质性**边界突破类型：

- **对象型（Object-break）**
- **方法型（Method-break）**
- **证据型（Evidence-break）**
- **评价型（Evaluation-break）**

我**不**把 $C_t$ 单列成第五种“实质性突破类型”，因为共同体配置的变化更适合作为**门槛条件与稳定化条件**：没有足够的共同体吸纳，再大的局部新奇也只是“候选突破”，而不是已经发生的边界突破，可以理解为随时间t变化的科学影响。


在操作化上，本文提出一套 0 到 100 的评分框架。先计算问题层面的

$$
\mathrm{SolveScore}
$$

再计算边界层面的四类分量分数

$$
ObjScore,\ MethScore,\ EvidScore,\ EvalScore
$$

以及共同体采纳分数

$$
AdoptScore.
$$

最终边界突破综合分数定义为

$$
\mathrm{BBS}
=
100\Bigl(
0.35\,\mathrm{SolveScore}
+
0.45\,\mathrm{ShiftScore}
+
0.20\,\mathrm{AdoptScore}
\Bigr),
$$

其中

$$
\mathrm{ShiftScore}
=
0.4\max\{ObjScore,MethScore,EvidScore,EvalScore\}
+
0.6\,\overline{S},
$$

$$
\overline{S}
=
\frac{
ObjScore+MethScore+EvidScore+EvalScore
}{4}.
$$

阈值建议如下：

- **High breakthrough**：$\mathrm{BBS}\ge 75$，$AdoptScore\ge 0.70$，且至少一个类型分数 $\ge 0.80$
- **Medium breakthrough**：$55\le \mathrm{BBS}<75$，$AdoptScore\ge 0.55$，且至少一个类型分数 $\ge 0.65$
- **Low breakthrough**：$40\le \mathrm{BBS}<55$，$AdoptScore\ge 0.40$，且至少一个类型分数 $\ge 0.50$
- 若 $AdoptScore<0.40$，则最多只能称为 **candidate boundary-break**，不能宣称边界已被真正改写

用这套框架回顾性编码三个典型案例，可得到：

- 广义相对论：$\mathrm{BBS}=85.1$
- DNA 双螺旋：$\mathrm{BBS}=81.1$
- CRISPR-Cas9：$\mathrm{BBS}=83.8$

三者都属于 High tier，但其**主突破类型**不同：

- 广义相对论：对象型主导，证据与评价辅助
- DNA 双螺旋：对象型主导，证据辅助
- CRISPR-Cas9：方法型主导，评价辅助

这一点表明：**边界突破不是单一形态，而是多型异构。**

---

## 理论基础与符号体系

理论上，本文使用以下五条主线作为理论底座：

- Kuhn 的《The Structure of Scientific Revolutions》
- Laudan 的《Progress and Its Problems》
- Lakatos 的《The Methodology of Scientific Research Programmes》
- Gieryn 1983 年的 boundary-work 论文
- Ziman 的《Real Science: What It Is and What It Means》

其核心思想分别是：

- Kuhn：normal science as puzzle-solving，以及异常—危机结构
- Laudan：科学进步系于 solved problems 与 anomalies
- Lakatos：progressive problemshift 必须带来 novel facts 并得到至少部分 corroboration
- Gieryn：边界改写是社会—制度性的 boundary-work
- Ziman：科学主张需要在共同体交流与公共批评中获得意义与稳定性

本文采用如下最小符号系统。

### 1. 边界状态

边界状态定义为：

$$
B_t=(D_t,M_t,E_t,V_t,C_t),
$$

其中：

- $D_t\subseteq\mathcal D$：时点 $t$ 被承认的对象域
- $M_t\subseteq\mathcal M$：合法方法族
- $E_t\subseteq\mathcal E$：合法证据形式与证据质量规则
- $V_t\subseteq\mathcal V$：合法评价与验收准则
- $C_t\subseteq\mathcal C$：实际执行这些规则并赋予其权威的共同体—制度配置

### 2. 科学问题

问题定义为：

$$
q=\langle u_q,\Delta_q,\tau_q,\rho_q,\pi_q\rangle,
$$

其中：

- $u_q$：未知对象或关系
- $\Delta_q$：竞争性未决空间
- $\tau_q$：问题的验收准则
- $\rho_q$：问题重要性
- $\pi_q$：其在边界中的位置

### 3. 科学工作

工作定义为：

$$
w=\langle q_w^{\mathrm{in}},m_w,e_w,r_w,s_w\rangle,
$$

其中：

- $q_w^{\mathrm{in}}$：其所回应的问题
- $m_w$：方法配置
- $e_w$：证据体
- $r_w$：结果与主张
- $s_w$：可复核状态（数据、材料、代码、仪器条件、同行可检验性等）

这个定义把“科学工作”从单纯论文文本改写成问题处理行动。

### 4. 更新关系

在这个系统里，工作 $w$ 的一般更新关系是：

$$
W:(B_t,Q_t)\mapsto(Q_{t+1},B_{t+h}),
$$

其中

$$
\Delta_q' = g(\Delta_q,e_w,r_w),
\qquad
\tau_q' = h(\tau_q,e_w,r_w).
$$

也就是说，工作首先更新问题：压缩未决空间、改变竞争假设的后验、或提高/重写验收要求；然后，只有在它造成 $D,M,E,V$ 的至少一个稳定变化并获得 $C$ 的吸纳时，才构成边界更新。这里的时滞 $h$ 是必要的，因为边界突破通常不是发表当日即可判断，而是经过一段时间的共同体吸纳过程之后才可确认。

---

## 最终边界突破类型学

本文的最终类型学为四型：对象型、方法型、证据型、评价型。其理由是：它们与 $B_t$ 的四个规范性分量 $D,M,E,V$ 一一对应；而 $C_t$ 虽然绝对关键，但更适合作为突破判成的门槛，而不是与前四型并列的“第五型”。

形式上，给定回顾窗口 $h$，定义四类突破判据如下。

### 1. 对象型突破

$$
\mathrm{ObjBreak}(w,t;h)
=
\mathbb{1}\Bigl[
\exists d^{\ast}\in D_{t+h}\setminus D_t,\ 
ObjScore(w,t;h)\ge \theta_O,\ 
AdoptScore(w,t;h)\ge \theta_A
\Bigr]
$$

### 2. 方法型突破

$$
\mathrm{MethBreak}(w,t;h)
=
\mathbb{1}\Bigl[
\exists m^{\ast}\in M_{t+h}\setminus M_t,\ 
MethScore(w,t;h)\ge \theta_M,\ 
AdoptScore(w,t;h)\ge \theta_A
\Bigr]
$$

### 3. 证据型突破

$$
\mathrm{EvidBreak}(w,t;h)
=
\mathbb{1}\Bigl[
\exists e^{\ast}\in E_{t+h}\setminus E_t,\ 
EvidScore(w,t;h)\ge \theta_E,\ 
AdoptScore(w,t;h)\ge \theta_A
\Bigr]
$$

### 4. 评价型突破

$$
\mathrm{EvalBreak}(w,t;h)
=
\mathbb{1}\Bigl[
\exists v^{\ast}\in V_{t+h}\setminus V_t,\ 
EvalScore(w,t;h)\ge \theta_V,\ 
AdoptScore(w,t;h)\ge \theta_A
\Bigr]
$$

同一工作可以同时触发多个类型，因此更自然的表示是：

$$
TypeVec(w)=\bigl(ObjScore,\ MethScore,\ EvidScore,\ EvalScore\bigr).
$$

### 类型定义表

| 类型 | 形式含义 | 直观解释 | 典型变化 |
|---|---|---|---|
| 对象型 Object-break | $D_{t+h}\setminus D_t\neq\varnothing$ | 新对象被承认为合法研究对象，或旧对象被重新本体化 | “什么东西算核心对象”被改写 |
| 方法型 Method-break | $M_{t+h}\setminus M_t\neq\varnothing$ | 新方法、平台、仪器进入主流方法族 | “用什么手段能做科学”被改写 |
| 证据型 Evidence-break | $E_{t+h}\setminus E_t\neq\varnothing$ | 新证据通道、新观测或新证据链被接受 | “什么证据算有效”被改写 |
| 评价型 Evaluation-break | $V_{t+h}\setminus V_t\neq\varnothing$ | 验收准则、终点、优劣标准被改写 | “什么算好解释、好结果、好试验”被改写 |

---

## 四类边界突破的典型实例

### 对象型突破案例

| 案例 | 主要变化 | $\Delta B$ 映射 | 为什么是对象型 |
|---|---|---|---|
| 广义相对论 | 引力从“背景空间中的力”转为“动力学时空几何” | $D,E,V,C$ | 时空曲率成为核心对象 |
| DNA 双螺旋 | “遗传信息的分子结构”成为生物学中心对象 | $D,E,C$ | 结构对象直接承载复制与信息传递 |
| 板块构造 | “运动的岩石圈板块”成为地球科学核心对象 | $D,E,V,C$ | 全球动力学对象替代静态大陆拼图 |
| H. pylori 与消化性溃疡 | 细菌进入原先以酸和压力解释的病因对象域 | $D,E,V,C$ | 病因对象从生理—心理框架转向感染因子 |

### 方法型突破案例

| 案例 | 主要变化 | $\Delta B$ 映射 | 为什么是方法型 |
|---|---|---|---|
| Bragg 的 X 射线晶体学 | 用 X 射线解析晶体结构的方法进入主流 | $M,E,C$ | 打开结构科学的仪器方法域 |
| Sanger 测序 | 快速、准确的链终止测序成为标准方法 | $M,E,C$ | 读出 DNA 序列成为常规操作 |
| PCR | 指定片段的指数扩增成为常规平台方法 | $M,C$ | 样本稀缺不再阻断分子分析 |
| CRISPR-Cas9 | 可编程、低门槛基因编辑进入主流 | $M,V,C$ | 基因编辑从小众工艺变为通用平台 |
| cryo-EM | 冷冻电镜把生物大分子三维成像推入新阶段 | $M,E,C$ | 原子级近似可视化成为现实 |

### 证据型突破案例

| 案例 | 主要变化 | $\Delta B$ 映射 | 为什么是证据型 |
|---|---|---|---|
| 1919 日食检验广义相对论 | 恒星光偏折成为检验引力理论的关键证据 | $E,V,C$ | 新观测直接区分竞争理论 |
| 磁条带与海底扩张 | 海洋磁异常成为板块运动的决定性证据链 | $E,D,C$ | 新证据把大陆漂移从猜想推向可检验理论 |
| DNA 的 X 射线衍射证据链 | 结构模型与衍射图样耦合为核心证据 | $E,D,C$ | 分子结构可从衍射证据稳定推出 |
| H. pylori 的因果证据链 | 组织学、培养、自体实验、抗生素根除形成闭环 | $E,D,V,C$ | 由相关性迈向因果与治疗验证 |
| LIGO 的引力波首次直接探测 | 时空扰动的直接探测成为新证据通道 | $E,D,C$ | 开启“引力波天文学” |

### 评价型突破案例

| 案例 | 主要变化 | $\Delta B$ 映射 | 为什么是评价型 |
|---|---|---|---|
| Koch’s postulates | 建立“病原体—疾病因果归属”的评价框架 | $V,E,C$ | 因果主张必须满足可重复的生物学标准 |
| MRC 1948 streptomycin trial | 随机对照成为治疗宣称的重要标准 | $V,E,C$ | 疗效评价从经验改为受控比较 |
| Evidence-Based Medicine | “best evidence” 成为临床决策核心评价原则 | $V,E,C$ | 评价标准从权威经验转向证据层级 |
| H. pylori 根除试验 | 溃疡治疗终点从缓解转向病原根除与持久治愈 | $V,E,D,C$ | “治好”被重新定义为因果源头的消除 |

---

## 量化评分框架

在量化上，本文区分**问题推进**与**边界位移**。Problem-solving 部分不应被简单的引文数替代；而 bibliometrics 可以作为采纳与传播的辅助代理，但不能取代结构性判断。

### 1. 问题推进分数

给定问题

$$
q=\langle u_q,\Delta_q,\tau_q,\rho_q,\pi_q\rangle,
$$

定义覆盖度：

$$
Cov(w,q)
=
\sum_{j=1}^{m}
\omega_j\,\mathbb{1}[c_j\in\tau_q\ \text{且被满足}],
\qquad
\sum_{j=1}^{m}\omega_j=1
$$

定义未决空间压缩度：

$$
Red_\Delta(w,q)
=
1-
\frac{
H\bigl(P(\Delta_q\mid e_w)\bigr)
}{
H\bigl(P(\Delta_q)\bigr)
}
$$

定义稳健性：

$$
Robustness(w)
=
0.4\,R_{ind}
+
0.3\,R_{ext}
+
0.3\,R_{time}
$$

其中：

- $R_{ind}$：独立证据来源的确认度
- $R_{ext}$：外部实验室或外部语境重现度
- $R_{time}$：结论在时间上的保持度

于是

$$
SolveScore(w,q)
=
0.4\,Cov
+
0.4\,Red_\Delta
+
0.2\,Robustness
$$

并定义：

$$
Solved(w,q)=\mathbb{1}[SolveScore\ge 0.75]
$$

$$
PartSolved(w,q)=\mathbb{1}[0.50\le SolveScore<0.75]
$$

### 2. 归一化函数

为保持跨领域可比性，所有子指标统一归一到区间 $[0,1]$。

计数型变量用截断对数归一化：

$$
N_{\log}(x;U)
=
\frac{
\log\bigl(1+\min(x,U)\bigr)
}{
\log(1+U)
}
$$

比例型变量直接截断到 $[0,1]$。  
分布型变量用标准熵归一化：

$$
H^{\ast}(p_1,\dots,p_F)
=
\frac{
-\sum_{f=1}^{F} p_f\log p_f
}{
\log F
}
$$

### 3. 四类边界分量分数

#### 对象型分数

$$
ObjScore
=
0.40\,D_{new}
+
0.35\,D_{reont}
+
0.25\,Q_{expand}
$$

其中：

- $D_{new}$：新对象术语或对象类是否进入核心文献与教科书
- $D_{reont}$：旧对象是否被降格为新本体中的特例或极限
- $Q_{expand}$：以新对象为中心的可承认问题簇增长

#### 方法型分数

$$
MethScore
=
0.30\,M_{legit}
+
0.25\,M_{reach}
+
0.25\,M_{perf}
+
0.20\,M_{reuse}
$$

其中：

- $M_{legit}$：方法合法化程度
- $M_{reach}$：新方法打开的新问题范围
- $M_{perf}$：在吞吐量、分辨率、成本上的标准化提升
- $M_{reuse}$：跨实验室、跨学科复用度

#### 证据型分数

$$
EvidScore
=
0.25\,E_{channel}
+
0.30\,E_{disc}
+
0.25\,E_{indep}
+
0.20\,E_{prov}
$$

其中：

- $E_{channel}$：是否出现新证据通道
- $E_{disc}$：区分竞争假设的能力，可直接用 $Red_\Delta$ 或其近似
- $E_{indep}$：独立证据链数量与多样性
- $E_{prov}$：可追溯性、仪器与数据透明度、误差控制

#### 评价型分数

$$
EvalScore
=
0.30\,V_{crit}
+
0.25\,V_{cod}
+
0.20\,V_{bench}
+
0.25\,V_{replace}
$$

其中：

- $V_{crit}$：是否出现新的验收准则、终点、准入标准
- $V_{cod}$：是否被指南、教材、评审标准、方法学文章编码
- $V_{bench}$：是否进入正式 benchmark 或规范程序
- $V_{replace}$：旧标准是否被降格为不足条件，或仅为必要非充分条件

### 4. 共同体采纳分数

$$
AdoptScore
=
0.30\,C_{field}
+
0.20\,C_{cross}
+
0.25\,C_{canon}
+
0.25\,C_{rep}
$$

其中：

- $C_{field}$：领域归一化影响的百分位或 RCR 百分位近似
- $C_{cross}$：跨学科扩散熵近似
- $C_{canon}$：教材、指南、奖项、标准课程等经典化信号
- $C_{rep}$：独立复现或独立实现的数量与质量

### 5. 边界位移汇总分数

$$
\overline{S}
=
\frac{
ObjScore+MethScore+EvidScore+EvalScore
}{4}
$$

$$
ShiftScore
=
0.4\cdot\max\{ObjScore,MethScore,EvidScore,EvalScore\}
+
0.6\cdot\overline{S}
$$

采用“最大值 + 均值”的混合，而不是简单平均，理由是：很多历史性突破有一个主导类型，但真正大的边界突破通常又不会只改变一个分量。

### 6. 综合突破分数

$$
BBS
=
100\Bigl(
0.35\,SolveScore
+
0.45\,ShiftScore
+
0.20\,AdoptScore
\Bigr)
$$

### 7. 分级阈值

| 层级 | 条件 |
|---|---|
| High breakthrough | $BBS\ge 75$，$AdoptScore\ge 0.70$，且 $\max\{Obj,Meth,Evid,Eval\}\ge 0.80$ |
| Medium breakthrough | $55\le BBS<75$，$AdoptScore\ge 0.55$，且主类型分数 $\ge 0.65$ |
| Low breakthrough | $40\le BBS<55$，$AdoptScore\ge 0.40$，且主类型分数 $\ge 0.50$ |
| Candidate only | $AdoptScore<0.40$，无论分数多高都不宣称“边界已突破” |

同时定义“普通科学贡献”：

$$
Contrib(w,q,t)
=
\mathbb{1}\Bigl[
SolveScore\ge 0.50
\ \lor\
\max\{ObjScore,MethScore,EvidScore,EvalScore\}\ge 0.50
\Bigr]
$$

如果

$$
Contrib=1,\qquad BBS<40,
$$

那么它是**重要但仍在边界内**的贡献。  
如果

$$
BBS\ge 40
\quad\text{但}\quad
AdoptScore<0.40,
$$

那么它是**高潜边界候选**。  
只有在经过采纳门槛之后，才改判为真正突破。

---

## 历史案例映射与算例

### 广义相对论

回顾性编码窗口取 1915 到 1930。

给出一组保守输入：

$$
Cov=0.90,\qquad
Red_\Delta=0.85,\qquad
Robustness=0.80
$$

$$
ObjScore=0.95,\qquad
MethScore=0.45,\qquad
EvidScore=0.80,\qquad
EvalScore=0.75,\qquad
AdoptScore=0.90
$$

于是：

$$
SolveScore
=
0.4(0.90)+0.4(0.85)+0.2(0.80)
=
0.86
$$

$$
\overline{S}
=
\frac{0.95+0.45+0.80+0.75}{4}
=
0.7375
$$

$$
ShiftScore
=
0.4(0.95)+0.6(0.7375)
=
0.8225
$$

$$
BBS
=
100\Bigl(
0.35\times 0.86
+
0.45\times 0.8225
+
0.20\times 0.90
\Bigr)
=
85.1
$$

判定：**High breakthrough**。  
主类型为对象型，证据型和评价型为强辅助型。

### DNA 双螺旋

回顾性编码窗口取 1953 到 1965。

给出保守输入：

$$
Cov=0.85,\qquad
Red_\Delta=0.80,\qquad
Robustness=0.80
$$

$$
ObjScore=0.90,\qquad
MethScore=0.30,\qquad
EvidScore=0.75,\qquad
EvalScore=0.60,\qquad
AdoptScore=0.95
$$

计算得：

$$
SolveScore
=
0.4(0.85)+0.4(0.80)+0.2(0.80)
=
0.82
$$

$$
\overline{S}
=
\frac{0.90+0.30+0.75+0.60}{4}
=
0.6375
$$

$$
ShiftScore
=
0.4(0.90)+0.6(0.6375)
=
0.7425
$$

$$
BBS
=
100\Bigl(
0.35\times 0.82
+
0.45\times 0.7425
+
0.20\times 0.95
\Bigr)
=
81.1
$$

判定：**High breakthrough**。  
主类型为对象型，证据型为辅助型。

### CRISPR-Cas9

回顾性编码窗口取 2012 到 2024。

给出输入：

$$
Cov=0.95,\qquad
Red_\Delta=0.90,\qquad
Robustness=0.90
$$

$$
ObjScore=0.20,\qquad
MethScore=0.95,\qquad
EvidScore=0.55,\qquad
EvalScore=0.50,\qquad
AdoptScore=0.98
$$

计算得：

$$
SolveScore
=
0.4(0.95)+0.4(0.90)+0.2(0.90)
=
0.92
$$

$$
\overline{S}
=
\frac{0.20+0.95+0.55+0.50}{4}
=
0.55
$$

$$
ShiftScore
=
0.4(0.95)+0.6(0.55)
=
0.71
$$

$$
BBS
=
100\Bigl(
0.35\times 0.92
+
0.45\times 0.71
+
0.20\times 0.98
\Bigr)
=
83.8
$$

判定：**High breakthrough**。  
主类型为方法型，评价型为次级辅助型。

### 三例汇总表

| 案例 | SolveScore | Obj | Meth | Evid | Eval | Adopt | ShiftScore | BBS | 层级 | 主类型 |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---|---|
| 广义相对论 | 0.86 | 0.95 | 0.45 | 0.80 | 0.75 | 0.90 | 0.8225 | 85.1 | High | 对象型 |
| DNA 双螺旋 | 0.82 | 0.90 | 0.30 | 0.75 | 0.60 | 0.95 | 0.7425 | 81.1 | High | 对象型 |
| CRISPR-Cas9 | 0.92 | 0.20 | 0.95 | 0.55 | 0.50 | 0.98 | 0.7100 | 83.8 | High | 方法型 |

这三例分别说明：**高分突破并不要求四项类型分数都高；它要求的是至少一个主类型极强、问题推进显著，并通过了共同体采纳门槛。**

---

## 自动化实现、敏感性与局限

### 1. 自动化实现

自动化实现可以分成四层。

#### 文本挖掘

从标题、摘要、引言、方法、结论中抽取对象词、方法词、证据词、评价词，并利用时间切片嵌入、topic burst、concept centrality 识别 $D,M,E,V$ 的变动。

典型语言信号例如：

- 对象型：`X is the cause/structure/field/object of ...`
- 方法型：`method / assay / protocol / platform / system`
- 证据型：`direct detection / randomised / controlled / blinded / observational evidence`
- 评价型：`criterion / endpoint / benchmark / gold standard / guideline / postulate / consensus`

#### 引文网络

用 OpenAlex、Crossref、PubMed 等构建：

- field-normalized uptake
- 跨学科扩散熵
- co-citation network
- RCR 等采纳代理

#### 复现与独立验证

通过显式 replication、validation 语句、系统综述、meta-analysis、独立实验室重复、或方法在多种物种、材料、仪器上的独立实现来估计 $R_{ind},R_{ext},C_{rep}$。

#### 经典化信号

教材、指南、Nobel 或其他重大奖项、标准课程、基金与期刊审稿要求都可作为 $C_{canon}$ 或 $V_{cod}$ 的代理。

### 2. Provenance 设计

建议每一次评分都保存

$$
\Pi(w)
=
\langle
h,\ 
\mathcal S_{docs},\ 
\mathcal S_{net},\ 
\text{field schema},\ 
\text{coder/version},\ 
\text{timestamp}
\rangle
$$

其中：

- $h$：回顾窗口
- $\mathcal S_{docs}$：原始文献与证据片段集合
- $\mathcal S_{net}$：引文、共引、复现网络快照
- field schema：学科校准方案
- coder/version：编码与版本信息
- timestamp：时间戳

原因很简单：边界突破的断言天然带有历史依赖与共同体依赖。如果不记录时窗、归一化基线与证据来源，评分就不可复查，也无法比较“早期候选突破”和“晚期已稳定突破”。

### 3. 敏感性

最关键的不是 $Obj/Meth/Evid/Eval$ 的细小权重，而是：

- **Adopt 门槛**
- **回顾窗口 $h$**

例如，某些工作在对象层面很强，但若共同体尚未吸纳，就只能算 candidate；窗口拉长后才可能升级为正式边界突破。

### 4. 局限

局限主要有五点：

1. **归因问题**：很多边界突破不是单篇论文，而是 work cluster  
2. **回顾性偏差**：经典案例容易被后见之明放大  
3. **学科差异**：不同学科的 $V$ 和阈值不同，应做 field-calibrated 处理  
4. **计量偏差**：RCR、disruption、引文数、扩散熵都只是代理，不等于突破本身  
5. **共同体政治性**：边界并非纯理性事实线，而是利益、权威、职业身份与制度秩序共同塑造的结果  

---

## 最小可执行判据

综上，本文给出的最小可执行判据可以压缩成三行：

$$
SolveScore
=
0.4\,Cov
+
0.4\,Red_\Delta
+
0.2\,Robustness
$$

$$
ShiftScore
=
0.4\max\{Obj,Meth,Evid,Eval\}
+
0.6\cdot
\frac{Obj+Meth+Evid+Eval}{4}
$$

$$
BoundaryBreak(w)
=
\mathbb{1}\bigl[
BBS\ge \theta_B
\ \land\
AdoptScore\ge \theta_A
\bigr]
$$

其含义是：

**科学贡献先看它如何推进问题；边界突破再看它是否改变了对象、方法、证据或评价中的至少一项，并被共同体稳定吸纳。**

这既能解释为什么爱因斯坦相对论相对于牛顿力学属于高阶对象—证据—评价复合突破，也能解释为什么 DNA 双螺旋与 CRISPR-Cas9 分别是对象主导型与方法主导型的高阶突破。

---

## 参考文献（纯文本）

1. Kuhn, Thomas S. *The Structure of Scientific Revolutions*. University of Chicago Press.
2. Laudan, Larry. *Progress and Its Problems*. University of California Press.
3. Lakatos, Imre. *The Methodology of Scientific Research Programmes*. Cambridge University Press.
4. Gieryn, Thomas F. “Boundary-Work and the Demarcation of Science from Non-Science.” *American Sociological Review*, 1983.
5. Ziman, John. *Real Science: What It Is and What It Means*. Cambridge University Press.
6. Einstein, Albert. 1915–1916 papers on general relativity.
7. Watson, James D., and Francis H. C. Crick. “A Structure for Deoxyribose Nucleic Acid.” *Nature*, 1953.
8. Jinek, Martin, et al. “A Programmable Dual-RNA-Guided DNA Endonuclease in Adaptive Bacterial Immunity.” *Science*, 2012.
9. Marshall, Barry J., and J. Robin Warren. “Unidentified Curved Bacilli in the Stomach of Patients with Gastritis and Peptic Ulceration.” *The Lancet*, 1984.
10. Saiki, R. K., et al. “Enzymatic Amplification of Beta-Globin Genomic Sequences and Restriction Site Analysis for Diagnosis of Sickle Cell Anemia.” *Science*, 1985.
11. Vine, F. J., and D. H. Matthews. “Magnetic Anomalies over Oceanic Ridges.” *Nature*, 1963.
12. Hutchins, B. I., et al. “Relative Citation Ratio (RCR): A New Metric That Uses Citation Rates to Measure Influence at the Article Level.” *PLOS Biology*, 2016.
13. Hicks, Diana, et al. “Bibliometrics: The Leiden Manifesto for Research Metrics.” *Nature*, 2015.