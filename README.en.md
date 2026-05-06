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

## ⚙️ Setup & Installation

1. Ensure Node.js (v18+) and Python 3.10+ are installed.
2. Install the required MCP tools for the workflow:
~~~bash
npm install -g @modelcontextprotocol/server-memory @modelcontextprotocol/server-sequential-thinking
~~~
3. Configure and mount the above MCPs in your AI Client (e.g., VSCode Copilot / Claude) using the provided configuration template `mcp.json.template`.

## 🚀 Workflow & Usage

**1. Awaken the Orchestrator & Iterate**
- Call `@orchestratorX` (the master agent) and deliver your development intention or execution command (e.g., `/whole` for global development, `/local` for targeted hot-reloading).
- **PlannerX (The Planner)**: Takes control of the initial requirements. Through multi-turn dialogue, it distills the intent into a single binding specification: `[Module]-hybrid.md`.
- **CodeX (The Coder)**: Develops and verifies code based on the hybrid document. Once completed, it outputs a summary of changes via a minimalist "Bus Pipeline Payload".
- **EvaluatorX (The Evaluator)**: Directionally inspects code changes and specs based on the Pipeline Payload. It writes an audit report directly into the `hybrid` document, proposes the next targeted payload for fixes, and hands control back.
- Iteration loops can be safely constrained (e.g., max 2 rounds to prevent infinite loops) using the `-N` configuration parameter.

## 💎 Core Advantages: Solving AI Development Bottlenecks

**1. Bus Pipeline Mechanism — Eradicating Context Hallucinations**
The biggest flaw in traditional AI development is the continuous stacking and pollution of dialog context, causing the AI to drift off course. WorkflowX solves this via isolated SubAgents and a "Bus Pipeline":
- **Pristine Awakening**: When sub-agents (coder, evaluator) are awakened, they do not inherit redundant discussions and historical errors. They start fresh, focused, and operating at absolute peak intelligence every time.
- **Payload Handoff**: Agents do not throw long historical texts at each other. They feed each other minimalist "Payloads." (E.g., CodeX outputs: "I focused on fixing Logic B in File A, please review directionally"). This drastically improves evaluation focus and almost entirely eliminates hallucinations.

**2. Agile Single Source of Truth — Hybrid Docs Constraint**
Agile development requires spontaneous shifts in direction, but scattered PRDs often lose sync with the code. 
- The entire iteration lifecycle relies on just ONE living document: `[Feature]-hybrid.md`. Static requirements are kept at the top, incremental knowledge in the middle, and volatile code health reports at the bottom. It is transparently transmitted to the AI while safely allowing human developers to pause, intervene, or seamlessly rewrite at any point.

**3. Customized Core Skill Set — Breaking the Token Barrier**
We've finely customized a suite of Skills that precisely combat common LLM structural catastrophes:
- **Prompt Caching Restructure**: Strictly mandates the topological layout of the Hybrid Document—rock-solid "Core Requirements" sit at the top for permanent cache hits, while the "Evaluation Report" (rewritten every round) sits at the very bottom. This saves massive token costs and ensures lightning-fast responses even after a hundred turns of conversation.
- **Graph Separation Architecture (Trunk vs Leaves)**: Explicitly forbids dumping massive chunks of code logic into Markdown. Markdown only retains the business "Trunk" outline. Detailed entity relations and code constraints ("Leaves") are forcibly extracted and maintained within a server-based MCP Knowledge Graph. Agents dynamically fetch these as needed, keeping engineering documents lean.
- **Auto-Compress Mechanism**: A custom threshold cleaning mechanism. Once the Evaluator detects a Hybrid Document exceeding 15KB or 300 lines, it automatically triggers abstract fragment consolidation to sweep out graph garbage. This functionally solves the fatal pain point of "AI getting dumber during prolonged battles".

## 📂 Core Modules

- `script/baseWorkFlow/automated_pipeline.py`: The heart of workspace snapshot listening and automation pipeline, monitoring repo file changes and state transitions.
- `script/baseWorkFlow/worker_daemon.py`: The worker daemon that handles low-level system communication and terminal interaction (including advanced background keystroke injection orchestration).
- `docx/`: Directory designated for passing the core hybrid state and knowledge docs between sub-agents.

## 🌟 About



---

<div align="center">

[MIT License](./LICENSE) · Free to use / Modify / Redistribute

Made by [@TreeX-X](https://github.com/TreeX-X)

</div>
