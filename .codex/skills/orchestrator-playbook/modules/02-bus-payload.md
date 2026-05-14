# 2. Bus Pipeline Payload Schema & Validation（总线 Payload 规范与校验）

在 whole/local 工作流的跨智能体交接环节（coderX → evaluatorX、evaluatorX → coderX），上游智能体必须在对话流中输出结构化的"总线 Payload"。orchestrator 在将控制权交给下游前，必须校验上游输出是否符合下述 Schema；若不符合，应自动附加格式修正指令重新调用上游智能体，直到 Payload 合格后才传递给下游。

## 2.1 Payload Type 1：coderX → evaluatorX（阶段成果总线负载）

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
- **Task ID**（并行模式必填）: [并行任务编号，如 `TASK-A`；非并行模式可省略]
```

## 2.2 Payload Type 2：evaluatorX → coderX（评估总结总线负载）

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
- **Task ID**（并行模式必填）: [并行任务编号，如 `TASK-A`；非并行模式可省略]
```

## 2.3 校验规则

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
