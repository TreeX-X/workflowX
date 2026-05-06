# Auto-Compress Hybrid Docs (自动压缩技能)

**描述 (Description)**: A specialized skill for `evaluatorX` to compress bloated Hybrid Documents and consolidate fragmented Knowledge Graph entities when specific thresholds are met.

此技能专门赋予 Evaluator 智能体，在检测到 Hybrid 文档过度膨胀时，进行高度智能化的上下文提炼与记忆重构。

---

## 1. 触发阈值规则 (Trigger Conditions)

当 Evaluator 读取到 Hybrid Document（或 product-spec-context.md）时，如果触发以下任一标准，必须在执行常规 Evaluation 之前或之后叠加执行本压缩技能：
- **体积阈值**：文件大小超过 **15KB**。
- **行数阈值**：文档总行数超过 **300行**。

## 2. 操作规范 (Compression Workflow)

按照以下三个步骤执行知识压缩：

### Step 1: 文档索引提炼 (Markdown Compression)
- **目标**：吞下因多轮迭代导致的膨胀 Markdown，尤其是 `8. 工程与知识索引附录`。
- **行动**：提取那些细碎的、罗列式的知识条目与工程文件说明。例如，将 20 条零散的知识索引归纳整理、合并、提炼为 **3 至 5 条包含“核心大意”与“抽象规则”的精炼说明**。
- **边界约束**：务必遵守 Prompt Caching 阵列结构（静态区、增量区、动态区）。不要篡改头部的背景、DoD 准则等。压缩重点完全放在知识库碎片上，保证压缩后的全文行数回到健康区间（<300行）。

### Step 2: 知识图谱碎片清理 (Graph Operation - Cleanup)
- **目标**：与 `mcp/server-memory` 联动，彻底清除无效与废弃的边缘图谱记忆，防止图谱过度蔓延。
- **行动**：主动调用工具 `mcp_memory_delete_entities` 和 `mcp_memory_delete_relations`，销毁上一阶段因为增量迭代留下的零碎 Entity 和孤立 Relation。

### Step 3: 图谱宏观实体归并 (Graph Operation - Consolidation)
- **目标**：建立单一的、包含核心上下文的“超大宏观模块”。
- **行动**：根据第一步的提炼结果，调用工具 `mcp_memory_create_entities`，将零散知识彻底打包，录入成为一个包含“整体架构核心大意”的单体超大 `Module_Entity` 或者 `System_Context_Entity`。
- **持久化回写**：更新 Hybrid 文档的 `8.2 Memory Snapshot`，用新的大实体快照替换旧快照，保证文件态和 MCP Server态完全同步。

## 3. 验收标准 (Success Criteria)
1. 压缩操作后，混合文档的总行数明确下降到 300 行以下，且索引区变得高度摘要。
2. 明确发起了 `mcp_memory_delete_*` 和 `mcp_memory_create_*` 的工具调用。
3. 压缩后没有丢失项目的核心非功能性要求或顶层的 DoD 约定。