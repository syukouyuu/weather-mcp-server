# weather mcp server Project Agent Rules

- ChatGPT 负责学习路线、阶段划分、MCP 概念解释和验收标准。
- Codex 负责读取仓库、执行命令、创建或修改代码、运行测试并汇报结果。
- 用户负责手写和复核核心代码，并决定是否进入下一阶段。
- Codex 不应自行扩大当前阶段范围，不主动加入未要求的抽象层、依赖或功能。
- 如 Codex 的建议与当前 ChatGPT 制定的阶段计划冲突，以当前阶段计划为准，并先向用户说明。

## Project Context

- 远程仓库：<https://github.com/syukouyuu/weather-mcp-server.git>
- MCP 官方参考文档：<https://modelcontextprotocol.io/docs/getting-started/intro>
- 本项目是 Python MCP 学习项目，当前子项目为 Weather MCP Server。

## Command Boundaries

- 用户贴回命令输出后，再帮助解释是否正常、下一步该做什么。
- 可以主动运行低风险的本地调查命令，例如 `git status`、`git diff`、`git log`、`ls`、`find`、`sed`、`rg`，但不要因此触发训练、下载或 GPU 调用。

## Git And Documentation

- 提交前先检查 `git status --short` 和暂存 diff，确认只包含本次目标相关文件。
- 不要提交 `.venv/`、`__pycache__/`、训练输出、checkpoint、下载数据或本地缓存。
- `runs/` 里的脚本可以被 Git 追踪；训练产物和缓存不要放进提交。
- 更新学习记录时，优先放入 `doc/phase*/` 或 `doc/templates/`，保持内容便于后续复习。

## Safety Rules

- 破坏性操作、外部发送、公开发布、高风险配置改动前必须确认。
- 证据不足时直接说明，不把猜测当事实。
- 不跨越角色边界：实现、重构、调试、测试可协助；最终学习路线以用户和 ChatGPT 当前安排为准。
- 结果优先汇报，不主动扩展到额外高风险动作。
