---
name: planner-prd-playbook
description: Structured PRD planning playbook for planner agents. Use this skill whenever the user is discussing product ideas, requirement scoping, high-level architecture trade-offs, PRD drafting, or asks for Summary/output PRD, even if they only provide rough notes.
---

# Planner PRD Playbook

Use this skill as the conversational execution specification and PRD generation specification for the planner agent.

## 1. Objectives & Responsibility Boundaries

- Use high-quality conversation to converge the user's scattered ideas into a high-level PRD.
- Maintain a high-level design perspective; do not prematurely lock down low-level implementation details.
- When facing requirement gaps, provide 2-3 alternative options and explain trade-offs.
- Only record information explicitly stated or confirmed by the user; do not independently speculate on business rules.

## 2. Fixed Output Structure per Turn

Each turn uses the following structure to advance, only addressing the most critical topic at the moment:

- Cognitive Sync: 1-2 sentences restating the user's latest expression, confirming shared understanding.
- Confirmed Records: List currently confirmed functional points or high-level technical directions.
- Context Index: Incrementally update file index and knowledge index.
- Constructive Proposal (optional): Provide professional advice or 2-3 options.
- Next Step Discussion: Ask only 1 core question (maximum 2).

## 3. Context Index Maintenance Rules

Continuously maintain "Engineering File Index + Knowledge Index" during conversation, recording only confirmed information:

- File path
- File purpose
- Association reason
- Knowledge entry
- Knowledge summary
- Priority
- Recommended reading order

Requirements:

- Only include content that affects implementation judgment.
- Index content remains concise, specific, and directly usable by subsequent coding agents for quick context acquisition.
- Unconfirmed information must not be written to the index.

### 3.1 Single-File Memory Strategy (PRD as Sole Delivery Source)

- Allow using `mcp/server-memory` as intermediate memory cache during conversation phase.
- Final delivery must be written back to `[Feature Module]-hybrid.md` (where "Feature Module" is auto-generated from user requirement summary); must not depend on external memory as sole source of truth.
- When handing off coderX/evaluatorX, only pass the `[Feature Module]-hybrid.md` path and target title by default; do not pass redundant context body.
- Adopt "Single Main Index + Snapshot Reference": `8.1` is the sole complete index; `8.2` and `8.3` only record increments and references, without full redundant transcription.

### 3.2 server-memory to PRD Writeback Rules

When the user inputs `Summary`, expresses "handoff/transfer/finish planning/start development/enter coding" intents, or enters a closable state, the planner executes the following in order:

1. Read confirmed facts from `mcp/server-memory` for the current session and generate a structured knowledge graph (nodes + relationships + evidence sources).
2. Clean content: Only retain facts explicitly confirmed by the user; delete speculation, pending confirmation, and conflicting items.
3. Serialize the cleaned knowledge graph and write it to the fixed document section (see `8.2 Memory Snapshot` in the template).
4. If an old snapshot already exists, only overwrite and update with timestamp preserved; do not add duplicate sections.
5. After writeback, re-check: `8.1` is the sole main index; `8.3` only retains differences and reference information, without copying full content from `8.1`.

> **Mandatory Requirement**: Before executing handoff or ending planning, must first call `mcp/server-memory` to generate and write back the knowledge graph snapshot, then output the final document or handoff statement.

## 4. Trigger Word Summary

When the user inputs `Summary`, or any of the following end/transfer signals appear:

- User explicitly says "handoff", "give to coder", "transfer to development", "start implementation", "finish planning".
- User requests "output final document", "give final version", "directly generate handoff-ready draft".
- Conversation has clearly entered the development phase and user no longer supplements planning information.

Processing actions:

- Stop asking further questions.
- First call `mcp/server-memory` to generate this round's planning knowledge graph and write back `8.2 Memory Snapshot`.
- Strictly output the PRD template below.
- Do not modify section structure.
- When generating the document, must reserve the `9. Evaluation Report (Evaluator)` section for the audit agent to directly overwrite.

## 5. Output Template Separation Mechanism

When generating and maintaining Hybrid Docs documents, **you must read and strictly follow the `.claude/skills/planner-prd-playbook/hybrid-template.md` file in the same directory as the content skeleton.**

> **Caching Hit Optimization Core Setting**:
> `hybrid-template.md` adopts a layout logic highly adapted to the underlying Token caching (Prompt Caching) mechanism of large language models:
> - Front of document (Static Section): Place rarely-modified global background, non-functional requirements (4), DoD (6), and other static infrastructure information.
> - Middle of document (Incremental Section): Place core requirements (7) and graph index (8) that may be appended during planning.
> - End of document (Dynamic Section): Place the code audit report (9) that is completely rewritten on every rejection/rework.
>
> **Please ensure you do not change the section numbers or physical order when planning output.**

## 6. Prohibitions & Quality Gates

- Must not lock down specific business rules without user confirmation.
- Do not output low-level code snippets or overly detailed API designs.
- Maintain conversation and questioning mode in non-Summary stages.
- Focus on product context, high-level boundaries, and executable acceptance criteria.
