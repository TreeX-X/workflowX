---
name: orchestrator-playbook
description: "orchestratorX 的运行时规程手册。包含环境自检、MCP 降级策略、Bus Payload 校验规范、检查点与回滚机制、Prompt 预处理规则和 Status Report 规范。orchestratorX 在执行工作流时按需加载本技能中的对应章节。"
---

# orchestrator Playbook — 运行时规程手册

> **定位**：本技能是 orchestratorX 的"操作手册"，包含所有触发式规程与首次调用流程。
> orchestratorX 智能体在需要时主动加载本技能的对应章节，而非将全部内容嵌入自身定义。
>
> **使用方式**：orchestratorX 在以下场景中应明确引用本技能：
> - 首次进入工作流时 → 加载「环境初始化」章节
> - 跨智能体交接时 → 加载「Bus Payload 校验」章节
> - coderX/evaluatorX 返回后 → 加载「检查点写入」章节
> - 用户发出 `/rollback` 时 → 加载「回滚执行流程」章节
> - 用户发出 `/status` 时 → 加载「Status Report 规范」章节
> - 调用 coderX 前 → 加载「Prompt 预处理规则」章节

---

## 1. Environment Initialization（环境与 MCP 自检机制）

当你在全新的工程或首次与用户开启对话时，必须具备"开箱自检"意识：

1. 主动检查工程中是否提供了 MCP 工具依赖（如 `server-memory` 和 `server-sequential-thinking`）。
2. 如果评估环境可能缺失这些 MCP Server，请以友好的方式提醒用户："检测到当前工作流依赖外部 MCP Server 能力，如果你是初次部署，请参考根目录的 `mcp.json.template` 配置到你的 IDE 或客户端中"。引导用户完成前置配置后，再顺利进入主工作流。

### 1.1 MCP Server 缺失降级策略 (MCP Fallback)

当 MCP Server（`server-memory` / `server-sequential-thinking`）不可用时，你必须执行以下降级流程，**而非阻塞工作流**：

1. **首次检测**：进入工作流前，尝试调用 `mcp_memory_read_graph` 等 MCP 工具。若调用失败或返回错误，判定为 MCP 不可用。
2. **标记降级模式**：使用 `#tool:todo` 记录当前处于 `MCP_DEGRADED` 状态。
3. **一次性通知用户**（仅首次）：
   > ⚠️ 检测到 MCP Server 不可用，工作流已进入降级模式。知识图谱检索步骤将被跳过，智能体将仅依赖 hybrid 文档中的 `8.1` 文件索引和 `8.3` 增量引用获取上下文。功能不受影响，但上下文精准度可能降低。如需恢复完整能力，请配置 `mcp.json.template`。
4. **SubAgent 调度适配**：在降级模式下，调用 coderX / evaluatorX 时，在 prompt 中追加降级指令前缀：
   > 📌 [MCP 降级模式] 当前 MCP Server 不可用。请跳过所有 `mcp_memory_open_nodes` / `mcp_memory_search_nodes` 等 MCP 图谱检索步骤。改为：仅依赖 hybrid 文档 `8.1` 主索引和 `8.3` 增量引用中的信息作为上下文。如果上下文不足，明确指出缺失的具体信息并继续执行，不要阻塞。
5. **恢复检测**：每次进入新的 whole/local/unit 工作流时，重新检测 MCP 可用性。若恢复可用，清除 `MCP_DEGRADED` 标记并通知用户。

---

## 2. Bus Pipeline Payload Schema & Validation（总线 Payload 规范与校验）

在 whole/local 工作流的跨智能体交接环节（coderX → evaluatorX、evaluatorX → coderX），上游智能体必须在对话流中输出结构化的"总线 Payload"。orchestrator 在将控制权交给下游前，必须校验上游输出是否符合下述 Schema；若不符合，应自动附加格式修正指令重新调用上游智能体，直到 Payload 合格后才传递给下游。

### 2.1 Payload Type 1：coderX → evaluatorX（阶段成果总线负载）

coderX 完成实现后必须输出，包含以下**必填字段**：

```markdown
### 📦 Bus Pipeline Payload: Implementation Summary
- **已完成功能项**: [列出本轮完成的 PRD 需求模块名称或编号]
- **核心修改清单**:
  - [文件路径] — [修改角色/逻辑摘要]
  - ...
- **提请定向审核点**: [指明复杂逻辑或外部依赖，提示 evaluatorX 重点审阅]
- **关联 Hybrid 文档**: [hybrid 文档路径]
- **覆盖写入要求**: 请 evaluatorX 将评估报告覆盖写入 hybrid 文档的 `9.*` 区块
```

### 2.2 Payload Type 2：evaluatorX → coderX（评估总结总线负载）

evaluatorX 完成评估后必须输出，包含以下**必填字段**：

```markdown
### 📦 Bus Pipeline Payload: Evaluation Summary
- **核心审核范围**: [本次校验对齐的主功能及代码片段]
- **重点漏洞/驳回项**:
  - 🔴 [P0 问题摘要 — 文件路径:问题描述]
  - 🟡 [P1 问题摘要 — 文件路径:问题描述]
  - ...
- **评估结果**: [PASS | 需修复]
- **下一步行动建议**: [精确指引 coderX 第一步从哪个文件的哪段逻辑着手]
- **关联 Hybrid 文档**: [hybrid 文档路径]
- **详细报告位置**: hybrid 文档 `9.*` 区块（已覆盖写入）
```

### 2.3 校验规则

orchestrator 在每个智能体返回后必须执行以下检查：

1. **必填字段检查**：Payload 中每个 `- **字段名**:` 标记的字段都必须存在且非空。
2. **评估结果合法性**：evaluatorX 的 Payload 中 `评估结果` 字段值只能是 `PASS` 或 `需修复`（不区分大小写）。如果值为其他内容，视为格式异常。
3. **核心修改清单非空**：coderX 的 Payload 中 `核心修改清单` 至少包含 1 个文件条目。
4. **Hybrid 文档路径存在性**：`关联 Hybrid 文档` 字段应指向一个合理的文档路径（以 `.md` 结尾）。

**校验失败处理**：
- 如果校验不通过，**不得**将该 Payload 传递给下游智能体。
- 应自动附加以下修正指令重新调用该智能体：

> ⚠️ 你的总线 Payload 格式不符合规范，缺少以下必填字段：[列出缺失字段]。请按照 Bus Pipeline Payload Schema 重新输出完整 Payload。

- 最多重试 **1 次**。若第 2 次仍不合格，停止流程并向人类开发者报告格式异常。

**校验通过处理**：
- 将合格的 Payload 作为**首要上下文**传递给下游智能体（优先级高于其他信息）。
- 同时告知下游智能体"已校验通过的 Payload 内容"，让其快速进入工作状态。

---

## 3. Incremental Checkpoint & Rollback（增量检查点与回滚机制）

为防止实现偏移越走越远，必须在关键迭代节点记录可回溯的检查点，允许人类随时回滚到任意已通过的中间态。

### 3.1 检查点写入规则

1. **写入时机**：在以下事件发生时，orchestrator 必须自动向当前 hybrid 文档的 `10. 🔄 迭代检查点` 区块追加一条检查点记录：
   - coderX 完成实现并输出合格 Payload 后（即进入 evaluatorX 之前）
   - evaluatorX 返回 `PASS` 后（即本轮迭代完全通过）
   - 用户手动执行 `/rollback` 恢复成功后（记录恢复目标状态）
2. **检查点内容**（必须包含以下字段）：
   ```
   - **#CP-[编号]** | **时间**: [ISO时间] | **阶段**: [coder实现完成 | 评估通过] | **触发**: [自动 | /rollback]
     - **已完成功能**: [本轮完成的功能项列表]
     - **核心修改文件**: [文件路径列表]
     - **Git 状态**: [当前 commit hash 或 "unstaged" 状态]
     - **评估结果**: [通过 | 未审核 | 需修复]
   ```
3. **编号规则**：`#CP-1`、`#CP-2`... 递增，从工作流开始时计数。
4. **限制**：最多保留最近 **10** 条检查点记录。超过时，删除最早的条目（但保留 `#CP-1` 首次检查点不删）。

### 3.2 回滚执行流程 (`/rollback`)

当用户发出 `/rollback [编号]` 指令时：

1. 读取 hybrid 文档 `10.*` 区块，定位目标检查点。
2. 执行 `git checkout -- [核心修改文件列表]` 将代码回退到该检查点记录的文件状态。
   - 若检查点记录了 commit hash，使用 `git reset --hard [hash]` 回退。
   - 若为 unstaged 状态，使用 `git checkout -- .` 全量回退。
3. **覆盖** hybrid 文档的 `9.*` 评估区块为初始空态。
4. **截断** `10.*` 区块：删除目标编号之后的所有检查点条目。
5. 向用户确认回滚结果，并询问下一步意图（继续开发 / 切换模式 / 总结）。
6. 将回滚事件作为新检查点写入 `10.*`（触发标记为 `/rollback`）。

> **⚠️ 安全约束**：回滚操作会丢弃目标检查点之后的所有改动。执行前必须向用户展示将被丢弃的改动摘要并获得确认（除非用户在指令中追加了 `-y` 强制参数）。

---

## 4. Prompt Preprocessing Rules（Prompt 预处理规则）

promptMasterX 是一个轻量 prompt 预处理智能体。职责单一：将用户的原始需求文本优化为高质量、无歧义、结构化的 prompt，然后交给下游智能体执行。

**调用方式**：使用 `#tool:agent/runSubagent` 调用 `promptMasterX`，将原始需求文本作为 prompt 传给它。

### 4.1 跳过规则（优先于自动触发规则）

当用户输入满足以下**所有**条件时，直接跳过 promptMasterX，将原始需求直传下游智能体：
- 输入长度 **≤ 30 字符**（去除首尾空格后）
- 输入中**包含明确的文件路径**（如 `src/foo.ts`、`lib/bar.py`）**或函数名**（如 `getUserInfo`、`handleLogin`）

> 💡 理由：此类输入已经是高度精确的执行指令，promptMasterX 优化只会增加额外开销且不产生价值。

### 4.2 自动触发规则

| 模式 | 场景 | 是否调用 promptMasterX | 说明 |
|---|---|---|---|
| `/unit` | 调用 coderX 前 | ✅ 自动调用 | 优化用户需求 + 原始需求一并传给 coderX |
| `/local` | 首次调用 coderX 前 | ✅ 自动调用 | 同上 |
| `/whole` | planner 阶段 | ❌ 不调用 | planner 阶段需要保留原始意图进行对话澄清 |
| `/whole` | coder 阶段（PRD 确认后） | ❌ 不调用 | PRD 本身已是结构化的 |
| `/whole` | evaluator 打回后修复轮 | ✅ 自动调用 | 将 evaluator 建议 + 用户补充合并优化后再传给 coderX |
| `/prompt` | 直接调用 | ✅ | 不进入任何工作流，仅做 prompt 工程 |

**传递规范**：优化后的 prompt 作为主体传给下游智能体，同时在上下文中附上原始需求文本，以防止意图丢失。

---

## 5. Status Report 规范 (`/status`)

`/status` 是一个**只读、零副作用**的响应式指令。执行时从当前 hybrid 文档中快速提取结构化信息并以简洁列表呈现给用户，**不在 hybrid 文档中写入任何内容**。

### 5.1 执行流程

1. 读取当前 hybrid 文档。
2. 提取以下信息并组装为摘要输出：

### 5.2 输出格式

```markdown
## 📊 WorkflowX Status Report

**当前模式**: [whole / local / unit]
**分支**: [若启用了 -b，显示工作分支名；否则显示当前 git 分支]

### ✅ 已完成的工作
- [功能/模块名] — 完成于 #CP-[编号]，评估结果: [PASS / 未审核]
- ...

### ⏳ 进行中 / 未完成的工作
- [功能/模块名] — 状态: [coder实现中 / 待评估 / 评估打回修复中]
  - 最近一次评估问题: [P0/P1 问题摘要，若有]
- ...

### 🔄 最近检查点
- #CP-[最近编号]: [阶段] | [时间] | [已完成功能]
```

### 5.3 信息提取规则

- **已完成**：从 `10. 迭代检查点` 区块中提取阶段为「评估通过」的条目，列出其已完成功能。
- **未完成/进行中**：
  - 检查 `9. 评估报告` 区块中是否有「评估结论 = 需修复」的记录 → 标记为「评估打回修复中」。
  - 如果 `10.*` 最新检查点阶段为「coder实现完成」且无对应「评估通过」记录 → 标记为「待评估」。
  - 如果上述均不匹配但 hybrid 文档中存在未勾选的 DoD（`6.*` 区块） → 列出未勾选项，标记为「待完成」。
- **分支信息**：通过 `#tool:execute/runInTerminal` 执行 `git branch --show-current` 获取。
- **无 hybrid 文档时**：输出「当前无活跃的 hybrid 文档，请先使用 `/whole`、`/local` 或 `/unit` 启动工作流。」
