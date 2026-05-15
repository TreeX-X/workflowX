# 5. Status Report Specification (`/status`)

`/status` is a **read-only, zero side-effect** reactive command. When executed, it quickly extracts structured information from the current hybrid document and presents it to the user as a concise list, **without writing anything to the hybrid document**.

## 5.1 Execution Flow

1. Read the current hybrid document.
2. Extract the following information and assemble as summary output:

## 5.2 Output Format

```markdown
## WorkflowX Status Report

**Current Mode**: [whole / local / unit]
**Branch**: [If `-b` is enabled, show the working branch name; otherwise show the current git branch]

### Completed Work
- [Feature/module name] -- completed at #CP-[number], evaluation result: [PASS / Not Audited]
- ...

### In Progress / Incomplete Work
- [Feature/module name] -- Status: [coder implementing / Pending Evaluation / Evaluation Rejected - Fixing]
  - Most recent evaluation issue: [P0/P1 issue summary, if any]
- ...

### Most Recent Checkpoint
- #CP-[latest number]: [Phase] | [Time] | [Completed Features]
```

## 5.3 Information Extraction Rules

- **Completed**: Extract entries from the `10. Iteration Checkpoints` section where the phase is "evaluation passed", listing their completed features.
- **Incomplete/In Progress**:
  - Check if the `9. Evaluation Report` section has records with "Evaluation Conclusion = Needs Fix" -> Mark as "Evaluation Rejected - Fixing".
  - If the latest checkpoint in `10.*` phase is "coder implementation complete" with no corresponding "evaluation passed" record -> Mark as "Pending Evaluation".
  - If neither of the above matches but unchecked DoD items exist in the hybrid document (`6.*` section) -> List unchecked items, marked as "Pending Completion".
- **Branch Information**: Execute `git branch --show-current` via `#tool:execute/runInTerminal` to obtain.
- **No hybrid document**: Output "No active hybrid document currently exists. Please first use `/whole`, `/local`, or `/unit` to start a workflow."

## 5.4 Parallel Mode Status Display

When in `-parallel` parallel execution, `/status` additionally displays parallel task status:

```markdown
### Parallel Task Progress
- **Task A** ({name}): [coder implementing / Pending Evaluation / Evaluation Passed / Needs Fix / FAILED]
- **Task B** ({name}): [Status]
- **Task C** ({name}): [Status]

**Overall Progress**: {completed count}/{total} tasks complete
```

Information source: Read each shadow doc filename (`*.TASK-*.md`) and its Section 9 evaluation conclusion.
