# 3. Incremental Checkpoint & Rollback (Incremental Checkpoint & Rollback Mechanism)

To prevent implementation drift from progressing further, traceable checkpoints must be recorded at key iteration nodes, allowing humans to roll back to any passed intermediate state at any time.

## 3.1 Checkpoint Write Rules

1. **Write Timing**: When the following events occur, the orchestrator must automatically append a checkpoint record to the `10. Iteration Checkpoints` section of the current hybrid document:
   - After coderX completes implementation and outputs a qualified Payload (i.e., before entering evaluatorX)
   - After evaluatorX returns `PASS` (i.e., this iteration round fully passed)
   - After user manually executes `/rollback` successfully (record the restored target state)
2. **Checkpoint Content** (must contain the following fields):
   ```
   - **#CP-[Number]** | **Time**: [ISO Time] | **Phase**: [coder implementation complete | evaluation passed] | **Trigger**: [auto | /rollback]
     - **Completed Features**: [List of features completed in this round]
     - **Core Modified Files**: [File path list]
     - **Git Status**: [Current commit hash or "unstaged" status]
     - **Evaluation Result**: [Passed | Not Audited | Needs Fix]
   ```
3. **Numbering Rule**: `#CP-1`, `#CP-2`... incrementing, counting from the start of the workflow.
4. **Limit**: Retain at most the most recent **10** checkpoint records. When exceeded, delete the oldest entries (but retain the initial `#CP-1` checkpoint).

## 3.2 Rollback Execution Flow (`/rollback`)

When the user issues `/rollback [number]`:

1. Read the hybrid document `10.*` section and locate the target checkpoint.
2. Execute `git checkout -- [core modified file list]` to revert the code to the file state recorded at that checkpoint.
   - If the checkpoint recorded a commit hash, use `git reset --hard [hash]` to revert.
   - If it was an unstaged state, use `git checkout -- .` for full revert.
3. **Overwrite** the hybrid document's `9.*` evaluation section to its initial empty state.
4. **Truncate** the `10.*` section: delete all checkpoint entries after the target number.
5. Confirm the rollback result to the user and ask about next intentions (continue development / switch mode / summarize).
6. Write the rollback event as a new checkpoint in `10.*` (trigger marked as `/rollback`).

> **Safety Constraint**: Rollback operations will discard all changes after the target checkpoint. Before execution, must display a summary of changes to be discarded and obtain user confirmation (unless the user appended the `-y` force parameter in the command).

## 3.3 Parallel Mode Checkpoint Rules

When using the `-parallel` parameter, the checkpoint mechanism has the following special rules:

1. **Shadow Doc Internal Checkpoints**: Each parallel task's shadow doc maintains an independent local checkpoint sequence, numbered with task prefix (`#CP-A1`, `#CP-A2`, `#CP-B1`, etc.).
2. **Master Doc Freeze**: During parallel execution, the master doc's Section 10 **does not write** any checkpoints. Only unified writes during the merge phase.
3. **Merge Checkpoint**: After all parallel tasks are complete, write a merge checkpoint in the master doc Section 10:
   ```
   - **#CP-[N]** | **Time**: [ISO Time] | **Phase**: All parallel tasks complete | **Trigger**: auto
     - **Completed Tasks**: [Task A: {name}] [Task B: {name}]
     - **Failed Tasks**: [Task X: {name} -- reason] (if any)
     - **Core Modified Files**: [Complete file list after merge]
     - **Git Status**: [commit hash or "unstaged"]
     - **Evaluation Result**: [All Passed | Partially Passed]
   ```

## 3.4 Parallel Mode Rollback Abort

When `/rollback` is received during parallel execution:
1. **Abort** all running task pairs (no longer waiting for their return).
2. **Delete** all shadow doc files.
3. If `-box` was used: **Delete** all parallel task branches (`git branch -D {branch_name}`).
4. **Execute standard rollback** process on the master doc (see Section 3.2).
