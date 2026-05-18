<div align="center">

[中文](./README.md) · **English**

# 🧰 WorkflowX: SubAgent-based Hybrid Orchestration Workflow

WorkflowX is a **pure file-driven multi-agent orchestration configuration system** — no servers to install, no runtime to set up. Just copy the config files into your AI IDE project and you're ready to go. By leveraging the `runSubAgent` capabilities of mainstream CLI tools, it builds an ecosystem where a master orchestrator intelligently delegates tasks to specialized sub-agents.

[![License](https://img.shields.io/badge/License-MIT-3B82F6?style=for-the-badge)](./LICENSE)
[![Skills](https://img.shields.io/badge/Skills-3-10B981?style=for-the-badge)](#-skills)
[![Prompts](https://img.shields.io/badge/Prompts-1-F59E0B?style=for-the-badge)](#-prompts)
[![AgentSkills](https://img.shields.io/badge/AgentSkills-Standard-8B5CF6?style=for-the-badge)](https://agentskills.io)

![Claude Code](https://img.shields.io/badge/Claude_Code-Skill-D97706?style=flat-square&logo=anthropic&logoColor=white)
![Codex](https://img.shields.io/badge/Codex-Skill-10B981?style=flat-square&logo=openai&logoColor=white)
![VSCode Copilot](https://img.shields.io/badge/VSCode_Copilot-Skill-6F42C1?style=flat-square&logo=github&logoColor=white)

</div>

The core philosophy: **Independent context for maximum efficiency, and hybrid document-driven state (Hybrid Docs) for seamless human-in-the-loop interaction.**

## 🌟 Design Philosophy

- **Zero-dependency deployment, config-and-run**
- **Reduce Hallucinations & Maximize Single-Step Efficiency**
- **Single-Point Operations with Global Synchronization**

## 🏗 System Architecture

Modern LLMs perform best when focused on a single, well-defined problem. WorkflowX solves the "context window bloating" and memory degradation problem through a modular design:

1. **Master Orchestrator Agent**: Acts as the central brain. It analyzes the main user prompt, plans the workflow path, and awakens the corresponding sub-agents at various nodes.
2. **Specialized Sub-Agents (Pure Context)**: Invoked via the `runSubAgent` protocol. Each sub-agent is awakened with a **pristine, strictly isolated context**, ensuring it operates at peak performance and focus without historical noise.
3. **Hybrid Document State Flow**: Instead of accumulating invisible black-box context like traditional chat histories, task progress, knowledge indexing, and architecture details are persisted into human-readable **Hybrid Documents**.
4. **Bus Pipeline Communication**: Agents don't pass verbose chat histories to each other — they exchange minimalist "Payloads" (e.g., coderX outputs: "I focused on fixing Logic B in File A, please review directionally"). Combined with a single source of truth (`[Feature]-hybrid.md`), this fundamentally eliminates context-stacking hallucinations.

## ✨ Core Capabilities

### Multi-Level Adaptive Compression (Auto-Compress)

As Hybrid documents bloat through iterations, `evaluatorX` automatically triggers a tiered compression strategy:

| Level | Trigger | Action |
|-------|---------|--------|
| **L0** Healthy | < 10KB / 200 lines | No action |
| **L1** Light | 10-15KB / 200-300 lines | Deduplicate file indexes, archive expired checkpoints |
| **L2** Standard | 15-25KB / 300-500 lines | Clean knowledge graph fragments, consolidate scattered entries |
| **L3** Deep | > 25KB / 500 lines | Full restructure: merge entities, sync memory snapshots, slim static sections |

Progressive compression eliminates the ultimate pain point: "AI getting dumber during prolonged battles."

### Prompt Optimization Engine (Prompt-Master)

Built-in **prompt-master** skill generates production-grade prompts for 20+ AI tools (Claude, GPT, Gemini, Cursor, Copilot, etc.):

- **9-Dimension Intent Extraction**: Silently analyzes task, target tool, output format, constraints, and more
- **Tool-Specific Routing**: Auto-matches optimal prompting strategies per model (e.g., no CoT for reasoning-native models)
- **6-Category Fault Scanning**: Detects and fixes ambiguity, missing context, format drift, and more
- **Copy-Paste Ready**: Outputs a single prompt block requiring zero manual edits

### Hybrid Docs × Indexing × Memory Graph — Maximum Token Savings

Three-layer collaboration that dramatically cuts context overhead:

**Layer 1: Hybrid Document Topology (Prompt Caching)**
- Strict zoning: **Static** (requirements, scope, DoD — rarely changes), **Incremental** (acceptance criteria, file indexes), **Dynamic** (evaluation reports — overwritten each round)
- Static sections at the top hit LLM Prompt Cache continuously; dynamic sections at the bottom don't invalidate cached tokens when overwritten
- Token costs stay minimal even after 100+ conversation turns

**Layer 2: Trunk-Leaf Index Separation**
- Markdown documents retain only business "trunk" outlines — no code detail dumps
- Entity relations, code structures ("leaves") are maintained separately in the MCP Knowledge Graph
- Agents fetch on-demand, keeping engineering documents lean

**Layer 3: Memory Graph Snapshot**
- Hybrid doc §8.2 stores only **skeleton pointers** to knowledge graph entities (names, relation summaries)
- Full leaf-node details are persisted by MCP server-memory
- L3 deep compression auto-syncs graph state, ensuring doc-graph consistency
- Cross-session, cross-agent knowledge sharing without redundant context transfer

> **Combined effect**: Static requirements trigger cache hits → incremental indexes enable targeted references → memory graph loads on-demand. Every SubAgent wake-up gets the minimum viable input tokens.

### 🤖 Seamless Auto / Semi-Auto Shift

Because cross-agent state is continuously persisted via clear Markdown/Text hybrid docs, human developers can safely pause, intervene, and guide the workflow by directly editing the documents for the next agent.

### 🧹 Zero Context Pollution

Strictly filters input information for each sub-agent. By blocking redundant long-history chats, it significantly drops the statistical probability of LLM hallucinations.

## ⚙️ Setup & Installation

1. Ensure Node.js (v18+) and Python 3.10+ are installed.
2. Install the required MCP tools for the workflow:
~~~bash
npm install -g @modelcontextprotocol/server-memory @modelcontextprotocol/server-sequential-thinking
~~~
3. Configure and mount the above MCPs in your AI Client (e.g., VSCode Copilot / Claude) using the provided configuration template `mcp.json.template`.

## 🚀 Workflow & Usage

### 1. Platform Integration

WorkflowX is a **lightweight, pure text-based configuration and instruction system**. No runtime lock-in, no extra services to install — just copy the config files into your project directory and deploy.

Three platform configurations are provided out of the box:

| Platform | Config Directory | Notes |
|----------|-----------------|-------|
| **Claude Code** | `.claude/` | agents + skills, native SubAgent support |
| **OpenAI Codex** | `.codex/` | agents (`.toml`) + skills, full parity |
| **GitHub Copilot** | `.github/` | agents (`.agent.md`) + skills + instructions |

> All three configurations share **identical workflow logic** — the same 7 commands, 3 modes, and 6 runtime modules. Only the tool-call syntax differs per platform.

**Quick Setup:**
1. Copy the relevant config directory (e.g., `.claude/`) into your project root
2. Install MCP dependencies: `npm install -g @modelcontextprotocol/server-memory @modelcontextprotocol/server-sequential-thinking`
3. Mount MCP config in your AI client (see `mcp.json.template`)
4. Start using: call orchestratorX in your chat and deliver your requirements

### 2. Command Reference

| Command | Description | Example |
|---------|-------------|---------|
| `/whole [req]` | Full-repo workflow (plan → code → evaluate) | `/whole implement user login module` |
| `/whole -box demo` | Execute in sandbox branch `demo`, isolated from main | `/whole -box auth refactor auth logic` |
| `/whole -parallel` | Auto-split independent tasks and dispatch in parallel | `/whole -parallel batch fix lint warnings` |
| `/whole -N 3` | Cap evaluator iterations at 3 (default: 2) | `/whole -N 3 optimize DB query performance` |
| `/local [req]` | Local module development, skips PRD planning | `/local fix order list pagination bug` |
| `/unit [req]` | Minimal single-task change, no evaluation | `/unit add timeout config to Config class` |
| `/prompt [text]` | Optimize a prompt only, no dev workflow triggered | `/prompt write me a login page prompt` |
| `/switch whole` | Force-switch workflow mode mid-task | `/switch unit` |
| `/rollback [iter]` | Rollback to a specific iteration checkpoint | `/rollback 1` |
| `/status` | Check completion status of the hybrid document | `/status` |

> By default, all development requests are routed through orchestratorX. Exceptions: pure file reads, config edits, Git operations, or when the user explicitly says "directly do it."

### 3. Three Workflow Modes

orchestratorX auto-routes based on requirement complexity, or you can specify manually:

```
/whole  → [plannerX plan] → [promptMasterX optimize] → [coderX implement] → [evaluatorX evaluate] → loop
/local  → [promptMasterX optimize] → [coderX implement] → [evaluatorX evaluate] → loop
/unit   → [promptMasterX optimize] → [coderX implement] → done
```

| | `/whole` Global | `/local` Scoped | `/unit` Minimal |
|---|---|---|---|
| **Use case** | New features, cross-module refactors | 1-2 module changes | Single-file fixes, small edits |
| **PRD planning** | plannerX generates full hybrid doc | Skipped | Skipped |
| **Evaluation loop** | evaluatorX auto-runs, up to N rounds | evaluatorX runs, up to N rounds | Only on explicit request |
| **Checkpoints** | Auto-created each iteration | Auto-created each iteration | Not mandatory |
| **Sandbox branch** | `-box` supported | Not supported | Not supported |
| **Parallel dispatch** | `-parallel` supported | Not supported | Not supported |

### 4. Walkthrough: A Complete `/whole` Session

Suppose you want to add a "User Login" feature to your project:

```
① Initiate the request
   /whole implement user login with email+password and OAuth support

② orchestratorX auto-routes to whole mode
   → plannerX analyzes requirements, generates [UserLogin]-hybrid.md
   → You review the hybrid doc, confirm it's correct, reply "confirmed"

③ promptMasterX optimizes the execution prompt
   → Translates confirmed requirements into precise coderX instructions

④ coderX implements based on the prompt
   → Outputs Bus Payload: "Completed auth module login logic,
     added oauth_callback handling. Focus review on token refresh flow"

⑤ evaluatorX reviews directionally based on the Payload
   → Writes audit report to the bottom of the hybrid doc
   → If issues found, generates fix Payload and hands back to coderX
     (up to N rounds)

⑥ Iteration complete
   → evaluatorX confirms pass, hybrid doc finalized
   → Optionally call abstracterX for a code summary
```

**Human Intervention**: At any point between steps, you can directly edit the hybrid document to adjust requirements, modify constraints, or correct direction. The next agent will automatically read your changes on startup.

### 5. Multi-Platform Collaboration

Since config directories are independent, you can use the same workflow across tools:

- **Claude Code CLI**: `.claude/agents/orchestratorX.md` defines agent behavior
- **VS Code + Copilot**: `.github/agents/orchestratorX.agent.md` uses VSCode-native tool bindings
- **OpenAI Codex CLI**: `.codex/agents/orchestratorX.toml` uses TOML format config

All three share the same skill definitions (in each platform's `skills/` directory), ensuring consistent workflow behavior.


## 🌟 About

This is an open-source experimental project deployed across real communities, aiming to explore best practices and architectural designs for multi-agent collaborative development.

Discussions, suggestions, and contributions of any kind are welcome!
How to contribute: Fork this repo, submit a Pull Request, or share your ideas directly in Issues.

If this project helps you, feel free to give it a ⭐ so more people can join us in exploring the future of AI-driven development!

---

<div align="center">

[MIT License](./LICENSE) · Free to use / Modify / Redistribute

Made by [@TreeX-X](https://github.com/TreeX-X)

</div>

## ⭐ Star History

<a href="https://www.star-history.com/#TreeX-X/workflowX&Date">
 <picture>
   <source media="(prefers-color-scheme: dark)" srcset="https://api.star-history.com/chart?repos=TreeX-X/workflowX&type=date&theme=dark&legend=top-left" />
   <source media="(prefers-color-scheme: light)" srcset="https://api.star-history.com/chart?repos=TreeX-X/workflowX&type=date&theme=light&legend=top-left" />
   <img alt="Star History Chart" src="https://api.star-history.com/chart?repos=TreeX-X/workflowX&type=date&theme=light&legend=top-left" />
 </picture>
</a>
