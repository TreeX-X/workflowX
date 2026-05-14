---
name: orchestrator-playbook
description: "orchestratorX 的运行时规程手册。按功能模块拆分为独立文件，orchestratorX 在执行工作流时仅加载对应模块，避免全量注入。"
---

# orchestrator Playbook — 运行时规程手册

> **定位**：本技能是 orchestratorX 的"操作手册"，包含所有触发式规程。
> 各功能模块已拆分为独立文件，orchestratorX 按需加载对应模块，而非全量读取。

## 模块索引

| # | 模块 | 触发条件 | 文件路径 |
|---|---|---|---|
| 1 | 环境初始化 + MCP 降级 | 首次进入 whole/local/unit 工作流 | `modules/01-environment-init.md` |
| 2 | Bus Payload 规范与校验 | 跨智能体交接（coderX ↔ evaluatorX） | `modules/02-bus-payload.md` |
| 3 | 增量检查点与回滚 | coderX/evaluatorX 返回后；用户发出 `/rollback` | `modules/03-checkpoint-rollback.md` |
| 4 | Prompt 预处理规则 | 调用 coderX 前（除 whole planner/coder 首轮） | `modules/04-prompt-preprocess.md` |
| 5 | Status Report 规范 | 用户发出 `/status` | `modules/05-status-report.md` |
| 6 | 并行调度与合并 | 使用 `-parallel` 参数时 | `modules/06-parallel-dispatch.md` |

## 加载规则

orchestratorX 在执行对应操作前，使用 Read 工具加载上述索引表中对应模块文件的完整路径。**严禁全量加载本技能目录下的所有模块文件**，只加载当前操作触发的模块。
