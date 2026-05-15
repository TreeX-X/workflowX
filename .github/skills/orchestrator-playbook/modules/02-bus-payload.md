# 2. Bus Pipeline Payload Schema & Validation (Bus Payload Specification & Validation)

In the cross-agent handoff step of whole/local workflows (coderX -> evaluatorX, evaluatorX -> coderX), the upstream agent must output a structured "Bus Payload" in the conversation flow. Before handing control to the downstream agent, the orchestrator must validate whether the upstream output conforms to the Schema below; if not, it should automatically append a format correction instruction and re-invoke the upstream agent, and only pass it to the downstream agent after the Payload passes validation.

## 2.1 Payload Type 1: coderX -> evaluatorX (Phase Result Bus Payload)

coderX must output after completing implementation, containing the following **required fields**:

```markdown
### Bus Pipeline Payload: Implementation Summary
- **Completed Feature Items**: [List the PRD requirement module names or numbers completed in this round]
- **Core Modification List**:
  - [File path] -- [Modification role/logic summary]
  - ...
- **Directed Audit Request Points**: [Specify complex logic or external dependencies, prompting evaluatorX to focus review]
- **Associated Hybrid Document**: [hybrid document path]
- **Overwrite Requirement**: Please evaluatorX overwrite the evaluation report to the `9.*` section of the hybrid document
- **Task ID** (required in parallel mode): [Parallel task number, e.g., `TASK-A`; can be omitted in non-parallel mode]
```

## 2.2 Payload Type 2: evaluatorX -> coderX (Evaluation Summary Bus Payload)

evaluatorX must output after completing evaluation, containing the following **required fields**:

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
- **Task ID** (required in parallel mode): [Parallel task number, e.g., `TASK-A`; can be omitted in non-parallel mode]
```

## 2.3 Validation Rules

The orchestrator must perform the following checks after each agent returns:

1. **Required Field Check**: Every field marked with `- **Field Name**:` in the Payload must exist and be non-empty.
2. **Evaluation Result Validity**: The `Evaluation Result` field value in evaluatorX's Payload can only be `PASS` or `Needs Fix` (case-insensitive). If the value is other content, treat it as a format error.
3. **Core Modification List Non-Empty**: The `Core Modification List` in coderX's Payload must contain at least 1 file entry.
4. **Hybrid Document Path Existence**: The `Associated Hybrid Document` field should point to a reasonable document path (ending with `.md`).

**Validation Failure Handling**:
- If validation fails, **do not** pass the Payload to the downstream agent.
- Automatically append the following correction instruction and re-invoke the agent:

> Your bus Payload format does not comply with the specification; the following required fields are missing: [list missing fields]. Please re-output the complete Payload according to the Bus Pipeline Payload Schema.

- Maximum **1** retry. If the second attempt still fails, stop the process and report the format anomaly to the human developer.

**Validation Pass Handling**:
- Pass the validated Payload as the **primary context** to the downstream agent (priority higher than other information).
- Simultaneously inform the downstream agent of the "validated Payload content" so it can quickly enter its working state.
