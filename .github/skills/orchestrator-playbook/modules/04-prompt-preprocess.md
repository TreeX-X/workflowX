# 4. Prompt Preprocessing Rules（Prompt 预处理规则）

promptMasterX 是一个轻量 prompt 预处理智能体。职责单一：将用户的原始需求文本优化为高质量、无歧义、结构化的 prompt，然后交给下游智能体执行。

**调用方式**：使用 `#tool:agent/runSubagent` 调用 `promptMasterX`，将原始需求文本作为 prompt 传给它。

## 4.1 跳过规则（优先于自动触发规则）

当用户输入满足以下**任一**条件时，直接跳过 promptMasterX，将原始需求直传下游智能体：
- 输入长度 **≤ 30 字符**（去除首尾空格后）— 短指令本身已足够精炼
- 输入中**包含明确的文件路径**（如 `src/foo.ts`、`lib/bar.py`）**或函数名**（如 `getUserInfo`、`handleLogin`）— 精确指向无需优化

> 💡 理由：短指令已精炼、含路径/函数名的指令已精确，promptMasterX 优化只会增加额外开销且不产生价值。

## 4.2 自动触发规则

| 模式 | 场景 | 是否调用 promptMasterX | 说明 |
|---|---|---|---|
| `/unit` | 调用 coderX 前 | ✅ 自动调用 | 优化用户需求 + 原始需求一并传给 coderX |
| `/local` | 首次调用 coderX 前 | ✅ 自动调用 | 同上 |
| `/whole` | planner 阶段 | ❌ 不调用 | planner 阶段需要保留原始意图进行对话澄清 |
| `/whole` | coder 阶段（PRD 确认后） | ❌ 不调用 | PRD 本身已是结构化的 |
| `/whole` | evaluator 打回后修复轮 | ✅ 自动调用 | 将 evaluator 建议 + 用户补充合并优化后再传给 coderX |
| `/prompt` | 直接调用 | ✅ | 不进入任何工作流，仅做 prompt 工程 |

**传递规范**：优化后的 prompt 作为主体传给下游智能体，同时在上下文中附上原始需求文本，以防止意图丢失。
