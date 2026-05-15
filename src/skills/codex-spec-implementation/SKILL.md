---
name: codex-spec-implementation
description: Spec-driven coding workflow for coderX agents. Use this skill whenever implementing, fixing, refactoring, or iterating code from hybrid docs or specified requirements, especially when file index, knowledge index, or evaluator findings are present.
---

# coderX: Spec-Driven Implementation Skill

## Objectives

Enable coderX to execute development following a unified process:
- First read specifications and acceptance criteria
- Then read engineering file index and knowledge index
- Then read audit reports and fix by priority
- Finally submit verifiable code changes

## Input Document Conventions

Prioritize reading documents explicitly handed off by upstream agents or actively referenced by users; if no explicit specification is given, automatically locate the correct `[Feature Module]-hybrid.md` document. If there is no active reference and no document record in context, coderX is still allowed to continue operations directly using existing conversation context. When a hybrid document exists, focus on the following key sections:
- `4` Core Features & Acceptance Criteria
- `5` Non-Functional Requirements
- `7` Definition of Done (DoD)
- `8.1` Engineering File Index & Knowledge Index (Main Index)
- `8.2` Memory Snapshot (Key Constraints)
- `8.3` Requirement-Related Incremental Index References
- `9` Evaluation Report (Evaluator Reserved Section)
- `10` Iteration Checkpoints (Incremental Checkpoints) — **Automatically managed by orchestrator; coderX is prohibited from modifying this section**

### Memory Snapshot & Knowledge Graph Usage Rules

- Hybrid docs follow the "trunk and leaves separation" principle: Markdown files (e.g., `8.2`) only store the "trunk" (high-level requirement structure and knowledge node outlines/pointers).
- "Leaves" (detailed code logic relationships, code-level context constraints, etc.) are entirely stored in the nodes of `mcp/server-memory`.
- Before implementation, after reading `8.2` to obtain the required graph node outline, coderX **must actively call** the relevant tools via MCP Server (such as `mcp_memory_open_nodes` or `mcp_memory_search_nodes`) to query and retrieve Node detail data directly relevant to the current implementation task. Do not expect all details to be in Markdown.

## Execution Process

### Step 1: Requirement Alignment

1. Read `4/5/7`, extract the functional points, acceptance criteria, and non-functional constraints that must be satisfied in this round.
2. Form the current round task list; avoid implementing beyond scope.

### Step 2: Context-Oriented Loading (MCP Deep Retrieval)

1. First read the `8.1` main index to confirm the involved core files, modules, and entry points.
2. Read `8.2` to obtain the core architecture graph outline and referenced nodes.
3. **Call MCP Graph Layer Retrieval**: Based on the obtained outline pointers, use `mcp_memory_open_nodes` or related MCP tools to accurately retrieve specific code logic relationships and constraints relevant to your currently focused module, using them as real context.
4. Then read the `8.3` incremental index, prioritizing the loading of context related to this round's changes.

### Step 3: Audit Feedback Handling (Combined with Bus Communication, Conditional Execution)

1. **Read Pipeline Payload**: Prioritize reading the "Evaluation Summary Bus Payload" directly handed off by upstream evaluatorX in the conversation, quickly identifying the core issues and directions to fix in this round.
2. **Align Detailed Report**: Read the `9` evaluation report section reserved in the hybrid document to obtain specific line numbers and code-level issue details.
3. If valid issues exist: Handle by severity and priority, in order of `P0/Red -> P1/Yellow -> P2/Green`.
4. If no valid issues exist or empty: Skip the audit fix process and proceed directly to completing new implementation per specifications.

### Step 4: Implementation & Verification

1. Only modify the minimal file set related to the task; avoid unrelated refactoring.
2. Map each change to acceptance criteria, ensuring verifiability.
3. Execute necessary builds/tests/static checks and record results.

### Step 5: Bus Pipeline Output & Handoff to Evaluator

After implementation is complete, not only maintain the hybrid document and graph snapshot, but also **must proactively output a standardized "Phase Result Bus Payload (Pipeline Payload)" in the current conversation context before calling task completion or invoking sub-agents**, for the subsequent evaluatorX to read and review directionally.

> **Format Enforcement**: The orchestrator will perform structured validation on this Payload; failure will result in rejection and rewrite. Please strictly output according to the following required fields.

Payload content format:

```markdown
### Bus Pipeline Payload: Implementation Summary
- **Completed Feature Items**: [List the PRD requirement module names or numbers completed in this round]
- **Core Modification List**:
  - [File path] — [Modification role/logic summary]
  - ...
- **Directed Audit Request Points**: [Specify complex logic or external dependencies, prompting evaluatorX to focus review]
- **Associated Hybrid Document**: [hybrid document path]
- **Overwrite Requirement**: Please evaluatorX overwrite the evaluation report to the `9.*` section of the hybrid document
```

## Output Constraints

1. Must not skip specification reading and directly code.
2. Must not ignore the `8.1/8.3` index context.
3. Processing of `9` must be conditional: if content exists, prioritize fixes; if empty, skip.
4. Must not fabricate test results or requirement completion status.
5. Keep changes traceable: every change can be traced back to specification items or evaluation issues.
6. Keep graph-driven changes traceable: every change should be traceable to `8.2` nodes or relationship evidence.
