---
name: codex-spec-implementation
description: Spec-driven coding workflow for coderX agents. Use this skill whenever implementing, fixing, refactoring, or iterating code from hybrid docs or specified requirements, especially when file index, knowledge index, or evaluator findings are present.
---

# coderX: Spec-Driven Implementation Skill

## 目标

让 coderX 按统一流程执行开发：
- 先读规格与验收标准
- 再读工程文件索引与知识索引
- 再读审核报告并按优先级修复
- 最后提交可验证的代码改动

## 输入文档约定

优先读取上游明确交接或用户主动引用的文档；若无明确指定，则自动寻找正确的 `[功能模组]-hybrid.md` 文档。若没有主动引用且上下文中也无记载文档，coderX 依然被允许直接使用现有对话上下文继续操作。当存在明确的 hybrid 文档时，需重点关注其以下关键区块：
- `4` 核心功能与验收标准
- `5` 非功能性需求
- `7` 完成定义（DoD）
- `8.1` 工程文件索引与知识索引（主索引）
- `8.2` Memory Snapshot（关键约束）
- `8.3` 需求相关索引增量引用
- `9` 评估报告（Evaluator Reserved Section）
- `10` 迭代检查点（Incremental Checkpoints）— **由 orchestrator 自动管理，coderX 禁止修改此区块**

### Memory Snapshot 与知识图谱使用规范

- Hybrid 文档奉行“树干与树叶分离”原则：Markdown 文件内（如 `8.2`）只存“树干”（高阶需求结构与知识节点大纲/指针）。
- “树叶”（具体的代码逻辑关系、代码级上下文约束等详尽信息）完全存储在 `mcp/server-memory` 的节点（Nodes）中。
- coderX 在实现前，读取 `8.2` 获得所需的图谱节点大纲后，**必须主动通过 MCP Server 调用** 相关工具（如 `mcp_memory_open_nodes` 或 `mcp_memory_search_nodes`）去查询检索与当前实现任务直接关切的 Node 详情数据。不要期望 Markdown 里包含全部细节。

## 执行流程

### 第一步：需求对齐

1. 读取 `4/5/7`，提取本轮必须满足的功能点、验收标准和非功能约束。
2. 形成本轮任务清单，避免实现超出范围。

### 第二步：上下文定向加载（MCP 深度检索）

1. 先读 `8.1` 主索引，确认涉及的核心文件、模块、入口。
2. 读 `8.2` 获取核心架构的图谱大纲与引用节点。
3. **调用 MCP 图谱层检索**：基于获取到的大纲指针，使用 `mcp_memory_open_nodes` 或相关 MCP 工具精准检索出与你当前关心的模块相关的具体代码逻辑关系与约束，将其作为真实上下文。
4. 再读 `8.3` 增量索引，优先加载本轮变化相关上下文。

### 第三步：审核反馈处理（结合总线通信，条件执行）

1. **读取管道负载**：优先读取上游 evaluatorX 通过对话交接直接传递过来的“评估总结总线负载”，快速圈定本轮需要修复的核心问题与方向。
2. **对齐详细报告**：读取 hybrid 文档预留的 `9` 评估报告区块，获取具体的行号与代码级问题细节。
3. 若存在有效问题项：按严重度与优先级处理，顺序为 `P0/🔴 -> P1/🟡 -> P2/🟢`。
4. 若无有效问题项或为空：跳过审核修复流程，按规格直接往下完成新实现。

### 第四步：实现与验证

1. 仅修改与任务相关的最小文件集合，避免无关重构。
2. 对每项改动映射到验收标准，确保可验证。
3. 执行必要的构建/测试/静态检查，记录结果。

### 第五步：总线管道输出与交接 evaluator (Bus Pipeline Handoff)

实现完成后，不仅要维护 hybrid 文档与图谱快照，还**必须在调用任务完成或呼叫子智能体之前，在当前的对话上下文中主动输出一份标准化的"阶段成果总线负载 (Pipeline Payload)"**，供后续的 evaluatorX 定向读取审核。

> ⚠️ **格式强制要求**：orchestrator 会对本 Payload 进行结构化校验，校验不通过将被打回重写。请严格按照以下必填字段输出。

负载内容格式如下：

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

## 输出约束

1. 不得跳过规格读取直接编码。
2. 不得忽略 `8.1/8.3` 的索引上下文。
3. 对 `9` 的处理必须条件化：有内容则优先修复，无内容则跳过。
4. 不得虚构测试结果或需求完成状态。
5. 保持改动可追踪：每项改动都能回指到规格条目或评估问题。
6. 对图谱驱动改动保持可追踪：每项改动应能回指到 `8.2` 的节点或关系证据。
