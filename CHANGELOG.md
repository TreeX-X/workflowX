# 更新日志 (CHANGELOG)

本文件记录 WorkflowX 工作流框架的重大变更。

---

## [未发布] - 2025-07-07

### 1. 子智能体命名统一
- **变更位置**:
  - `.github/agents/` + `.codex/agents/` — 智能体文件重命名与 YAML name 字段统一
  - `.github/skills/` + `.codex/skills/` 中所有引用文件 — 引用名称同步更新
  - `README.md`、`README.en.md` — 文档中的智能体名称更新
- **内容**: 将所有子智能体名称统一为 `职责X` 命名规范（全小写 + X 后缀）：
  - `AbstracterX_x` → `abstracterX`（去除 `_x` 后缀，统一小写）
  - `codeX_x` → `codeX` → `coderX`（两阶段统一：先去后缀，再加 `r` 使职责更明确）
  - `plannerX_x` → `plannerX`（去除 `_x` 后缀）
  - 新增 `promptMasterX` 智能体
- **涉及范围**: 约 20+ 文件跨 `.github/` 和 `.codex/` 双镜像

### 2. Bus Pipeline Payload Schema
- **变更位置**:
  - `orchestratorX` (.github/agents + .codex/agents) — 主定义：两种 Payload 类型及校验规则
  - `codex-spec-implementation/SKILL.md` (.github/skills + .codex/skills) — coderX 侧输出模板
  - `evaluator-prd-audit/SKILL.md` (.github/skills + .codex/skills) — evaluatorX 侧输出模板
- **内容**: 为 `coderX ↔ evaluatorX` 总线通信定义结构化 Payload Schema：
  - **Payload Type 1 (coderX → evaluatorX)**：`已完成功能项`、`核心修改清单`、`提请定向审核点`、`关联Hybrid文档`、`覆盖写入要求`
  - **Payload Type 2 (evaluatorX → coderX)**：`核心审核范围`、`重点漏洞/驳回项`（🔴P0/🟡P1）、`评估结果`（仅 `PASS` | `需修复`）、`下一步行动建议`、`关联Hybrid文档`、`详细报告位置`
  - **校验规则**：orchestratorX 负责在转发前执行必填字段检查、评估结果合法性校验、核心修改清单非空校验、Hybrid 文档路径 `.md` 后缀校验。校验失败自动重试 1 次，仍不合格则停止并报告人类。

### 3. MCP Server 缺失降级策略
- **变更位置**: `orchestratorX` (.github/agents + .codex/agents)
- **内容**: 当 `mcp/server-memory` 或 `mcp/server-sequential-thinking` 不可用时，自动进入 `MCP_DEGRADED` 模式，跳过图谱操作并记录降级状态，避免阻塞主流程。

### 4. 回滚机制 (Checkpoint & Rollback)
- **变更位置**:
  - `orchestratorX` (.github/agents + .codex/agents) — 新增 `/rollback [编号]` 命令
  - `hybrid-template.md` (.github/skills/planner-prd-playbook + .codex/skills/planner-prd-playbook) — 新增 `10. 🔄 迭代检查点` 区块
  - `evaluator-prd-audit/SKILL.md` (.github/skills + .codex/skills) — 新增 Section 10 保护规则
  - `codex-spec-implementation/SKILL.md` (.github/skills + .codex/skills) — 新增 Section 10 输入文档约定
- **内容**: 每次迭代完成后在 hybrid 文档 `10.*` 区块写入检查点快照，支持通过 `/rollback [编号]` 命令回滚至指定检查点。

### 5. promptMasterX 跳过规则
- **变更位置**: `orchestratorX` (.github/agents + .codex/agents)
- **内容**: 当用户输入 ≤30 字符且包含明确的文件路径或函数名时，直接跳过 promptMasterX 预处理，将请求直达 coderX，减少不必要的智能体调度延迟。

### 6. Evaluator 增量评估模式
- **变更位置**:
  - `evaluator-prd-audit/SKILL.md` (.github/skills + .codex/skills) — 新增"第二步补充：评估模式判定"与增量模式规则
  - `hybrid-template.md` (.github/skills/planner-prd-playbook + .codex/skills/planner-prd-playbook) — 9.1 元信息新增 `evaluation_mode: full | incremental` 字段
- **内容**: 支持 `full`（全量评估）和 `incremental`（增量评估）两种模式。增量模式仅评估 Bus Payload 中声明的变更范围，提升评估效率。当增量评估中发现新的 P0 级问题时自动升级为全量模式。

### 7. 渐进式压缩机制 (Progressive Compression)
- **变更位置**:
  - `auto-compress-hybrid/SKILL.md` (.github/skills + .codex/skills) — 从单阈值(15KB/300行)重构为 L0-L3 四级渐进式压缩
  - `evaluatorX` (.github/agents + .codex/agents) — 阈值检测规则更新为引用渐进式等级
- **内容**: 将原来的单阈值"触发即压缩"策略升级为四级渐进式压缩：
  - **L0 健康** (< 10KB / < 200行): 无需压缩
  - **L1 轻量** (10~15KB / 200~300行): 仅索引去重 + 增量区精简 + 检查点归档
  - **L2 标准** (15~25KB / 300~500行): L1 + 知识条目提炼 + 图谱碎片清理
  - **L3 深度** (> 25KB / > 500行): L2 + 图谱宏观归并 + 静态区瘦身 + 检查点截断
- **验收标准**: 压缩等级判定准确、行数达标、无 DoD 丢失、压缩记录写入 9.1 元信息

---

> 以上变更均已在 `.github/` (GitHub Copilot) 和 `.codex/` (Codex CLI) 双镜像结构中同步应用。
