---
name: wiki-creater
description: "构建并维护 Wiki 知识库。触发词：ingest、摄入、知识库、wiki、概念页、来源摘要。负责从 src/content/knowledge-base 只读提炼信息，并写入 src/content/wiki。"
---

# Wiki Cteater Skill

你具有最高的文件读写权限修改 `src/content/wiki` 目录，但对 `src/content/knowledge-base` 目录只有只读权限。

## 目录结构规范
- `src/content/wiki/index.md`：全局索引目录。
- `src/content/wiki/log.md`：按时间倒序排列的操作日志（Append-only）。
- `src/content/wiki/concepts/`：核心概念与专业术语页面。
- `src/content/wiki/sources/`：单篇原始文献的摘要总结。

## 核心工作流：Ingest（知识库建立与编译）
当我向你发送指令“请 ingest（摄入）文件 [文件名]”时，你必须严格按顺序执行以下 7 步工作流：

1. **全量读取**：仔细阅读 `src/content/knowledge-base/` 目录下该文件的全部内容。
2. **提取摘要**：在 `src/content/wiki/sources/` 下建立对应的摘要页面，并包含关键结论、可复用方法、相关概念链接。
3. **实体与概念更新**：提取文章中的核心概念/技术栈。去 `src/content/wiki/concepts/` 检查是否已有同名文件。
   - 如果有，将新知识增量合并进去，并保留历史观点。
   - 如果没有，创建新文件，并补全定义、边界和示例。
4. **建立双向链接**：使用 `[[页面名称]]` 的格式（兼容 Obsidian）在文件之间添加交叉引用链接。
5. **矛盾排查**：如果新摄入的观点与 Wiki 中已有的观点冲突，不要覆盖，而是在页面中添加 `⚠️ 矛盾 (Contradiction)` 章节，并保留双方观点及适用条件。
6. **更新索引**：在 `src/content/wiki/index.md` 中更新受影响的目录结构。
7. **写入日志**：在 `src/content/wiki/log.md` 的末尾追加一条记录，格式为 `## [YYYY-MM-DD] Ingest | 处理了 [文件名]`。

## 约束条件
- 所有输出必须使用结构化的 Markdown。
- 保证生成的知识库具有“复利效应”，不要遗漏任何具有长期价值的思考。
- 如果信息不充分，明确标注“待补充”，不得臆造事实。
