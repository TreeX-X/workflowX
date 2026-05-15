---
name: evaluator-prd-audit
description: >
  Structured PRD-based code audit workflow. Use when evaluating code implementations against Product Requirement Documents.
  Triggers for: auditing code, evaluating implementation quality, checking requirements alignment, reviewing code diffs against PRD,
  running evaluator/audit agent, or any iteration handoff from a coding agent. Must be loaded whenever code needs systematic comparison
  against documented requirements to identify gaps, quality issues, and optimization opportunities.
---

# Evaluator: PRD-Based Code Audit Skill

## Why This Skill Is Needed

In iterative development workflows, after the coding agent completes code implementation, an **independent audit step** is needed to ensure:
- Code remains aligned with PRD requirements, with no omissions or deviations
- Code quality meets engineering standards
- Clear optimization directions exist for the next iteration round

This skill provides a standardized audit workflow for the evaluator agent, ensuring each evaluation result is structured, traceable, and handoff-ready.

## Trigger Conditions

When a user or upstream agent requests to "audit code", "evaluate implementation", "check code-requirements alignment", "run evaluator", "review", or similar expressions, this skill must be loaded.

## Core Workflow

### Step 1: Load Specification Document

1. Prioritize reading documents explicitly handed off by upstream agents or actively referenced by users (typically `[Feature Module]-hybrid.md`); if none, automatically search the project directory for the corresponding hybrid document and read it.
2. If there is no active reference and no related hybrid document record in context, the evaluator agent is allowed to proceed with the audit directly based on existing conversation context or code changes, explicitly noting that this is a "No Specification Document Evaluation Mode".
3. If a specification document is successfully read, extract the following key information:
   - **Requirement List**: Functional requirements, non-functional requirements, business rules
   - **Acceptance Criteria**: Verifiable conditions for each requirement
   - **Engineering File Index**: Engineering file entries in the `8.1` main index
   - **Knowledge Graph Outline**: Read the associated graph node outline/pointers from `8.2`.
4. **Graph Detail Retrieval (MCP)**: Based on the outline guide obtained from `8.2`, for the core module structures relevant to this change, proactively call `mcp/server-memory` (such as `mcp_memory_open_nodes` and other tools) to retrieve "leaf-level" specific code logic and context constraint details. Dynamically retrieved knowledge entities must serve as verification code specification basis; do not rely solely on Markdown reasoning.
5. Read the `8.3` incremental index differences and reading order variations.
6. Read the reserved evaluation section `9.*` for overwriting this round's evaluation results.
7. **Note**: The `10. Iteration Checkpoints` section is automatically managed by the orchestrator; evaluatorX is prohibited from modifying this section.

### Step 2: Obtain Code Changes & Directional Parsing (Bus Pipeline Mode)

This is the core input for evaluation:

1. **Read Upstream Bus Pipeline Payload**: Prioritize reading the "Phase Result Payload" output and handed off by coderX in the conversation flow (clarifying which features were completed, which files were modified). Use this information for **directional narrowing of audit scope** instead of blindly traversing the entire codebase.
2. **Read git diff**: Combined with the above payload scope, obtain the relative changes in the current working directory (unstaged + staged).
3. If git diff is empty, retrieve changes from the most recent commit.
4. **Search Context Files**: For modules, interfaces, and types specifically referenced by coderX, search related files in the project for complete context.

### Step 2 Supplement: Evaluation Mode Detection

Before formal evaluation, determine the evaluation mode for this round:

| Mode | Identifier | Trigger Condition | Behavior |
|------|------|---------|------|
| **Full Evaluation** | `full` | First evaluation / previous result was `Needs Fix` / no historical `9.*` records | Evaluate against all PRD requirements + all AC item by item |
| **Incremental Evaluation** | `incremental` | Previous evaluation result was `PASS` (i.e., new round after fix and resubmit) | **Only evaluate modified files and feature items declared in this round's Payload**; previously passed ACs directly inherit the previous round's conclusion |

**Determination Rules**:
- Read the previous round's `evaluation_mode` in hybrid document `9.1` and the `9.5` comprehensive evaluation conclusion.
- If the previous round's conclusion was `PASS` and this round's coderX Payload declares a localized modification scope -> `incremental`.
- All other cases -> `full`.

**Incremental Mode Special Behavior**:
1. Only verify the AC and requirement entries corresponding to files in the `Core Modification List` of the Payload.
2. Uninvolved requirements/ACs are directly marked as `Passed (inherited)` without redundant review.
3. If new P0 issues appear within the incremental scope, **automatically upgrade to `full` mode** and re-evaluate all requirements.

### Step 3: Requirement-by-Requirement Evaluation

Compare against each requirement in the PRD and evaluate code implementation status:

| Evaluation Dimension | Description |
|---------|------|
| Fully Implemented | Requirement has been completely and correctly implemented |
| Partially Implemented | Requirement has been implemented but with omissions or incompleteness |
| Not Implemented | Requirement has not been implemented at all |
| Unevaluable | Requirement cannot be evaluated within the current change scope (requires combining other parts) |

For each requirement, record:
- File path and key code segments of the corresponding implementation
- Consistency judgment between implementation and requirement
- Specific description of deviation from requirement (if any)

### Step 3 Supplement: Acceptance Criteria (AC) Evaluation (Mandatory)

In addition to requirement-level judgment, each acceptance criterion in the `4` section must be evaluated item by item:

| AC Evaluation Dimension | Description |
|------------|------|
| Pass | Code and behavior can directly prove satisfaction of the AC |
| Partial Pass | Implementation exists but is incomplete, with boundary or conditional omissions |
| Fail | Current implementation cannot satisfy the AC |
| Unevaluable | Missing runtime conditions, external dependencies, or insufficient current change scope |

Each AC must record:
- Original AC text or unique identifier
- Corresponding implementation location (file path and line number)
- Determination status
- Determination basis and gap description

If `Partial Pass / Fail` appears, actionable modification suggestions must be provided in the `9.3` issue list and `9.4` optimization suggestions.

### Step 4: Code Quality Review

In addition to requirement alignment, review general code quality dimensions:

1. **Correctness**: Whether obvious logic errors, boundary condition omissions, null pointer/null value risks exist
2. **Robustness**: Whether error handling is complete, input validation is sufficient
3. **Maintainability**: Whether naming, comments, and module division are clear
4. **Performance Risks**: Whether obvious performance issues exist (e.g., unnecessary loops, repeated queries, etc.)
5. **Security**: Whether injection risks, sensitive information leaks, etc. exist (judged based on project type)

### Step 5: Generate Evaluation Report

Generate the evaluation results as structured Markdown and **overwrite the `9. Evaluation Report (Evaluator Reserved Section)` block**.

> Do not append multiple rounds of reports at the bottom of the document; each round overwrites the `9.*` content.

```markdown
---

## 9. Evaluation Report (Evaluator Reserved Section)

### 9.1 Most Recent Evaluation Metadata
- Evaluation Time: {timestamp}
- Evaluation Scope: git diff (unstaged + staged)
- Evaluator/Agent: evaluatorX
- evaluation_mode: {full | incremental}
- Related Code Scope: {file_list}

### 9.2 Requirement Compliance Overview

| Requirement | Type | Status | Corresponding Code | Description |
|------|------|------|---------|------|
| {requirement name} | {functional/non-functional/rule} | Status | {file:line} | {description} |

- Fully Implemented: {count} / {total}
- Partially Implemented: {count}
- Not Implemented: {count}
- Unevaluable: {count}

### 9.2.1 Acceptance Criteria (AC) Compliance

| AC | Status | Corresponding Code | Basis/Gap | Modification Suggestion |
|----|------|---------|----------|---------|
| {AC identifier or summary} | Status | {file:line} | {evidence or gap description} | {actionable suggestion; N/A if Pass} |

- AC Total: {total}
- Pass: {count}
- Partial Pass: {count}
- Fail: {count}
- Unevaluable: {count}

### 9.3 Code Issue List

| # | Issue Type | Severity | Location | Description |
|---|---------|---------|------|------|
| 1 | {requirement deviation/logic defect/spec issue} | Severity | {file:line} | {issue description} |

### 9.4 Optimization Suggestions

| # | Suggestion | Expected Benefit | Suggested Priority |
|---|------|---------|-----------|
| 1 | {specific suggestion} | {benefit description} | P0/P1/P2 |

### 9.5 Comprehensive Evaluation Conclusion

{A summary paragraph describing the overall implementation quality of the current code, main gaps, and recommended next actions}
```

### Step 6: Supplementary Search When Needed

If the following situations are discovered during evaluation, proactively search other project files:
- Changed code references functions/classes/modules not included in the changes
- Specification requirements involve integration points with existing systems
- Suspected duplicate implementation or conflicts with existing functionality

Prioritize directed reading based on the `8.1` file index and knowledge index; when necessary, combine with `8.3` incremental differences to locate this round's focus.

Use semantic_search or grep_search to locate related code.

## Output Behavior Constraints

1. **Always Overwrite**: Each evaluation result overwrites the `9.*` evaluation section; no incremental appending.
2. **Evaluate Only Visible Facts**: Do not over-infer beyond what the code and specifications show; mark as "Pending Confirmation" when uncertain.
3. **Evaluations Must Be Actionable**: Every issue and suggestion must specify the file path and line number, enabling the coding agent to locate modifications directly.
4. **Distinguish Severity**:
   - P0 Red -- Blocking: Requirement not implemented or implementation incorrect, must be fixed
   - P1 Yellow -- Improvement: Implementation is basically correct but has optimization space
   - P2 Green -- Suggestion: Style, naming, comments, and other non-functional suggestions
5. **No Requirement, No Evaluation**: If the specification document has no evaluation criteria for a requirement, mark as "Unevaluable" rather than speculating.
6. **Index First**: Read the `8.1` main index and knowledge entries before evaluation; if `8.3` increments exist, supplement reading by difference priority.
7. **AC Must Be Evaluated**: As long as the specification document defines acceptance criteria, the `9.2.1` item-by-item AC evaluation and modification suggestions must be output; not just requirement-level summaries.

## Upstream/Downstream Collaboration (Bus Pipeline Output)

After overwriting the structured detailed evaluation report into the `9` section of the hybrid document, to form an efficient high-frequency iteration loop, **before returning control to coderX, a "Evaluation Summary Bus Payload (Pipeline Payload)" must be directly output in the current conversation flow** for the downstream agent.

> **Format Enforcement**: The orchestrator will perform structured validation on this Payload; failure will result in rejection and rewrite. Please strictly output according to the following required fields.

Payload content format:

```markdown
### Bus Pipeline Payload: Evaluation Summary
- **Core Audit Scope**: [Main features and code segments verified in this round]
- **Key Vulnerabilities/Rejection Items**:
  - P0 [issue summary -- file path:issue description]
  - P1 [issue summary -- file path:issue description]
  - ...
- **Evaluation Result**: [PASS | Needs Fix]
- **Recommended Next Action**: [Precisely guide coderX on which file and which logic to start with]
- **Associated Hybrid Document**: [hybrid document path]
- **Detailed Report Location**: hybrid document `9.*` section (overwritten)
```

Through this bus payload, the downstream agent can quickly enter repair state without consuming large amounts of tokens to deeply digest the full evaluation table each time.
