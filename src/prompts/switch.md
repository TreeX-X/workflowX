---
name: switch
description: "切换工作流模式（whole / local / unit），自动保存当前检查点"
---
请切换当前工作流模式。

目标模式：$ARGUMENTS

支持的值：whole / local / unit

切换规则：
- 如果当前有进行中的任务，先保存当前检查点
- 切换到目标模式后，通知用户新模式已生效
- 后续输入按新模式的流程执行
