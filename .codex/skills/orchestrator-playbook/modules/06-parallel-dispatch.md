# 6. Parallel Dispatch & Merge (Parallel Dispatch & Merge Mechanism)

This module is triggered when the user uses the `-parallel` parameter. It defines the complete procedure from task decomposition to parallel dispatch to result merging.

## 6.1 Trigger Conditions

- Command format: `/whole -parallel [requirement]` or `/whole -box -parallel [requirement]`
- Execution timing: After plannerX confirms the PRD, before the first call to coderX
- Limitation: `-parallel` only supports `/whole` mode (requires PRD Section 7 as task decomposition basis)

## 6.2 Task Decomposition Flow

After plannerX confirms the PRD, orchestratorX executes the following decomposition steps:

1. **Read Section 7** (Features & Acceptance Criteria), extract for each feature:
   - AC item numbers and descriptions
   - Expected files to modify/create
   - Functional dependency relationships (whether it imports files that other features will create)

2. **Parallelism Determination** (hard rules; all must be satisfied for parallelism):
   - **File Set Mutual Exclusion**: Target file sets of two tasks have no intersection
   - **No Import Coupling**: Task B does not depend on files that Task A will create
   - **Shared Config Isolation**: Do not simultaneously modify `package.json`, `tsconfig.json`, or other shared configuration files
   - **AC Completeness**: Each task contains a complete feature AC set; do not split a single AC

3. **Grouping Strategy** (soft constraints):
   - Maximum parallelism recommended <= 3 pairs
   - Prioritize grouping by directory/module affinity
   - Features with strong dependency relationships should be serialized even if file sets are mutually exclusive

4. **Output Grouping Plan**, format below, awaiting user confirmation:

```markdown
## Parallelization Analysis

Based on Section 7, identified {N} parallelizable task groups:

**Task A** -- `{Feature Name}`
  - AC: {number list}
  - Target Files: `{path list}`
  - Complexity: {Low/Medium/High}

**Task B** -- `{Feature Name}`
  - AC: {number list}
  - Target Files: `{path list}`
  - Complexity: {Low/Medium/High}

**Conflict Detection**: {None / Conflicts Detected}
**Must Serialize Tasks**: {list (if any)}

Confirm parallel dispatch? (yes / no / adjust)
```

5. After user replies `yes`, enter Shadow Doc creation phase; `adjust` allows user to manually adjust grouping.

## 6.3 Shadow Doc Creation Rules

For each confirmed parallel task T:

1. **Copy master hybrid doc** -> `{master-name}.TASK-{T.id}.md`
2. **Filter Section 7**: Only retain the AC items for this task, add scope annotation at the top:
   ```markdown
   > This file is the working document for Task {T.id}
   > Please only complete the following AC items:
   > - {AC number}: {description}
   > - ...
   >
   > Write Constraint: Only modify Section 8.2 (Memory Snapshot) and Section 9 (Evaluation Report).
   > Prohibited from modifying Section 1-7, 8.1, 8.3, 10.
   ```
3. **Section 10**: Add task prefix marker `<!-- TASK_ID: {T.id} -->` at the top
4. If `-box` is used: Create isolation for each task
   - **Claude Code**: Use `EnterWorktree` to create an independent worktree per task. Worktree naming: `parallel-{TASK-ID}-{short-summary}`. This provides true filesystem-level isolation without branch switching.
   - **Codex / Copilot**: Fall back to independent branch per task. Branch naming: `wfx/parallel-{TASK-ID}-{short-summary}-{YYYYMMDD-HHmm}`. Example: `wfx/parallel-A-feat-auth-20260514-1530`

## 6.4 Dispatch Specification

### 6.4.1 Prompt Construction

Construct independent prompts for each task pair (coderX + evaluatorX), must include:

- **shadow doc path**: As the hybrid doc for this task
- **Filtered requirement description**: Only this task's AC items
- **Write constraint instruction**: "Only modify Section 8.2 and Section 9; prohibited from modifying other areas"
- **Bus Payload requirement**: Must include `task_id` field (refer to module 02)
- **Task ID marker**: Mark `Task {T.id}` at the beginning of the prompt

### 6.4.2 Dispatch Order

Dispatch strategy depends on the current platform's capabilities:

#### Platform Capability Matrix

| Capability | Claude Code | Codex | Copilot |
|---|---|---|---|
| Sub-agent dispatch | `Agent` tool | Sub-agent scheduling | `agent/runSubagent` + handoffs |
| Background parallel | `run_in_background: true` | Not supported | Not supported |
| Worktree isolation | `EnterWorktree` / `ExitWorktree` | Not supported | Not supported |

Detect the platform at runtime (check available tools / config). Use the corresponding dispatch mode below.

#### Mode CC (Claude Code): True Pipeline Parallel

Use `run_in_background: true` to launch sub-agents concurrently. As each coderX completes, immediately launch its evaluatorX without waiting for other tasks.

```
t0:  coderX-A [bg]  coderX-B [bg]  coderX-C [bg]
     (all three run concurrently)

t1:  coderX-A finishes -> immediately launch evaluatorX-A [bg]
     (coderX-B and coderX-C still running)

t2:  evaluatorX-A finishes -> PASS, task A done
     coderX-B finishes -> immediately launch evaluatorX-B [bg]

t3:  evaluatorX-B finishes -> Needs Fix -> launch coderX-B(fix) [bg]
     coderX-C finishes -> immediately launch evaluatorX-C [bg]
     ...pipeline continues...
```

Orchestrator maintains a **task state table**, polling for completed background agents:

| Task | Phase | Status |
|---|---|---|
| A | coderX | running / done / failed |
| A | evaluatorX | pending / running / done / PASS / NeedsFix |
| B | coderX | ... |

**Completion detection**: After launching all initial coderX calls, enter a poll loop:
1. Check which background agents have completed
2. For each completed coderX: validate Payload -> launch evaluatorX [bg]
3. For each completed evaluatorX: validate Payload -> if PASS mark done, if NeedsFix launch coderX(fix) [bg] (if iterations remain)
4. Repeat until all tasks are done or max iterations reached

**Key rule**: There is NO barrier. Do NOT wait for all coderX to finish before starting any evaluatorX. Each task flows independently through its own coder->evaluator pipeline.

#### Mode Serial (Codex / Copilot): Per-Task Chain

No background parallel available. Instead of round-robin with full barrier, dispatch **per-task serial chains**:

```
Chain A: coderX-A -> evaluatorX-A -> PASS ✅ (or NeedsFix -> coderX-A(fix) -> evaluatorX-A)
Chain B: coderX-B -> evaluatorX-B -> PASS ✅
Chain C: coderX-C -> evaluatorX-C -> PASS ✅
```

**Key improvement over old round-robin**: Each task's coder->evaluator pair runs as a complete unit. Task A's evaluator does NOT wait for Task C's coder to finish. This breaks the "all coderX must complete before any evaluatorX" barrier.

Execute chains sequentially: run Chain A to completion (including all fix iterations), then Chain B, then Chain C. Within each chain, iterations follow the normal coder->evaluator loop until PASS or max iterations.

After each coderX/evaluatorX returns, immediately validate its Bus Payload (including task_id) per module 02.

### 6.4.3 Iteration Limit

Each task pair **counts independently**, default 2 times (controlled by `-N` parameter). If a task reaches maximum iterations and still does not PASS, mark it as FAILED without affecting other tasks' continuation.

## 6.5 Result Merge Flow

After all tasks complete (or partially fail), orchestratorX executes the merge:

### 6.5.1 Code Merge

| Mode | Platform | Operation |
|---|---|---|
| `-parallel` (no -box) | All | All tasks work on the same branch; verify `git diff --check` has no conflicts |
| `-box -parallel` | Claude Code | Each task completed in its own worktree. Merge via `git merge` from worktree branches. No branch switching needed. |
| `-box -parallel` | Codex / Copilot | Switch back to original branch; sequentially `git merge --no-ff` each task branch |

Pre-merge audit: `git diff --name-only` for each task branch/worktree, compare declared file sets, detect out-of-scope modifications.

**Worktree merge procedure** (Claude Code `-box -parallel`):
1. After all tasks complete, return to original branch (call `ExitWorktree` per task or orchestrate from main)
2. For each successful task worktree: `git merge --no-ff {worktree-branch}`
3. For conflicts: stop and report to user with conflicting files
4. After all merges: `ExitWorktree action=remove` for successful worktrees; `action=keep` for failed task worktrees

### 6.5.2 Hybrid Doc Merge

| Section | Merge Strategy |
|---|---|
| **8.2 Memory Snapshot** | Aggregate all shadow doc 8.2 content, prefix each entry with `[Task {id}]` |
| **9 Evaluation Report** | Append each task's evaluation report, separated by `## Task {T.id} Evaluation`; write overall summary at top |
| **10 Checkpoints** | Append each shadow doc's checkpoints, maintaining global number increment |

### 6.5.3 Merge Checkpoint

Write a merge checkpoint in master doc Section 10:
```
- **#CP-[N]** | **Time**: [ISO Time] | **Phase**: All parallel tasks complete | **Trigger**: auto
  - **Completed Tasks**: [Task A: {name}] [Task B: {name}] ...
  - **Failed Tasks**: [Task X: {name} -- reason] ... (if any)
  - **Core Modified Files**: [Complete file list after merge]
  - **Git Status**: [commit hash or "unstaged"]
  - **Evaluation Result**: [All Passed | Partially Passed]
```

### 6.5.4 Cleanup

- Successful task shadow docs -> **Delete**
- Failed task shadow docs -> **Retain** for debugging
- `-box -parallel` task branches -> **Not automatically deleted**; user decides

## 6.6 Error Handling

| Scenario | Handling |
|---|---|
| **Single Task Failure** | Does not affect other tasks continuing; merge results of successful tasks; report failed task details |
| **All Failed** | Do not merge any results; master doc retains pre-parallel state; retain all shadow docs |
| **File Out-of-Scope** | coderX modified unassigned files -> detected in pre-merge audit -> mark and report to user |
| **Payload Validation Failure** | Retry once per module 02 rules; if still failed, mark the task as FAILED |
| **Runtime Crash** | Catch exception, log, continue executing remaining tasks |

### Single Task Failure Report Format:
```markdown
## Parallel Execution Results

PASS: Task A ({name}), Task C ({name})
FAILED: Task B ({name}) -- reached maximum iteration count {N}, evaluation did not pass

**Task B Last Evaluation Summary**: {evaluatorX's P0/P1 issues}

**Recommended Next Steps**:
1. Manually fix Task B
2. Re-run: `/whole -parallel --retry TASK-B`
3. Or continue using already merged partial results
```

## 6.7 Interaction with `-box` Parameter

- `/whole -parallel` (no -box): All tasks work on the same branch; shadow docs provide document-level isolation
- `/whole -box -parallel` (Claude Code): Each task gets an independent git worktree via `EnterWorktree`; document + filesystem double isolation. No branch switching overhead.
- `/whole -box -parallel` (Codex / Copilot): Each task gets an independent git branch; document + branch double isolation
- Command parameter order is flexible: `/whole -box -parallel` = `/whole -parallel -box`

## 6.8 Interaction with `/rollback`

When `/rollback` is received during parallel execution:
1. **Abort** all running task pairs (stop any background agents if in CC pipeline mode)
2. **Delete** all shadow docs
3. If `-box` was used:
   - **Claude Code**: `ExitWorktree action=remove discard_changes=true` for all task worktrees
   - **Codex / Copilot**: **Delete** all task branches (`git branch -D`)
4. **Execute standard rollback** process on the master doc (refer to module 03)

## 6.9 Interaction with `/status`

During parallel execution, `/status` output must additionally display:
- Current status of each parallel task (coder implementing / Pending Evaluation / Evaluation Passed / Needs Fix / FAILED)
- Overall progress (e.g., 2/3 tasks complete)
- Most recent parallel checkpoint

(Refer to module 05 for parallel status display format)
