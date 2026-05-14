# 6. Parallel Dispatch & Merge（并行调度与合并机制）

当用户使用 `-parallel` 参数时触发本模块。本模块定义了从任务分解到并行调度再到结果合并的完整规程。

## 6.1 触发条件

- 指令格式：`/whole -parallel [需求]` 或 `/whole -box -parallel [需求]`
- 执行时机：plannerX 确认 PRD 之后、首次调用 coderX 之前
- 限制：`-parallel` 仅支持 `/whole` 模式（需 PRD Section 7 作为任务分解依据）

## 6.2 任务分解流程

plannerX 确认 PRD 后，orchestratorX 执行以下分解步骤：

1. **读取 Section 7**（Features & Acceptance Criteria），提取每个 feature 的：
   - AC 项编号与描述
   - 预期修改/创建的文件列表
   - 功能依赖关系（是否导入其他 feature 将创建的文件）

2. **并行性判定**（硬性规则，全部满足才可并行）：
   - **文件集互斥**：两个任务的目标文件集合无交集
   - **无导入耦合**：Task B 不依赖 Task A 将创建的文件
   - **共享配置隔离**：不同时修改 `package.json`、`tsconfig.json` 等共享配置文件
   - **AC 完整性**：每个任务包含完整的 feature AC 集，不拆分单个 AC

3. **分组策略**（软性约束）：
   - 最大并行数建议 ≤ 3 对
   - 优先按目录/模块亲和性分组
   - 有强依赖关系的功能即使文件集互斥也应串行

4. **输出分组方案**，格式如下，等待用户确认：

```markdown
## 并行化分析

基于 Section 7，识别出 {N} 个可并行任务组：

**Task A** — `{功能名称}`
  - AC: {编号列表}
  - 目标文件: `{路径列表}`
  - 复杂度: {低/中/高}

**Task B** — `{功能名称}`
  - AC: {编号列表}
  - 目标文件: `{路径列表}`
  - 复杂度: {低/中/高}

**冲突检测**: {无 / 检测到冲突项}
**必须串行的任务**: {列表（如有）}

确认并行调度？(yes / no / adjust)
```

5. 用户回复 `yes` 后进入 Shadow Doc 创建阶段；`adjust` 则允许用户手动调整分组。

## 6.3 Shadow Doc 创建规则

对每个确认的并行任务 T：

1. **复制 master hybrid doc** → `{master-name}.TASK-{T.id}.md`
2. **过滤 Section 7**：仅保留该任务的 AC 项，在顶部添加范围标注：
   ```markdown
   > ** 本文件为 Task {T.id} 的工作文档**
   > 请仅完成以下 AC 项：
   > - {AC编号}: {描述}
   > - ...
   >
   > **写入约束**：请仅修改 Section 8.2（Memory Snapshot）和 Section 9（评估报告）。
   > 禁止修改 Section 1-7、8.1、8.3、10。
   ```
3. **Section 10**：在顶部添加任务前缀标记 `<!-- TASK_ID: {T.id} -->`
4. 若使用 `-box`：为每个任务创建独立分支
   - 分支命名：`wfx/parallel-{TASK-ID}-{简短摘要}-{YYYYMMDD-HHmm}`
   - 例如：`wfx/parallel-A-feat-auth-20260514-1530`

## 6.4 调度规范

### 6.4.1 Prompt 构造

为每个任务对（coderX + evaluatorX）构造独立 prompt，必须包含：

- **shadow doc 路径**：作为该任务的 hybrid doc
- **过滤后的需求描述**：仅该任务的 AC 项
- **写入约束指令**：「仅修改 Section 8.2 和 Section 9，禁止修改其他区域」
- **Bus Payload 要求**：必须包含 `task_id` 字段（参考模块 02）
- **任务 ID 标识**：在 prompt 开头标明 `📌 [Task {T.id}]`

### 6.4.2 调度顺序

由于 Claude Code 的 Agent 工具为同步调用，采用**交替轮转调度**：

```
轮次 1: coderX-A → coderX-B → coderX-C
        （等待所有 coderX 返回并校验 Payload）
轮次 1: evaluatorX-A → evaluatorX-B → evaluatorX-C
        （等待所有 evaluatorX 返回并校验 Payload）
轮次 2（如需）: coderX-A(fix) → coderX-B(fix) → ...
```

每个 coderX/evaluatorX 返回后，立即按模块 02 校验其 Bus Payload（含 task_id）。

### 6.4.3 迭代限制

每个任务对**独立计数**，默认 2 次（由 `-N` 参数控制）。某任务达到最大迭代仍未 PASS 则标记为 FAILED，不影响其他任务继续。

## 6.5 结果合并流程

所有任务完成后（或部分失败），orchestratorX 执行合并：

### 6.5.1 代码合并

| 模式 | 操作 |
|---|---|
| `-parallel`（无 -box） | 所有任务在同一分支工作，验证 `git diff --check` 无冲突 |
| `-box -parallel` | 切回原始分支，按顺序 `git merge --no-ff` 每个任务分支 |

合并前审计：`git diff --name-only` 每个任务分支，对比声明文件集，检测越界修改。

### 6.5.2 Hybrid Doc 合并

| Section | 合并策略 |
|---|---|
| **8.2 Memory Snapshot** | 汇总所有 shadow doc 的 8.2 内容，每条加前缀 `[Task {id}]` |
| **9 评估报告** | 追加各任务评估报告，用 `## Task {T.id} 评估` 分隔；顶部写总评 |
| **10 检查点** | 追加各 shadow doc 的检查点，保持全局编号递增 |

### 6.5.3 合并检查点

在 master doc Section 10 写入合并检查点：
```
- **#CP-[N]** | **时间**: [ISO时间] | **阶段**: 并行任务全部完成 | **触发**: 自动
  - **已完成任务**: [Task A: {名称}] [Task B: {名称}] ...
  - **失败任务**: [Task X: {名称} — 原因] ... （如有）
  - **核心修改文件**: [合并后的完整文件列表]
  - **Git 状态**: [commit hash 或 "unstaged"]
  - **评估结果**: [全部通过 | 部分通过]
```

### 6.5.4 清理

- 成功任务的 shadow doc → **删除**
- 失败任务的 shadow doc → **保留**，供 debug
- `-box -parallel` 的任务分支 → **不自动删除**，用户自行决定

## 6.6 错误处理

| 场景 | 处理方式 |
|---|---|
| **单任务失败** | 不影响其他任务继续执行；合并成功任务的结果；报告失败任务详情 |
| **全部失败** | 不合并任何结果；master doc 保持并行前状态；保留所有 shadow doc |
| **文件越界** | coderX 修改了未分配的文件 → 合并前审计发现 → 标记并报告用户 |
| **Payload 校验失败** | 按模块 02 规则重试 1 次；仍失败则标记该任务 FAILED |
| **运行时崩溃** | 捕获异常，记录日志，继续执行剩余任务 |

### 单任务失败报告格式：
```markdown
## 并行执行结果

✅ **PASS**: Task A ({名称}), Task C ({名称})
❌ **FAILED**: Task B ({名称}) — 达到最大迭代次数 {N}，评估未通过

**Task B 最后评估摘要**: {evaluatorX 的 P0/P1 问题}

**建议下一步**：
1. 手动修复 Task B
2. 重新运行: `/whole -parallel --retry TASK-B`
3. 或继续使用已合并的部分结果
```

## 6.7 与 `-box` 参数的交互

- `/whole -parallel`（无 -box）：所有任务在同一分支工作，shadow doc 实现文档级隔离
- `/whole -box -parallel`：每个任务获得独立 git 分支，文档+分支双重隔离
- 命令参数顺序灵活：`/whole -box -parallel` = `/whole -parallel -box`

## 6.8 与 `/rollback` 的交互

并行执行期间收到 `/rollback`：
1. **中止**所有正在运行的任务对
2. **删除**所有 shadow doc
3. 若有 `-box`：**删除**所有任务分支（`git branch -D`）
4. 在 master doc 上**执行标准回滚**流程（参考模块 03）

## 6.9 与 `/status` 的交互

并行执行期间的 `/status` 输出需额外展示：
- 每个并行任务的当前状态（coder实现中 / 待评估 / 评估通过 / 需修复 / FAILED）
- 整体进度（如 2/3 任务完成）
- 最近的并行检查点

（参考模块 05 的并行状态展示格式）
