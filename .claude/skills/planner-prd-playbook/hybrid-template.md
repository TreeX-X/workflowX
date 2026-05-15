# Hybrid Docs - [Feature Module]

**File Name**: [Feature Module]-hybrid.md

**Document Status**: Draft
**Update Date**: [Current Date]
**Author**: [Tree]
**Version**: v1.0

---

> **Static Context (Static Section)**
> The following configuration rarely changes after initial establishment. Placing it at the top of the file maximizes the utilization of the LLM underlying Prompt Caching (Token caching) mechanism, saving substantial re-read costs.

## 1. Project Overview (Overview)
- **Project Goal**: [Fill in the goal determined through discussion]
- **Core Value**: [e.g., improve efficiency, reduce costs, provide a unique experience]

## 2. Target Audience (Target Audience)
- **Persona 1**: [e.g., Tech Blogger - needs minimal configuration, one-click generation.]
- **Persona 2**: [If applicable, fill in other user personas]

## 3. Boundaries & Scope (Scope & Non-Goals)
### 3.1 Clearly In-Scope
- Develop according to the project's data structures and mechanisms; ensure code is correctly added to the project
- Generated content conforms to mechanism logic
- [Fill in other core scopes confirmed during discussion]

### 3.2 Clearly Out-of-Scope / Non-Goals
- **Non-Goal**: Avoid excessive intrusion into existing project files unless necessary
- [Fill in items confirmed as out-of-scope during discussion]

## 4. Non-Functional Requirements (Non-Functional Requirements)
- **Comments**: Generated code needs Chinese comments added in reasonable places, formatted as "/*-- comment content --*/"
- **Code Quality**: Generated code must be concise and highly readable
- **Other Requirements**: [e.g., performance, compatibility requirements]

## 5. Success Metrics (Success Metrics)
- Evaluated by internal personnel on whether functionality is usable
- [Other success metrics confirmed during discussion]

## 6. Definition of Done (DoD)
- [ ] All code must pass Linter static checks with no warnings or errors.
- [ ] No `TODO` or `FIXME` remains in core logic code.
- [ ] If `mcp/server-memory` is enabled, corresponding session memory has been serialized and written back to `8.2 Memory Snapshot`.
- [ ] The `9. Evaluation Report (Evaluator)` section has been reserved for the evaluation agent to overwrite.
- [ ] [Other engineering or business-level completion criteria]

---

> **Incremental Section (Slow-Changing Incremental Section)**
> Contains core feature acceptance criteria and engineering index. May be slightly modified during iterative development.

## 7. Core Features & Acceptance Criteria (Features & Acceptance Criteria)
### Feature 1: [Feature Name]
- **Description**: [High-level business logic description]
- **Implementation Requirements**: [High-level technical requirements, module boundary constraints]
- **Acceptance Criteria (AC)**:
  - [ ] [Criterion 1]
  - [ ] [Criterion 2]

*(Based on records, list all confirmed features sequentially...)*

## 8. Engineering & Knowledge Index Appendix (Context Appendix)
### 8.1 Engineering File Index & Knowledge Index (Main Index)
- **File Path**: [] | **File Purpose**: [] | **Association Reason**: []
- **Knowledge Entry**: [] | **Knowledge Summary**: [] | **Priority**: []

### 8.2 Memory Snapshot (Only Store Graph Index Node Summaries)
> **Note**: Markdown only retains the "trunk" (high-level skeleton/outline) of knowledge nodes. Leaf nodes (specific code logic relationships, detailed context constraints) are entirely stored in `mcp/server-memory`. Below only records node IDs and their brief names.
- **Associated Nodes List (Pointer only)**: [Fill in associated node entity names/IDs]
- **Associated Relation Outline**: [Fill in the general direction of topological relationships between core nodes]

### 8.3 Requirement-Related Incremental Index References
- [Refer to skill specification; only record incremental differences]

---

> **Dynamic Section (High-Frequency Volatile Section)**
> Overwritten by sub-agents every iteration round. Placed at the very end of the file to prevent its frequent changes from invalidating the cached Tokens of the large static text above.

## 9. Evaluation Report (Evaluator Reserved Section)
### 9.1 Most Recent Evaluation Metadata
- **Evaluator/Agent**: [evaluatorX]
- **evaluation_mode**: [full | incremental]
### 9.2 Requirement Compliance Overview
*(Table)*
### 9.3 Code Issue List
*(Table)*
### 9.4 Optimization Suggestions
*(Table)*
### 9.5 Comprehensive Evaluation Conclusion
[]

## 10. Iteration Checkpoints (Incremental Checkpoints)
> **Note**: This section is automatically managed by the orchestrator, recording traceable checkpoints at each key iteration. Sub-agents must not manually modify the content of this area.

*(Checkpoint record example)*
<!-- - **#CP-1** | **Time**: 2025-01-01T10:00:00Z | **Phase**: coder implementation complete | **Trigger**: auto
  - **Completed Features**: [Login Module - Form Validation]
  - **Core Modified Files**: [src/auth/login.ts, src/utils/validator.ts]
  - **Git Status**: a1b2c3d (commit hash) or unstaged
  - **Evaluation Result**: Not Audited -->
