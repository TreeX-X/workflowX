<div align="center">

**中文** · [English](./README.en.md)

# 🧰WorkflowX:基于 SubAgent 调度的混合多智能体工作流

WorkflowX 是一个先进的多智能体编排框架，旨在为 AI 辅助开发提供强大的底层引擎。它充分利用主流 CLI 工具的 `runSubAgent` 能力，通过主智能体（Orchestrator）智能委派任务给多个专职子智能体（SubAgents），实现开发全链路的高效流转。


[![License](https://img.shields.io/badge/License-MIT-3B82F6?style=for-the-badge)](./LICENSE)
[![Skills](https://img.shields.io/badge/Skills-3-10B981?style=for-the-badge)](#-skills)
[![Prompts](https://img.shields.io/badge/Prompts-1-F59E0B?style=for-the-badge)](#-prompts)
[![AgentSkills](https://img.shields.io/badge/AgentSkills-Standard-8B5CF6?style=for-the-badge)](https://agentskills.io)

![Claude Code](https://img.shields.io/badge/Claude_Code-Skill-D97706?style=flat-square&logo=anthropic&logoColor=white)
![Codex](https://img.shields.io/badge/Codex-Skill-10B981?style=flat-square&logo=openai&logoColor=white)
![VSCode Copilot](https://img.shields.io/badge/VSCode_Copilot-Skill-6F42C1?style=flat-square&logo=github&logoColor=white)


</div>


核心设计哲学：**通过纯净独立的上下文保持智能体的最高水准状态，通过混合文档（Hybrid Docs）实现优雅的自动化与半自动化无缝切换。**

## 🌟 核心理念

- **自动部署、敏捷开发、持续交付**
- **降低幻觉成本，极限提升单步效率**
- **单点切入，全局联动**

## 🏗 系统架构设计

当前大语言模型在处理超长且复杂的上下文时容易出现“记忆灾难”。WorkflowX 提出了一套模块化的解决方案：

1. **调度主智能体（Orchestrator Agent）**：中枢大模型，负责拆解用户需求、规划路径，并在各个节点唤起对应能力的子智能体。
2. **纯净态子智能体（Specialized Sub-Agents）**：通过 `runSubAgent` 协议挂载。每个子智能体被唤起时，都拥有**独立且纯净的上下文**，这确保了它们工作时始终处于最佳和最专注的性能巅峰。
3. **“混合文档”状态流转**：摒弃传统对话中“长文不断累加”的隐性黑盒上下文，将任务进度、知识索与工程架构输出并持久化为**混合文档**。

## ✨ 核心特性

- 🤖 **自动化与半自动化随时切换**：因为跨智能体状态通过清晰的 Markdown/混合文本持久化存储，人类开发者可以随时在某个环节介入，审查或修改文档，指导下一个智能体的方向。
- 🧹 **拒绝上下文污染**：严格控制每一个子 Agent 的信息输入口径，不向它灌输冗余的历史对话，大幅降低大模型的幻觉概率。


## 环境准备 (Setup & Installation)

1. 确保安装了 Node.js (v18+) 与 Python 3.10+。
2. 安装工作流所需的 MCP 工具：
~~~
npm install -g @modelcontextprotocol/server-memory @modelcontextprotocol/server-sequential-thinking
~~~
3. 提供的配置文件模板 `mcp.json.template`,在您的 AI Client (如 VSCode Copilot / Claude) 中配置并挂载上述 MCP。

## 🚀 框架工作流与使用指南 (Workflow & Usage)

**1. 框架定位与平台接入**
WorkflowX 本质上是一套**轻量纯粹的配置文件与指令集系统**。它不绑定死板的单一应用，您可以按需将其无缝接入到任何支持 Agent/Skill 体系的 AI IDE 客户端中（如 **GitHub Copilot, Claude Code, 或 Codex**）。
> 💡 **强烈推荐使用 GitHub Copilot**: 其原生的 Workspace 感知能力和无缝的子智能体 (SubAgent) 唤起机制，能与本框架的总线管道与动静缓存模型完美契合，发挥出最极致的体验。

**2. 唤醒中枢调度与迭代流转**
- 呼叫 `@orchestratorX`（主智能体），并投递开发意图或执行指令（如 `/whole` 全局开发、`/local` 局部热更）。
- **PlannerX (规划者)**：接手初始需求，通过多轮对话沉淀出仅有一份的 `[模组]-hybrid.md` 规范。
- **CodeX (编码者)**：根据混合文档进行开发验证，通过后以“阶段成果总线负载 (Payload)”的形态输出修改摘要。
- **EvaluatorX (评估者)**：根据上述的总线负载定向核测代码变更与文档规范，并在 `hybrid` 中回写审计报告，再提出下一步修复总线载荷，交还控制权。
- 通过配置指令 `-N` 可自动限定迭代轮数（如默认最多 2 轮防死循环）。

## 💎 核心优势：如何解决 AI 开发通病？

**1. 总线管道机制 (Bus Pipeline) —— 彻底根除上下文幻觉**
传统 AI 开发最大的问题在于**对话上下文的不停堆叠污染**，越野越偏。
WorkflowX 通过独立的 SubAgent 机制配合“总线管道”解决此痛点：
- **纯净态唤醒**：每个子智能体（coder, evaluator）在被唤起时，不会继承之前冗余的探讨与报错历史，每次都处于“全新、专注”的最高智商区间。
- **总线载荷交接**：智能体之间不抛历史长文，而是互相投喂极简的“成果 Payload”。（例如 Coder 仅仅输出：“我重点修了 A 文件的 B 逻辑，请重点定向查阅”）。极大地提高了评估专注度，几乎消除幻觉。

**2. 敏捷单一事实源 —— 混合文档 (Hybrid Docs) 约束**
敏捷开发需要随时调整方向，散落的 PRD 与设计文档极易与代码脱节。
- 整个迭代生命周期只认一份活文档 `[Feature]-hybrid.md`。上方记录死需求，中间记录增删知识，最下方预留为代码体检报告。不仅全透传给 AI 保持对齐，且随时支持人类介入无缝审阅或重写。

**3. 定制化核心 Skill 群 —— 跨越 Token 屏障**
这里深度定制了一系列精细的技能（Skill），精准击破大模型开发常见灾难：
- **Prompt Caching 动静态重组化**：强行规定混合文档的拓扑排序——坚如磐石的“核心需求”放顶部永久触发缓存，每轮都在覆写的“评估报告”放底部。极大节约 Token 开销，纵使百轮对话亦不卡顿。
- **干叶分离架构 (Graph Separation)**：严禁将长篇大论的代码逻辑堆积在 Markdown 内。Markdown 中只留业务“树干大纲”。具体的实体关联、代码结构（“树叶”）通过指令强行抽离并维护于基于服务器的 MCP Knowledge Graph 内。智能体干活前，按需动态检索提取，保证工程文档精瘦。
- **自动排毒压缩 (Auto-Compress)**：定制超限清洗机制，一旦检测出 Hybrid 文档超过 15KB，评估员将自动触发碎片提炼与图谱归并动作清扫垃圾，彻底解决“AI 在持久战中逐渐变笨”的终极痛点。

## 📂 子功能——多cli协同

- `script/baseWorkFlow/automated_pipeline.py`：目录树快照监听与自动化流水线的核心，监控代码库文件变动与状态流转。
- `script/baseWorkFlow/worker_daemon.py`：工作者守护进程，处理与终端交互的底层系统通信（包含后台击键注入等高级交互式协调）。
- `docx/`：存放用于在子智能体之间做状态与知识传递的核心混合文档。


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