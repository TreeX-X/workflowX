---
name: whole
description: "以全局模式（Mode A）执行完整工作流：plannerX PRD规划 → coderX编码 → evaluatorX审查"
---
请调用 orchestratorX 智能体，以全局模式（Mode A: whole）执行以下需求。

用户输入：$ARGUMENTS

执行流程：
1. 加载运行时环境（模块 01）
2. 调用 plannerX 进行 PRD 规划，生成 hybrid 文档
3. 等待用户确认 PRD
4. 调用 promptMasterX 优化执行指令（模块 04）
5. 调用 coderX 根据指令编码实现
6. 总线载荷校验（模块 02）+ 创建检查点（模块 03）
7. 调用 evaluatorX 定向审查
8. 如需修复，循环步骤 5-7（默认最多 2 轮，可通过 -N 参数覆盖）
9. 迭代完成后收口，如有 -box 参数则处理沙箱分支合并

支持的参数（从 $ARGUMENTS 中解析）：
- -N [数字]：限定评估最大迭代轮数
- -box [名称]：在沙箱分支中执行，隔离主线
- -parallel：PRD 确认后并行派发独立子任务
