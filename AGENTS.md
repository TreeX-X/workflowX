# AGENTS.md — WorkflowX 项目指令 (Codex / 通用 AI Agent)

## Default Behavior: Always Use orchestratorX

**All development tasks must be executed through the orchestratorX agent.** Do not handle development requests directly.

### Rules

1. When receiving any code development, feature implementation, refactoring, or bug fix request, you **must** delegate to the `orchestratorX` agent.
2. orchestratorX will automatically route to the appropriate workflow mode (whole/local/unit) and coordinate sub-agents: plannerX, coderX, evaluatorX, etc.
3. **Exceptions** — the following scenarios do NOT need orchestratorX:
   - Pure file reading / searching / browsing (exploratory)
   - Project configuration changes (settings.json, CLAUDE.md, AGENTS.md, etc.)
   - Git operations (commit, branch, status, etc.)
   - User explicitly says "do it directly" or skips orchestration

### Quick Commands

- `/whole [task description]` — Full-repo workflow (planner → coder → evaluator)
- `/local [task description]` — Single-module local development workflow
- `/unit [task description]` — Minimal unit task, direct modification
- `/prompt [raw prompt]` — Prompt optimization only, no workflow triggered

## File Read/Write Rules (Mandatory)

**Source files in this project use encrypted encoding. Direct Read on project files will show garbled output.** All file operations must follow these rules:

### Reading Files

- **DO NOT** use the Read tool to open project source files (will return garbled text)
- **MUST** use `rg` (ripgrep) via Bash to search and read file content:
  - Search keyword: `rg "keyword" path/to/file`
  - Search with context: `rg -C 3 "keyword" file`
  - Search entire project: `rg -n "keyword"`
- Only files under `.claude/` directory (settings.json, CLAUDE.md, AGENTS.md, agents/*.md, skills/*.md) can be read/written normally with Read/Write tools

### Modifying Files

- **PREFER** the Edit tool for precise string-replacement edits (preserves file encoding)
- **DO NOT** use the Write tool to overwrite entire project source files (will lose encoding, corrupting the file)
- If new content needs to be appended, use `Bash` + `echo` or `printf` to append to file
- Before modifying, **always** use `rg` to confirm the exact location and context of the target content

### Summary

| Operation | Correct Method | Wrong Method |
|---|---|---|
| Read source files | `rg` via Bash | Read tool |
| Search keywords | `rg -n "keyword"` | Grep tool (limited scenarios) |
| Modify source files | Edit tool (precise replacement) | Write tool (overwrite entire file) |
| Read/write config files | Read / Write tools | — |

## General Rules

- Under normal circumstances, the use of PowerShell is prohibited. If it is unavoidable to use it, the correctness and completeness of the commands must be ensured.

## Project Overview

WorkflowX is a multi-agent collaborative development framework. orchestratorX coordinates plannerX, coderX, evaluatorX, abstracterX and other sub-agents to achieve a complete loop from requirement clarification → code implementation → quality evaluation.

- Agent definitions: `src/agents/`
- Skill definitions: `.claude/skills/`
- Runtime playbook: `.claude/skills/orchestrator-playbook/SKILL.md`
