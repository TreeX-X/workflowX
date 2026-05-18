<div align="center">

**中文** · [English](./README.en.md)

# 🧰WorkflowX:基于 SubAgent 调度的混合多智能体工作流

![alt text](docx/images/WorkFlowX-Logo.png)
WorkflowX 是一套**纯文件驱动的多智能体编排配置系统**——无需安装服务、无需搭建运行时，将配置文件拷贝到您的 AI IDE 项目中即可完成部署。它充分利用主流 CLI 工具的 `runSubAgent` 能力，通过主智能体（Orchestrator）智能委派任务给多个专职子智能体（SubAgents），实现开发全链路的高效流转。


[![License](https://img.shields.io/badge/License-MIT-3B82F6?style=for-the-badge)](./LICENSE)
[![Skills](https://img.shields.io/badge/Skills-3-10B981?style=for-the-badge)](#-skills)
[![Prompts](https://img.shields.io/badge/Prompts-1-F59E0B?style=for-the-badge)](#-prompts)
[![AgentSkills](https://img.shields.io/badge/AgentSkills-Standard-8B5CF6?style=for-the-badge)](https://agentskills.io)

![Claude Code](https://img.shields.io/badge/Claude_Code-Skill-D97706?style=flat-square&logo=anthropic&logoColor=white)
![Codex](https://img.shields.io/badge/Codex-Skill-10B981?style=flat-square&logo=openai&logoColor=white)
![VSCode Copilot](https://img.shields.io/badge/VSCode_Copilot-Skill-6F42C1?style=flat-square&logo=github&logoColor=white)


</div>


核心设计哲学：**通过纯净独立的上下文保持智能体的最高水准状态，通过混合文档（Hybrid Docs）实现优雅的自动化与半自动化无缝切换。**

## 🌟 设计理念

- **零依赖部署，配置即运行**
- **降低幻觉成本，极限提升单步效率**
- **单点切入，全局联动**

## 🏗 系统架构设计

当前大语言模型在处理超长且复杂的上下文时容易出现”记忆灾难”。WorkflowX 提出了一套模块化的解决方案：

1. **调度主智能体（Orchestrator Agent）**：中枢大模型，负责拆解用户需求、规划路径，并在各个节点唤起对应能力的子智能体。
2. **纯净态子智能体（Specialized Sub-Agents）**：通过 `runSubAgent` 协议挂载。每个子智能体被唤起时，都拥有**独立且纯净的上下文**，这确保了它们工作时始终处于最佳和最专注的性能巅峰。
3. **”混合文档”状态流转**：摒弃传统对话中”长文不断累加”的隐性黑盒上下文，将任务进度、知识索引与工程架构输出并持久化为**混合文档**。
4. **总线管道通信（Bus Pipeline）**：智能体之间不传递冗长的对话历史，而是互相投喂极简的”成果 Payload”（如 Coder 仅输出：”我重点修了 A 文件的 B 逻辑，请重点定向查阅”）。结合单一事实源（整个迭代仅认一份 `[Feature]-hybrid.md`），从根本上杜绝上下文堆叠污染导致的幻觉问题。

## ✨ 核心能力

### 多级自适应压缩 (Auto-Compress)

当 Hybrid 文档随迭代膨胀时，evaluatorX 将自动触发分级压缩策略：

| 级别 | 触发条件 | 处理动作 |
|------|----------|----------|
| **L0** 健康 | < 10KB / 200行 | 无需处理 |
| **L1** 轻量 | 10-15KB / 200-300行 | 去重文件索引、归档过期检查点 |
| **L2** 标准 | 15-25KB / 300-500行 | 清理知识图谱碎片、合并散落条目 |
| **L3** 深度 | > 25KB / 500行 | 全量重构：合并知识实体、同步记忆快照、精简静态段 |

通过渐进式压缩，彻底解决”AI 在持久战中逐渐变笨”的终极痛点。

### 提示词优化引擎 (Prompt-Master)

内置 **prompt-master** 技能，为 20+ 种 AI 工具（Claude、GPT、Gemini、Cursor、Copilot 等）生成生产级提示词：

- **9维意图解析**：静默分析任务、目标工具、输出格式、约束条件等维度
- **工具专属路由**：根据目标模型自动匹配最优提示策略（如推理模型不追加 CoT）
- **6类故障扫描**：自动检测并修复任务歧义、上下文缺失、格式偏差等常见问题
- **一键即用**：输出可直接复制粘贴的提示词块，零二次修改

### 混合文档 × 索引 × 记忆图谱 —— 极致 Token 节省

WorkflowX 通过三层协同架构大幅削减上下文开销：

**第一层：混合文档拓扑排序 (Prompt Caching)**
- 将 Hybrid 文档严格划分为**静态区**（需求、范围、DoD — 极少变动）、**增量区**（功能验收、文件索引）、**动态区**（评估报告 — 每轮覆写）
- 静态区置于顶部，持续命中 LLM Prompt Cache；动态区置于底部，覆写时不会导致缓存失效
- 百轮对话后 Token 开销仍可保持极低水平

**第二层：干叶分离索引 (Trunk-Leaf Index)**
- Markdown 文档仅保留业务”树干”大纲，不堆积代码细节
- 实体关联、代码结构等”树叶”通过 MCP Knowledge Graph 独立维护
- 智能体按需动态检索，保持工程文档精瘦

**第三层：记忆图谱快照 (Memory Snapshot)**
- Hybrid 文档 §8.2 仅存储知识图谱的**骨架指针**（实体名称、关系概要）
- 完整的叶子节点详情由 MCP server-memory 持久化
- L3 深度压缩时自动同步图谱状态，确保文档与图谱一致
- 跨会话、跨智能体共享知识，无需重复传递上下文

> 三层协同效果：静态需求触发缓存 → 增量索引定向引用 → 记忆图谱按需加载，将每次 SubAgent 唤醒的输入 Token 压缩到最小。

### 🤖 自动化与半自动化随时切换

因为跨智能体状态通过清晰的 Markdown/混合文本持久化存储，人类开发者可以随时在某个环节介入，审查或修改文档，指导下一个智能体的方向。

### 🧹 拒绝上下文污染

严格控制每一个子 Agent 的信息输入口径，不向它灌输冗余的历史对话，大幅降低大模型的幻觉概率。


## 环境准备 (Setup & Installation)

1. 确保安装了 Node.js (v18+) 与 Python 3.10+。
2. 安装工作流所需的 MCP 工具：
~~~
npm install -g @modelcontextprotocol/server-memory @modelcontextprotocol/server-sequential-thinking
~~~
3. 提供的配置文件模板 `mcp.json.template`,在您的 AI Client (如 VSCode Copilot / Claude) 中配置并挂载上述 MCP。

## 🚀 使用指南 (Workflow & Usage)

### 1. 平台接入

WorkflowX 本质上是一套**轻量纯粹的配置文件与指令集系统**。不绑定任何运行时，无需安装额外服务——将配置文件复制到项目目录即可完成部署。

本工程提供三套平台配置，按需选用：

| 平台 | 配置目录 | 说明 |
|------|----------|------|
| **Claude Code** | `.claude/` | agents + skills，原生支持 SubAgent |
| **OpenAI Codex** | `.codex/` | agents (`.toml`) + skills，完全对等 |
| **GitHub Copilot** | `.github/` | agents (`.agent.md`) + skills + instructions |

> 💡 三套配置的**工作流逻辑完全一致**（相同的 7 个指令、3 种模式、6 个运行时模块），仅工具调用语法因平台而异。

**快速部署步骤：**
1. 将对应平台的配置目录（如 `.claude/`）复制到您的项目根目录
2. 安装 MCP 依赖：`npm install -g @modelcontextprotocol/server-memory @modelcontextprotocol/server-sequential-thinking`
3. 在 AI 客户端中挂载 MCP 配置（参考 `mcp.json.template`）
4. 开始使用：在对话中呼叫 orchestratorX 并投递需求

### 2. 指令速查

| 指令 | 说明 | 示例 |
|------|------|------|
| `/whole [需求]` | 全仓库级完整工作流（规划 → 编码 → 评估） | `/whole 实现用户登录模块` |
| `/whole -box demo` | 在沙箱分支 `demo` 中执行，隔离主线 | `/whole -box auth 重构鉴权逻辑` |
| `/whole -parallel` | 自动拆分可并行子任务，同时派发 | `/whole -parallel 批量修复 lint 告警` |
| `/whole -N 3` | 限定评估最多迭代 3 轮（默认 2 轮） | `/whole -N 3 优化数据库查询性能` |
| `/local [需求]` | 局部模块开发，跳过 PRD 规划阶段 | `/local 修复订单列表分页 bug` |
| `/unit [需求]` | 最小单元任务，直接修改，无评估 | `/unit 给 Config 类添加超时配置` |
| `/prompt [文本]` | 仅优化提示词，不触发开发流程 | `/prompt 帮我写一个登录页面的提示词` |
| `/switch whole` | 中途切换工作流模式 | `/switch unit` |
| `/rollback [轮次]` | 回滚到指定检查点 | `/rollback 1` |
| `/status` | 查看当前 hybrid 文档完成度 | `/status` |

> 默认行为：所有开发类请求会自动路由经过 orchestratorX。纯文件读取、配置修改、Git 操作等例外场景可直接执行。

### 3. 三种工作流模式

orchestratorX 根据需求复杂度自动路由，也可通过指令手动指定：

```
/whole  → [plannerX 规划] → [promptMasterX 优化] → [coderX 实现] → [evaluatorX 评估] → 循环
/local  → [promptMasterX 优化] → [coderX 实现] → [evaluatorX 评估] → 循环
/unit   → [promptMasterX 优化] → [coderX 实现] → 完成
```

| | `/whole` 全局模式 | `/local` 局部模式 | `/unit` 单元模式 |
|---|---|---|---|
| **适用场景** | 新功能、跨模块重构 | 1-2 个模块内的修改 | 单文件修复、小改动 |
| **PRD 规划** | plannerX 生成完整 hybrid 文档 | 跳过 | 跳过 |
| **评估迭代** | evaluatorX 自动执行，最多 N 轮 | evaluatorX 执行，最多 N 轮 | 仅在明确要求时执行 |
| **检查点** | 每轮迭代后自动创建 | 每轮迭代后自动创建 | 非强制 |
| **沙箱分支** | 支持 `-box` 参数 | 不支持 | 不支持 |
| **并行派发** | 支持 `-parallel` 参数 | 不支持 | 不支持 |

### 4. 实战示例：一次完整的 `/whole` 工作流

假设您要为项目添加一个"用户登录"功能：

```
① 发起请求
   /whole 实现用户登录功能，支持邮箱+密码和 OAuth 两种方式

② orchestratorX 自动路由到 whole 模式
   → plannerX 分析需求，生成 [UserLogin]-hybrid.md
   → 您审阅 hybrid 文档，确认需求无误后回复"确认"

③ promptMasterX 优化执行指令
   → 将确认后的需求转化为精确的 coderX 执行提示词

④ coderX 根据提示词编码实现
   → 完成后输出 Bus Payload："完成了 auth 模块的登录逻辑，
     新增 oauth_callback 处理，请重点检查 token 刷新流程"

⑤ evaluatorX 根据 Payload 定向审查
   → 在 hybrid 文档底部写入审计报告
   → 如发现问题，生成修复 Payload 交还 coderX（最多 N 轮）

⑥ 迭代完成
   → evaluatorX 确认通过，hybrid 文档收口为最终版本
   → 可手动呼叫 abstracterX 生成代码摘要（可选）
```

**人工介入**：在任意步骤之间，您可以直接编辑 hybrid 文档来调整需求、修改约束或纠正方向。下一个智能体启动时会自动读取您修改后的内容。

### 5. 多平台协作

由于配置目录互相独立，您可以在不同工具中使用同一套工作流：

- **Claude Code CLI**：`.claude/agents/orchestratorX.md` 定义智能体行为
- **VS Code + Copilot**：`.github/agents/orchestratorX.agent.md` 使用 VSCode 原生工具绑定
- **OpenAI Codex CLI**：`.codex/agents/orchestratorX.toml` 使用 TOML 格式配置

三者共享相同的 skills 定义（位于各平台的 `skills/` 目录），确保工作流行为一致。


## 🌟 关于

这是真实投入各个社区使用的一个开源实验性项目，旨在探索多智能体协同开发的最佳实践与架构设计。

欢迎任何形式的讨论、建议与贡献！
如何贡献：Fork 本仓库，提交 Pull Request，或直接在 Issues 中提出你的想法。

公众号：[TreeX-AI]


如果开源对你有帮助，欢迎点亮⭐，让更多人加入一起探索 AI 开发的未来！

---

<div align="center">

[MIT License](./LICENSE) · 自由使用 / 修改 / 再分发

Made by [@TreeX-X](https://github.com/TreeX-X)

</div>

## ⭐星级历史

<a href="https://www.star-history.com/#TreeX-X/workflowX&Date">
 <picture>
   <source media="(prefers-color-scheme: dark)" srcset="https://api.star-history.com/chart?repos=TreeX-X/workflowX&type=date&theme=dark&legend=top-left" />
   <source media="(prefers-color-scheme: light)" srcset="https://api.star-history.com/chart?repos=TreeX-X/workflowX&type=date&theme=light&legend=top-left" />
   <img alt="Star History Chart" src="https://api.star-history.com/chart?repos=TreeX-X/workflowX&type=date&theme=light&legend=top-left" />
 </picture>
</a>