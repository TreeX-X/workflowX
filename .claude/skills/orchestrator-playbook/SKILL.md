---
name: orchestrator-playbook
description: "Runtime specification manual for orchestratorX. Split into independent files by functional module; orchestratorX loads only the corresponding module during workflow execution, avoiding full injection."
---

# orchestrator Playbook -- Runtime Specification Manual

> **Positioning**: This skill is the "operations manual" for orchestratorX, containing all trigger-based procedures.
> Each functional module has been split into independent files; orchestratorX loads the corresponding module on demand rather than reading the entire skill.

## Module Index

| # | Module | Trigger Condition | File Path |
|---|---|---|---|
| 1 | Environment Init + MCP Fallback | First entry into whole/local/unit workflow | `modules/01-environment-init.md` |
| 2 | Bus Payload Schema & Validation | Cross-agent handoff (coderX <-> evaluatorX) | `modules/02-bus-payload.md` |
| 3 | Incremental Checkpoint & Rollback | After coderX/evaluatorX returns; user issues `/rollback` | `modules/03-checkpoint-rollback.md` |
| 4 | Prompt Preprocessing Rules | Before calling coderX (except whole planner/coder first round) | `modules/04-prompt-preprocess.md` |
| 5 | Status Report Specification | User issues `/status` | `modules/05-status-report.md` |
| 6 | Parallel Dispatch & Merge | When using `-parallel` parameter | `modules/06-parallel-dispatch.md` |

## Loading Rules

Before executing the corresponding operation, orchestratorX uses the Read tool to load the full path of the corresponding module file from the index table above. **Strictly prohibited from loading all module files in this skill directory at once**; only load the module triggered by the current operation.
