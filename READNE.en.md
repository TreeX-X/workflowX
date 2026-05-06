<div align="center">

[中文](./READNE.md) · **English**

# 🧰 WorkflowX: SubAgent-based Hybrid Orchestration Workflow

WorkflowX is an advanced multi-agent orchestration framework designed to supercharge your AI-assisted development. By leveraging the `runSubAgent` capabilities of mainstream CLI tools, it builds an ecosystem where a master orchestrator intelligently delegates tasks to specialized sub-agents. 

[![License](https://img.shields.io/badge/License-MIT-3B82F6?style=for-the-badge)](./LICENSE)
[![Skills](https://img.shields.io/badge/Skills-3-10B981?style=for-the-badge)](#-skills)
[![Prompts](https://img.shields.io/badge/Prompts-1-F59E0B?style=for-the-badge)](#-prompts)
[![AgentSkills](https://img.shields.io/badge/AgentSkills-Standard-8B5CF6?style=for-the-badge)](https://agentskills.io)

![Claude Code](https://img.shields.io/badge/Claude_Code-Skill-D97706?style=flat-square&logo=anthropic&logoColor=white)
![Codex](https://img.shields.io/badge/Codex-Skill-10B981?style=flat-square&logo=openai&logoColor=white)
![VSCode Copilot](https://img.shields.io/badge/VSCode_Copilot-Skill-6F42C1?style=flat-square&logo=github&logoColor=white)

</div>

The core philosophy: **Independent context for maximum efficiency, and hybrid document-driven state (Hybrid Docs) for seamless human-in-the-loop interaction.**

## 🌟 Core Concepts

- **Automated Deployment, Agile Process & Continuous Delivery**
- **Reduce Hallucinations & Maximize Single-Step Efficiency**
- **Single-Point Operations with Global Synchronization**

## 🏗 System Architecture

Modern LLMs perform best when focused on a single, well-defined problem. WorkflowX solves the "context window bloating" and memory degradation problem through a modular design:

1. **Master Orchestrator Agent**: Acts as the central brain. It analyzes the main user prompt, plans the workflow path, and awakens the corresponding sub-agents at various nodes.
2. **Specialized Sub-Agents (Pure Context)**: Invoked via the `runSubAgent` protocol. Each sub-agent is awakened with a **pristine, strictly isolated context**, ensuring it operates at peak performance and focus without historical noise.
3. **Hybrid Document State Flow**: Instead of accumulating invisible black-box context like traditional chat histories, task progress, knowledge indexing, and architecture details are persisted into human-readable **Hybrid Documents**.

## ✨ Key Features

- 🤖 **Seamless Auto / Semi-Auto Shift**: Because cross-agent state is continuously persisted via clear Markdown/Text hybrid docs, human developers can safely pause, intervene, and guide the workflow by directly editing the documents for the next agent.
- 🧹 **Zero Context Pollution**: Strictly filters input information for each sub-agent. By blocking redundant long-history chats, it significantly drops the statistical probabilty of LLM hallucinations.
- 🔌 **CLI-Agnostic Interface**: Backed by a robust `automated_pipeline` and scheduler daemon, perfectly compatible with terminal workflow engines for tests, scripts, and deep IDE integration.

## 📂 Core Modules

- `script/baseWorkFlow/automated_pipeline.py`: The heart of workspace snapshot listening and automation pipeline, monitoring repo file changes and state transitions.
- `script/baseWorkFlow/worker_daemon.py`: The worker daemon that handles low-level system communication and terminal interaction (including advanced background keystroke injection orchestration).
- `docx/`: Directory designated for passing the core hybrid state and knowledge docs between sub-agents.

## 🛠️ Environments & MCP Setup

Our advanced workflows heavily rely on toolsets provided by MCP (Model Context Protocol), such as the Memory graph and Sequential Thinking engine.
To ensure the full capabilities of workflowX run flawlessly out-of-the-box, please configure your client environment:

1. Ensure `Node.js` is correctly installed on your system (for `npx` execution).
2. Locate the provided setup template `mcp.json.template` at the project root.
3. Copy the `mcpServers` JSON block and merge it into the MCP settings file of your AI IDE (e.g., VS Code Copilot, Cursor, RooCode/Cline).
4. The Orchestrator agent performs an automatic bootstrap check at initialization to guide you through resolving any missing dependencies.

## 🌟 About



---

<div align="center">

[MIT License](./LICENSE) · Free to use / Modify / Redistribute

Made by [@TreeX-X](https://github.com/TreeX-X)

</div>
