请调用 orchestratorX 智能体，以单元模式（Mode C: unit）执行以下需求。

用户输入：$ARGUMENTS

执行流程：
1. 调用 promptMasterX 优化执行指令（模块 04）
2. 调用 coderX 执行最小化修改
3. 向用户报告完成，evaluatorX 仅在用户明确要求时调用
