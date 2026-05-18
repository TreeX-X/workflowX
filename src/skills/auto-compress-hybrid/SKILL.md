# Auto-Compress Hybrid Docs (Progressive Auto-Compression Skill)

**Description**: A progressive compression skill for `evaluatorX` to manage Hybrid Document bloat through multi-level compression strategies, adapted to document size.

This skill provides **progressive** document compression capability for the Evaluator agent. Based on the degree of bloat, it automatically selects light, standard, or deep compression strategies to avoid information loss from over-compression.

---

## 1. Compression Levels & Trigger Thresholds (Progressive Compression Levels)

| Level | Identifier | Size Threshold | Line Count Threshold | Compression Strategy |
|------|------|---------|---------|---------|
| **L0 Healthy** | `healthy` | < 10KB | < 200 lines | No compression needed, skip |
| **L1 Light** | `light` | 10 ~ 15KB | 200 ~ 300 lines | Only perform document index deduplication and redundancy trimming |
| **L2 Standard** | `standard` | 15 ~ 25KB | 300 ~ 500 lines | Document index refinement + knowledge graph fragment cleanup |
| **L3 Deep** | `aggressive` | > 25KB | > 500 lines | Full compression: index refinement + graph cleanup + merge + historical checkpoint archival |

> **Determination Rule**: Take the **higher level** between size and line count as the execution level. For example, a file of 12KB but 450 lines -> execute L2.

## 2. Operations Specification per Level

### L1 Light Compression
Only handle Markdown-level redundancy; do not touch the knowledge graph:

1. **Index Deduplication**: Scan the `8.1` engineering file index and merge duplicate file path entries.
2. **Incremental Section Refinement**: Scan the `8.3` requirement-related incremental index references and delete expired incremental entries that have already been merged into the `8.1` main index.
3. **Checkpoint Archival**: If the `10.*` section has more than 5 records, only retain `#CP-1`, the most recent 3 entries, and all checkpoints with `PASS` status; delete the rest.
4. **Goal**: Reduce the document to below 200 lines.

### L2 Standard Compression
Add knowledge graph operations on top of L1:

5. **Knowledge Entry Refinement** (inherited from L1): Consolidate and merge fragmented, enumerated knowledge entries in `8.1` into **3 to 5 refined descriptions containing core ideas and abstract rules**.
6. **Graph Fragment Cleanup**: Call `mcp_memory_delete_entities` and `mcp_memory_delete_relations` to destroy fragmented Entities and orphaned Relations left from incremental iterations.
7. **Boundary Constraints**: Must adhere to the Prompt Caching array structure (static section, incremental section, dynamic section). Do not alter the header background, DoD criteria, etc. The compression focus should be on knowledge base fragments and incremental sections.
8. **Goal**: Reduce the document to below 300 lines.

### L3 Deep Compression
Execute global restructuring on top of L2:

9. **Graph Macro Entity Merge**: Call `mcp_memory_create_entities` to package scattered knowledge into a single monolithic `Module_Entity` or `System_Context_Entity` containing the overall architecture core idea.
10. **Persistent Writeback**: Update the `8.2 Memory Snapshot`, replacing the old snapshot with the new macro entity snapshot, ensuring file state and MCP Server state are fully synchronized.
11. **Static Section Slimming**: Refine redundant descriptions in the `1-6` static sections (retain core constraints, delete redundant examples and explanatory text).
12. **Checkpoint Truncation**: `10.*` only retains `#CP-1`, the most recent 1 checkpoint, and all checkpoints with `PASS` status.
13. **Goal**: Reduce the document to below 500 lines.

## 3. Success Criteria
1. Compression level determination is accurate (no omissions, no over-compression).
2. Post-compression document line count is reduced below the target value for the corresponding level.
3. No loss of core non-functional requirements or top-level DoD agreements from the project.
4. After L2/L3 compression, `mcp_memory_delete_*` tool calls were clearly initiated (skip this criterion in MCP fallback mode).
5. After L3 compression, `mcp_memory_create_*` tool calls were clearly initiated (skip this criterion in MCP fallback mode).
6. After each compression, append a `last_compression: [level]-[ISO_time]` record in the hybrid document `9.1` metadata.
