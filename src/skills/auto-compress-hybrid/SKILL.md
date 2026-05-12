# Auto-Compress Hybrid Docs (渐进式自动压缩技能)

**描述 (Description)**: A progressive compression skill for `evaluatorX` to manage Hybrid Document bloat through multi-level compression strategies, adapted to document size.

此技能为 Evaluator 智能体提供**渐进式**的文档压缩能力。根据膨胀程度自动选择轻量、标准或深度压缩策略，避免过度压缩导致信息丢失。

---

## 1. 压缩等级与触发阈值 (Progressive Compression Levels)

| 等级 | 标识 | 体积阈值 | 行数阈值 | 压缩策略 |
|------|------|---------|---------|---------|
| **L0 健康** | `healthy` | < 10KB | < 200 行 | 无需压缩，跳过 |
| **L1 轻量** | `light` | 10 ~ 15KB | 200 ~ 300 行 | 仅执行文档索引去重与冗余裁剪 |
| **L2 标准** | `standard` | 15 ~ 25KB | 300 ~ 500 行 | 文档索引提炼 + 知识图谱碎片清理 |
| **L3 深度** | `aggressive` | > 25KB | > 500 行 | 全量压缩：索引提炼 + 图谱清理 + 归并 + 历史检查点归档 |

> **判定规则**：取体积和行数中**较高的等级**作为执行等级。例如文件 12KB 但 450 行 -> 执行 L2。

## 2. 各等级操作规范

### L1 轻量压缩 (Light Compression)
仅处理 Markdown 层面的冗余，不触碰知识图谱：

1. **索引去重**：扫描 `8.1` 工程文件索引，合并重复文件路径条目。
2. **增量区精简**：扫描 `8.3` 需求相关索引增量引用，删除已被合并进 `8.1` 主索引的过期增量条目。
3. **检查点归档**：若 `10.*` 区块超过 5 条记录，仅保留 `#CP-1`、最近 3 条和所有 `PASS` 状态的检查点，删除其余。
4. **目标**：将文档降至 200 行以下。

### L2 标准压缩 (Standard Compression)
在 L1 基础上增加知识图谱操作：

5. **知识条目提炼**（继承 L1）：将 `8.1` 中细碎的、罗列式知识条目归纳整理、合并为 **3 至 5 条包含核心大意与抽象规则的精炼说明**。
6. **图谱碎片清理**：调用 `mcp_memory_delete_entities` 和 `mcp_memory_delete_relations`，销毁增量迭代留下的零碎 Entity 和孤立 Relation。
7. **边界约束**：务必遵守 Prompt Caching 阵列结构（静态区、增量区、动态区）。不要篡改头部的背景、DoD 准则等。压缩重点放在知识库碎片和增量区上。
8. **目标**：将文档降至 300 行以下。

### L3 深度压缩 (Aggressive Compression)
在 L2 基础上执行全局重构：

9. **图谱宏观实体归并**：调用 `mcp_memory_create_entities`，将零散知识打包成为包含整体架构核心大意的单体超大 `Module_Entity` 或 `System_Context_Entity`。
10. **持久化回写**：更新 `8.2 Memory Snapshot`，用新大实体快照替换旧快照，保证文件态和 MCP Server 态完全同步。
11. **静态区瘦身**：对 `1-6` 静态区中的冗余描述进行精简（保留核心约束，删除冗余示例和说明性文字）。
12. **检查点截断**：`10.*` 仅保留 `#CP-1` 和最近 1 条检查点。
13. **目标**：将文档降至 500 行以下。

## 3. 验收标准 (Success Criteria)
1. 压缩等级判定准确（不遗漏、不过度）。
2. 压缩后文档行数降至对应等级的目标值以下。
3. 未丢失项目的核心非功能性要求或顶层 DoD 约定。
4. L2/L3 压缩后明确发起了 `mcp_memory_delete_*` 工具调用（MCP 降级模式下跳过此条）。
5. L3 压缩后明确发起了 `mcp_memory_create_*` 工具调用（MCP 降级模式下跳过此条）。
6. 每次压缩后，在 hybrid 文档 `9.1` 元信息中追加 `last_compression: [等级]-[ISO时间]` 记录。
