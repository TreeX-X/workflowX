---
name: abstracter-code-summary
description: Code & engineering analysis skill for abstracter agents. Use this skill whenever the user asks to summarize code, analyze project structure, review a module or subsystem, produce a structured Markdown analysis report, or evaluate code quality, risks, and improvement suggestions — even if they only provide a file path or directory name.
---

# Abstracter Code Summary Playbook

将本技能作为 abstracter 智能体的代码分析执行规范。

## 1. 目标

- 快速理解工程结构、核心逻辑与模块关系。
- 识别关键实现点、数据流/调用链、配置与构建方式。
- 用清晰、可复用的 Markdown 输出总结结果，帮助用户阅读、评审与决策。

## 2. 输入类型

- 单文件或多文件代码片段
- 指定目录/模块/子系统
- 完整工程仓库
- 用户附加关注点（如：架构、性能、风险、可维护性、测试覆盖、改进建议）

## 3. 工作方式

1. **深度思考与梳理**：对于大型工程片段或复杂业务逻辑，建议使用 `mcp/server-sequential-thinking` 工具进行多步递进式的代码读取验证和逻辑推演总结，以确保不出错。
2. 先提取上下文：项目语言、目录结构、入口点、核心依赖与运行方式。
3. 再聚焦主线：核心模块职责、关键函数/类、调用关系与数据流。
4. 补充质量视角：异常处理、边界条件、潜在风险、技术债与可优化点。
5. 最后给出结论：总结、优先级建议与后续行动项。

## 4. 输出要求

- 始终输出结构化 Markdown。
- 适度使用表格展示模块职责、风险分级或改进优先级。
- 对重要结论给出「依据来源」（文件路径、函数名、类名或配置项）。
- 语言简洁、信息密度高，避免空泛描述。

### 输出模板（必须遵循至少包含以下章节）

~~~markdown
# 总览
- 项目目标：
- 技术栈：
- 当前总结范围：

## 工程结构与模块职责
| 模块/目录 | 主要职责 | 关键文件 |
|---|---|---|
|  |  |  |

## 核心实现与工作流程
1. ...
2. ...

## 关键代码解读
- `path/to/file`：说明
- `ClassOrFunction`：说明

## 风险与问题
| 风险项 | 影响 | 证据 | 优先级 |
|---|---|---|---|
|  |  |  | 高/中/低 |

## 优化建议
1. 建议：
   - 预期收益：
   - 改动成本：
   - 适用范围：

## 结论与下一步
- 结论：
- 建议优先执行：
~~~

## 5. 行为约束

- 不臆测未出现的信息；不确定时明确标注「待确认」。
- 优先基于代码与配置事实，避免脱离上下文的通用建议。
- 涉及多种可行方案时，给出利弊对比与推荐方案。
- 若输入范围过大，先给分层摘要（全局 → 模块 → 关键点），再展开细节。
