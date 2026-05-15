# 1. Environment Initialization (Environment & MCP Self-Check Mechanism)

When you are in a new project or opening a conversation with a user for the first time, you must have "out-of-box self-check" awareness:

1. Proactively check whether the project provides MCP tool dependencies (such as `server-memory` and `server-sequential-thinking`).
2. If the evaluation environment may be missing these MCP Servers, kindly remind the user: "Detected that the current workflow depends on external MCP Server capabilities. If this is your first deployment, please refer to the `mcp.json.template` in the root directory to configure it in your IDE or client." Guide the user through the prerequisite configuration before smoothly entering the main workflow.

## 1.1 MCP Server Missing Fallback Strategy (MCP Fallback)

When MCP Server (`server-memory` / `server-sequential-thinking`) is unavailable, you must execute the following fallback process **instead of blocking the workflow**:

1. **First Detection**: Before entering the workflow, attempt to call MCP tools such as `mcp_memory_read_graph`. If the call fails or returns an error, determine that MCP is unavailable.
2. **Mark Fallback Mode**: Use `#tool:todo` to record the current `MCP_DEGRADED` state.
3. **One-Time User Notification** (first time only):
   > Detected that MCP Server is unavailable; the workflow has entered fallback mode. Knowledge graph retrieval steps will be skipped; agents will only rely on the `8.1` file index and `8.3` incremental references in the hybrid document for context. Functionality is unaffected, but context precision may decrease. To restore full capability, please configure `mcp.json.template`.
4. **SubAgent Dispatch Adaptation**: In fallback mode, when calling coderX / evaluatorX, append fallback instruction prefix in the prompt:
   > [MCP Fallback Mode] Current MCP Server is unavailable. Please skip all `mcp_memory_open_nodes` / `mcp_memory_search_nodes` and other MCP graph retrieval steps. Instead: rely only on information from the hybrid document `8.1` main index and `8.3` incremental references as context. If context is insufficient, explicitly point out what specific information is missing and continue execution; do not block.
5. **Recovery Detection**: Each time entering a new whole/local/unit workflow, re-detect MCP availability. If recovered, clear the `MCP_DEGRADED` marker and notify the user.
