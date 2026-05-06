<div align="center">

**中文** · [English](./README.en.md)

# 🧰WorkflowX:基于 SubAgent 调度的混合 Mult-Agent 工作流

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

## 🛠️ 环境依赖与 MCP 工具配置 (Setup)

本项目的高级工作流深度依赖 MCP (Model Context Protocol) 提供的工具集（如记忆网络与系统思考引擎）。
为确保拉取工程后能直接运行完整的 workflowX 能力，请参照以下步骤配置你的客户端环境：

1. 确保安装了 Node.js (v18+) 与 Python 3.10+。
2. 安装工作流所需的 MCP 工具：
~~~
npm install -g @modelcontextprotocol/server-memory @modelcontextprotocol/server-sequential-thinking
~~~
3. 提供的配置文件模板 `mcp.json.template`,在您的 AI Client (如 VSCode Copilot / Claude) 中配置并挂载上述 MCP。
4. Orchestrator 在开始任务前，会执行“环境开箱自检”，协助您排查工具配置障碍。


## 📂 子功能——多终端协同

- `script/baseWorkFlow/automated_pipeline.py`：目录树快照监听与自动化流水线的核心，监控代码库文件变动与状态流转。
- `script/baseWorkFlow/worker_daemon.py`：工作者守护进程，处理与终端交互的底层系统通信（包含后台击键注入等高级交互式协调）。


## 🌟 关于


---

<div align="center">

[MIT License](./LICENSE) · 自由使用 / 修改 / 再分发

Made by [@TreeX-X](https://github.com/TreeX-X)

</div>