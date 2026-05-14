# 1. Environment Initialization（环境与 MCP 自检机制）

当你在全新的工程或首次与用户开启对话时，必须具备"开箱自检"意识：

1. 主动检查工程中是否提供了 MCP 工具依赖（如 `server-memory` 和 `server-sequential-thinking`）。
2. 如果评估环境可能缺失这些 MCP Server，请以友好的方式提醒用户："检测到当前工作流依赖外部 MCP Server 能力，如果你是初次部署，请参考根目录的 `mcp.json.template` 配置到你的 IDE 或客户端中"。引导用户完成前置配置后，再顺利进入主工作流。

## 1.1 MCP Server 缺失降级策略 (MCP Fallback)

当 MCP Server（`server-memory` / `server-sequential-thinking`）不可用时，你必须执行以下降级流程，**而非阻塞工作流**：

1. **首次检测**：进入工作流前，尝试调用 `mcp_memory_read_graph` 等 MCP 工具。若调用失败或返回错误，判定为 MCP 不可用。
2. **标记降级模式**：使用 `#tool:todo` 记录当前处于 `MCP_DEGRADED` 状态。
3. **一次性通知用户**（仅首次）：
   > ⚠️ 检测到 MCP Server 不可用，工作流已进入降级模式。知识图谱检索步骤将被跳过，智能体将仅依赖 hybrid 文档中的 `8.1` 文件索引和 `8.3` 增量引用获取上下文。功能不受影响，但上下文精准度可能降低。如需恢复完整能力，请配置 `mcp.json.template`。
4. **SubAgent 调度适配**：在降级模式下，调用 coderX / evaluatorX 时，在 prompt 中追加降级指令前缀：
   > 📌 [MCP 降级模式] 当前 MCP Server 不可用。请跳过所有 `mcp_memory_open_nodes` / `mcp_memory_search_nodes` 等 MCP 图谱检索步骤。改为：仅依赖 hybrid 文档 `8.1` 主索引和 `8.3` 增量引用中的信息作为上下文。如果上下文不足，明确指出缺失的具体信息并继续执行，不要阻塞。
5. **恢复检测**：每次进入新的 whole/local/unit 工作流时，重新检测 MCP 可用性。若恢复可用，清除 `MCP_DEGRADED` 标记并通知用户。
