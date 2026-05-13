# CLAUDE.md — WorkflowX 项目指令

## 默认行为：始终使用 orchestratorX

**所有任务必须通过 orchestratorX 智能体执行。** 不要直接处理用户的开发请求。

### 规则

1. 当收到任何与代码开发、功能实现、重构、bug 修复相关的请求时，**必须**使用 `Agent` 工具调用 `orchestratorX` 子智能体。
2. 调用方式：`Agent(subagent_type="orchestratorX", prompt=用户原始需求)`。
3. orchestratorX 会自动路由到合适的工作流模式（whole/local/unit）并协调 plannerX、coderX、evaluatorX 等子智能体。
4. **例外情况**：以下场景不需要经过 orchestratorX：
   - 纯文件读取/搜索/浏览（探索性操作）
   - 项目配置修改（settings.json、CLAUDE.md 等）
   - Git 操作（commit、branch、status 等）
   - 用户明确说"直接做"或跳过编排

### 快捷指令

用户可以直接在对话中使用以下指令控制 orchestratorX：

- `/whole [需求描述]` — 全仓库级完整工作流（planner → coder → evaluator）
- `/local [需求描述]` — 单模块局部开发工作流
- `/unit [需求描述]` — 最小单元任务，直接修改
- `/prompt [原始 prompt]` — 仅做 prompt 优化，不触发工作流

## 文件读写规范（强制）

**本项目的源文件经过加密编码处理，Read 工具直接读取会显示乱码。** 所有文件操作必须遵循以下规则：

### 读取文件

- **禁止**使用 `Read` 工具直接打开项目源文件（会得到乱码）
- **必须**使用 `rg`（ripgrep）通过 Bash 搜索文件内容：
  - 搜索关键词：`rg "要搜索的内容" --path/to/file`
  - 搜索并显示上下文：`rg -C 3 "关键词" file`
  - 搜索全项目：`rg -n "关键词"`
- 仅 `.claude/` 目录下的配置文件（settings.json、CLAUDE.md、agents/*.md、skills/*.md）可正常使用 Read 工具读写

### 修改文件

- **优先**使用 `Edit` 工具做精准的字符串替换修改（不会破坏文件编码）
- **禁止**使用 `Write` 工具覆写整个项目源文件（会丢失加密编码，导致文件损坏）
- 如果需要新增文件内容，使用 `Bash` + `echo` 或 `printf` 追加到文件末尾
- 修改前务必先用 `rg` 确认目标内容的准确位置和上下文

### 总结

| 操作 | 正确方式 | 错误方式 |
|---|---|---|
| 读取源文件 | `rg` via Bash | Read 工具 |
| 搜索关键词 | `rg -n "keyword"` | Grep 工具（部分场景可用） |
| 修改源文件 | Edit 工具（精准替换） | Write 工具（覆写整个文件） |
| 读写配置文件 | Read / Write 工具 | — |

## 项目概要

WorkflowX 是一套多智能体协作开发框架，通过 orchestratorX 编排 planner、coder、evaluator、abstracter 等子智能体，实现从需求澄清到代码实现再到质量评估的完整闭环。

- 智能体定义：`.claude/agents/`
- 技能定义：`.claude/skills/`
- 运行时规程：`.claude/skills/orchestrator-playbook/SKILL.md`
