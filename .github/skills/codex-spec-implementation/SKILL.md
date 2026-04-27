---
name: codex-spec-implementation
description: Spec-driven coding workflow for codeX agents. Use this skill whenever implementing, fixing, refactoring, or iterating code from product-spec-context.md, especially when file index, knowledge index, or evaluator findings are present.
---

# codeX: Spec-Driven Implementation Skill

## 目标

让 codeX 按统一流程执行开发：
- 先读规格与验收标准
- 再读工程文件索引与知识索引
- 再读审核报告并按优先级修复
- 最后提交可验证的代码改动

## 输入文档约定

默认读取 `product-spec-context.md`，关键区块如下：
- `4` 核心功能与验收标准
- `5` 非功能性需求
- `7` 完成定义（DoD）
- `8.1` 工程文件索引与知识索引（主索引）
- `8.2` Memory Snapshot（关键约束）
- `8.3` 需求相关索引增量引用
- `9` 评估报告（Evaluator Reserved Section）

### Memory Snapshot 读取策略

- `8.2` 视为 server-memory 回写的知识图谱快照。
- codeX 在实现前应优先读取 `8.2` 中的 `nodes/edges/entrypoints` 作为上下文主入口。
- 若 `8.2` 缺失关键图谱信息，可调用 `mcp/server-memory` 进行补充读取，再以 `8.2` 为落地事实源执行开发。

## 执行流程

### 第一步：需求对齐

1. 读取 `4/5/7`，提取本轮必须满足的功能点、验收标准和非功能约束。
2. 形成本轮任务清单，避免实现超出范围。

### 第二步：上下文定向加载

1. 先读 `8.1` 主索引，确认涉及的核心文件、模块、入口。
2. 再读 `8.2` 知识图谱快照，提取与本轮任务相关的节点关系和实现入口。
3. 再读 `8.3` 增量索引，优先加载本轮变化相关上下文。
4. 若 `8.2` 图谱信息不足，调用 `mcp/server-memory` 补充读取后回填工作上下文。

### 第三步：审核反馈处理（条件执行）

1. 读取 `9` 评估报告区块。
2. 若 `9` 存在有效问题项：按严重度与优先级处理，顺序为 `P0/🔴 -> P1/🟡 -> P2/🟢`。
3. 若 `9` 无有效问题项或为空：跳过审核修复流程，按规格直接实现。

### 第四步：实现与验证

1. 仅修改与任务相关的最小文件集合，避免无关重构。
2. 对每项改动映射到验收标准，确保可验证。
3. 执行必要的构建/测试/静态检查，记录结果。

### 第五步：交接 evaluator

实现完成后，交给 evaluator 审核时必须明确：
- 本轮基于 `product-spec-context.md` 的哪些需求实现
- 需审核的代码范围
- 要求 evaluator 覆盖写 `9` 区块，不做增量追加

## 输出约束

1. 不得跳过规格读取直接编码。
2. 不得忽略 `8.1/8.3` 的索引上下文。
3. 对 `9` 的处理必须条件化：有内容则优先修复，无内容则跳过。
4. 不得虚构测试结果或需求完成状态。
5. 保持改动可追踪：每项改动都能回指到规格条目或评估问题。
6. 对图谱驱动改动保持可追踪：每项改动应能回指到 `8.2` 的节点或关系证据。
