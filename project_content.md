# Python MCP 学习项目规划

## 一、项目背景

我正在从 C#/.NET 开发逐步转向 Python 和 AI 工程方向。

这次不准备直接研究或复刻代码量较大的官方 FalkorDB MCP Server。官方项目文件较多，包含大量当前阶段暂时不需要理解的内容，不适合作为第一个 MCP 开发项目。

本项目的目标是从简单、完整、可实际运行的案例开始，同时学习 MCP Server 和 MCP Client 两个方向。

学习方式如下：

1. 本项目采用 ChatGPT 负责教学规划、Codex 负责本地实现与验证的协作方式。
2. 用户会阅读 Codex 生成的代码。
3. 用户会自己重新手写一遍核心代码。
4. 每个阶段都必须能够运行和验证。
5. 不要一次性生成过多代码，应按阶段逐步实现。
6. 优先保证用户能够理解，而不是追求功能数量。

---

# 二、整体项目方向

本次 MCP 学习分为两个子项目。

## Project 1：Weather MCP Server

目标：

使用 Python 开发一个本地 Weather MCP Server，将普通天气 HTTP API 包装成 MCP Tool，并接入本地 Codex。

该项目用于学习 MCP 的 Server 侧。

整体结构：

```text
Codex
  ↓ MCP Client
Weather MCP Server
  ↓ HTTP API
第三方天气服务
```

Codex 本身已经具备 MCP Client 能力，因此本项目不需要为 Codex 另外实现 MCP Client。

Weather MCP Server 负责：

* 注册 MCP Tools
* 接收城市名等输入参数
* 调用第三方天气 API
* 解析天气 API 返回结果
* 将结果转换为结构化数据并返回
* 处理超时、城市不存在、接口异常等情况

---

## Project 2：Remote MCP Client CLI & Agent Adapter

目标：

基于官方 MCP Python SDK，开发一个可以连接远程 MCP Server 的通用客户端应用，并使用 Notion 官方 MCP Server 作为真实验证对象。

该项目用于学习 MCP 的 Client 侧，但不从零实现 MCP 协议、JSON-RPC、Transport 或完整 Client SDK。

整体结构：

```text
Python CLI / 自己的 Agent / OpenClaw / Hermes
                ↓
 Remote MCP Client CLI & Agent Adapter
                ↓
        官方 MCP Python SDK
                ↓
        Notion 官方 MCP Server
                ↓
          Notion Workspace
```

本项目不重新开发 Notion MCP Server，也不重新封装 Notion REST API。

官方 MCP Python SDK 负责底层协议处理、消息结构、Transport、Session 和生命周期管理。本项目重点开发 SDK 上层的客户端应用与适配层，包括：

* MCP Server 配置管理
* Streamable HTTP 远程连接
* OAuth 或 Token 认证
* Client 初始化与 Session 生命周期管理
* Server capability 获取
* Tools、Resources 和 Prompts 发现
* Tool Schema 展示与参数校验
* Tool 调用与结果解析
* 超时、重试和异常处理
* 日志与 CLI 输出格式化
* Python Agent Adapter
* 多个 MCP Server 的配置支持

项目定位：

> 基于官方 MCP Python SDK 开发可复用的 Remote MCP Client CLI 与 Agent Adapter，并使用 Notion 官方 MCP Server 完成真实的连接、认证、工具发现和工具调用。

---

# 三、Project 1：Weather MCP Server

## 1. 技术目标

建议使用：

* Python 3.11 或更高版本
* uv
* MCP Python SDK
* FastMCP
* httpx
* Pydantic
* pydantic-settings
* pytest
* pytest-asyncio
* respx 或 httpx MockTransport
* ruff
* mypy

初期使用 stdio transport，方便本地 Codex 启动。

不要从底层手写 JSON-RPC 或 MCP 协议。

---

## 2. 第一版功能范围

第一版只实现一个 Tool：

```python
get_current_weather(city: str)
```

返回内容建议包括：

* city
* country
* temperature
* apparent_temperature
* humidity
* weather_description
* wind_speed
* observed_at

输入输出必须使用明确的 Python 类型。

---

## 3. 推荐项目结构

```text
python-mcp-study/
├── README.md
├── pyproject.toml
├── .gitignore
├── .env.example
├── src/
│   └── weather_mcp/
│       ├── __init__.py
│       ├── server.py
│       ├── weather_client.py
│       ├── models.py
│       ├── config.py
│       └── exceptions.py
└── tests/
    ├── test_weather_client.py
    └── test_weather_tool.py
```

职责划分：

### server.py

负责：

* 创建 FastMCP Server
* 注册 MCP Tool
* 接收和校验参数
* 调用 WeatherClient
* 将异常转换为适合 MCP 返回的信息

### weather_client.py

负责：

* 使用 httpx 调用天气 API
* 请求超时设置
* HTTP 错误处理
* JSON 解析
* 将第三方 API 数据转换为内部模型

这里的 WeatherClient 是普通 HTTP Client，不是 MCP Client。

### models.py

负责定义：

* WeatherResult
* API 响应模型
* 必要的枚举或值对象

### config.py

负责：

* API URL
* API Key
* Timeout
* 环境变量读取

### exceptions.py

负责定义：

* WeatherApiError
* CityNotFoundError
* InvalidWeatherResponseError
* WeatherTimeoutError

---

## 4. 第一阶段测试范围

至少覆盖：

* 正常返回天气数据
* 城市不存在
* 请求超时
* HTTP 4xx
* HTTP 5xx
* 返回 JSON 缺少必要字段
* 城市名为空
* 第三方 API 返回格式异常

测试时不能真实请求外部天气 API，应使用 Mock。

---

## 5. 第二阶段扩展

第一版完成后再增加：

```text
get_weather_forecast(city, days)
```

可选扩展：

* 当前天气
* 多日预报
* 城市搜索
* 摄氏度和华氏度选择
* 日语、中文和英文天气描述
* 日志记录
* 重试机制
* API 限流处理

不要在第一阶段加入全部功能。

---

## 6. Codex 接入验证

最终需要：

1. 启动 Weather MCP Server。
2. 在 Codex MCP 配置中注册该 Server。
3. 确认 Codex 可以发现 Tool。
4. 让 Codex 调用：

```text
查询东京当前天气
```

5. 验证 MCP Server 收到调用。
6. 验证 Weather API 被正确调用。
7. 验证结果返回给 Codex。

---

# 四、Project 2：Remote MCP Client CLI & Agent Adapter

## 1. 项目定位

该项目基于官方 MCP Python SDK 开发，不自行实现底层 MCP Client 协议栈。

主要学习：

* 官方 MCP Python SDK 的 Client 用法
* 远程 MCP Server 连接
* MCP Client 初始化与 Session 生命周期
* Server capabilities
* tools/list 与 tools/call
* resources/list 与 prompts/list
* OAuth 认证
* Token 保存和刷新
* CLI 应用设计
* Agent Tool Adapter
* 多 Server 配置管理

Notion 只作为一个实际存在的远程 MCP Server 用于验证。

不要开发自己的 Notion MCP Server，不要重新封装 Notion REST API，也不要重新实现官方 SDK 已经提供的 HTTP、JSON-RPC、Transport 和 Session 功能。

---

## 2. 技术原则

建议使用：

* Python 3.11 或更高版本
* uv
* 官方 MCP Python SDK
* Typer 或 argparse
* Pydantic
* pydantic-settings
* httpx
* pytest
* pytest-asyncio
* ruff
* mypy

版本原则：

* 开始开发时固定 MCP SDK 版本，避免学习过程中被破坏性更新影响。
* 优先使用当时的稳定版本。
* SDK 升级与迁移单独作为后续任务，不与第一版开发混在一起。

---

## 3. 推荐结构

```text
src/
└── remote_mcp_client/
    ├── __init__.py
    ├── client.py
    ├── config.py
    ├── registry.py
    ├── auth.py
    ├── token_store.py
    ├── models.py
    ├── exceptions.py
    ├── cli.py
    └── adapters/
        ├── __init__.py
        ├── base.py
        └── cli.py
```

职责说明：

### client.py

* 封装官方 SDK Client
* 管理连接和关闭
* 获取 capabilities
* 发现 Tools、Resources 和 Prompts
* 调用 Tool
* 将 SDK 返回值转换为应用内部模型

### config.py

* 定义单个 MCP Server 配置
* 读取 URL、认证方式、超时和 Server 名称
* 不写死 Notion 配置

### registry.py

* 保存和读取多个 MCP Server 配置
* 根据 Server 名称创建对应 Client

### auth.py / token_store.py

* 处理 OAuth 或 Token 获取
* 判断 Token 是否过期
* 刷新 Token
* 安全保存 Token

### adapters/

* 将 MCP Tool 定义转换为上层 Agent 或 CLI 能使用的格式
* 第一版只实现基础接口和 CLI Adapter

不需要自行编写 `transport.py` 或 `session.py` 去重复官方 SDK 的底层实现。只有当未来确实需要扩展 SDK 行为时，才增加相应封装。

---

## 4. 第一版功能范围

第一版先实现不包含完整 Agent 集成的 CLI，并优先使用无需复杂 OAuth 的测试 MCP Server 完成基础流程。

建议命令：

```bash
mcp-client server list
mcp-client server add <name> <url>
mcp-client connect <server>
mcp-client tools <server>
mcp-client tool describe <server> <tool-name>
mcp-client tool call <server> <tool-name> --json '{...}'
mcp-client resources <server>
mcp-client prompts <server>
```

核心接口示例：

```python
class RemoteMcpClient:
    async def connect(self) -> None:
        ...

    async def list_tools(self) -> list[ToolDefinition]:
        ...

    async def call_tool(
        self,
        name: str,
        arguments: dict[str, object],
    ) -> ToolResult:
        ...

    async def close(self) -> None:
        ...
```

客户端不应写死 Notion 的 Tool 名称和参数，应通过 MCP 的工具发现机制动态读取 Tool Schema。

第一版验收标准：

* 可以从配置读取一个远程 MCP Server
* 可以通过官方 SDK 建立连接
* 可以完成 initialize
* 可以列出 Tools
* 可以展示 Tool Schema
* 可以调用一个 Tool
* 可以格式化输出结果
* 可以正常关闭 Session
* 连接错误和调用错误有明确提示

---

## 5. OAuth 和 Token 管理

基础连接流程完成后，再接入 Notion 官方 MCP Server 并处理 OAuth。

需要理解和实现：

* Authorization Code Flow
* PKCE
* 浏览器授权
* Redirect URI
* Access Token
* Refresh Token
* Token 过期判断
* Token 刷新
* Token 本地安全保存

优先使用官方 SDK 已提供的认证能力。只有 SDK 未覆盖的应用层逻辑才自行开发。

Token 不允许：

* 写入 Git
* 硬编码在源码中
* 输出到普通日志
* 直接发送给模型

第一版可先实现本地 JSON Token Store，但必须：

* 文件权限受限
* `.gitignore` 排除
* 不记录完整 Token

后续可考虑系统 Keyring。

---

## 6. MCP Client 学习流程

客户端至少需要理解和验证以下流程：

```text
读取 Server 配置
  ↓
官方 SDK 建立连接
  ↓
initialize
  ↓
获取 Server capabilities
  ↓
tools/list
  ↓
读取 Tool Schema
  ↓
tools/call
  ↓
解析 Tool Result
  ↓
关闭 Session
```

学习重点不是重写底层协议，而是理解官方 SDK 如何完成这些流程，以及如何在其上构建稳定的应用程序。

项目重点：

* SDK Client 使用
* Session 生命周期管理
* 认证管理
* Tool 动态发现
* 参数校验
* Tool 调用
* 返回结果转换
* 错误处理
* 配置管理
* Agent 接口转换

---

## 7. Agent Adapter

CLI 完成后，增加统一适配接口：

```python
class AgentToolProvider:
    async def list_tools(self) -> list[ToolDefinition]:
        ...

    async def call_tool(
        self,
        name: str,
        arguments: dict[str, object],
    ) -> ToolResult:
        ...
```

这样可以将远程 MCP Tools 转换为不同 Agent 可以使用的格式。

未来可扩展：

```text
Notion MCP Server / 其他远程 MCP Server
                    ↓
          官方 MCP Python SDK
                    ↓
       Remote MCP Client Application
                    ↓
CLI Adapter
OpenClaw Adapter
Hermes Adapter
自定义 Python Agent Adapter
```

Adapter 第一阶段只定义接口和一个 CLI Adapter，不需要立刻完成 OpenClaw 和 Hermes 的完整接入。

---

# 五、为什么要同时学习 Server 和 Client

未来企业系统可能出现两种典型情况。

## 情况一：系统只有普通 API

例如：

* 天气 API
* kintone API
* Backlog API
* 工时系统 API
* Oracle Database
* 文件服务器
* 企业内部 REST API

此时需要开发：

```text
普通 API
  ↓
自研 MCP Server
  ↓
Agent 自带的 MCP Client
```

Weather MCP Server 就是这一类的最小实践。

---

## 情况二：系统已经提供 MCP Server

例如 Notion 已经提供官方 MCP Server，但本地程序或 Agent 没有合适的 MCP 支持，或者现有支持无法满足配置、认证、日志和业务适配要求。

此时需要开发：

```text
Agent / Python 程序
        ↓
自研 Client Application 或 Adapter
        ↓
官方 MCP Python SDK
        ↓
现有 MCP Server
```

Project 2 就是这一类的实践。

---

## 日本企业场景

日本很多企业网站和内部业务系统目前可能只有：

* REST API
* SOAP API
* OAuth
* API Key
* CSV
* Excel
* Oracle Database
* 文件服务器
* 社内批处理
* 既有 Web 系统

未来 AI 系统落地时，真正需要的工作可能是：

* 将旧系统封装为 MCP Server
* 使用官方 SDK 将业务程序接入现有 MCP Server
* 完成权限控制和认证
* 处理既有系统的数据结构
* 实现 Agent 与业务系统之间的适配层

因此，这两个项目和未来企业系统集成工作有较高关联性。

---

# 六、开发顺序

不要同时开发两个项目。

按以下顺序推进：

## Phase 1：Weather MCP 最小版本

完成：

* 项目初始化
* FastMCP Server
* 一个 Weather Tool
* Mock 测试
* 本地运行
* Codex 接入

## Phase 2：Weather MCP 工程化

完成：

* 配置管理
* Pydantic 模型
* 异常体系
* 日志
* 超时
* 重试
* 测试覆盖
* README

## Phase 3：官方 SDK Client 基础学习

完成：

* 固定 MCP Python SDK 版本
* 阅读官方 Client 示例
* 连接一个简单远程 MCP Server
* initialize
* capabilities
* tools/list
* tools/call
* Session 生命周期验证

## Phase 4：Remote MCP Client CLI

完成：

* Server 配置管理
* 多 Server Registry
* Tools、Resources 和 Prompts 展示
* Tool Schema 展示
* Tool 调用
* 结果格式化
* 错误处理
* CLI 测试

## Phase 5：Notion OAuth 验证

完成：

* OAuth + PKCE
* Token 保存
* Token 刷新
* Notion 官方 MCP 连接验证
* 至少一次真实 Tool 发现和调用

## Phase 6：Agent Adapter

完成：

* 通用 AgentToolProvider 接口
* CLI Adapter
* 可选 OpenClaw Adapter
* 可选 Hermes Adapter

---

# 七、对 Codex 的开发要求

请遵守以下原则：

1. 不要一次性生成整个项目。
2. 每次只完成一个阶段。
3. 每个阶段先说明：
   * 本阶段目标
   * 要新增或修改的文件
   * 每个文件的职责
   * 如何运行
   * 如何验证
4. 代码应符合 Python 工程规范。
5. 代码应包含完整类型注解。
6. 不要过度设计。
7. 不要引入当前阶段不需要的抽象层。
8. 先实现最小可运行版本，再逐步重构。
9. 所有外部 API 调用必须有 Timeout。
10. 所有 Token 和 API Key 必须通过环境变量或安全存储读取。
11. 测试不能依赖真实外部 API。
12. 每完成一个阶段，给出用户应该手写和重点理解的代码清单。
13. 不要直接替用户完成所有学习过程。
14. 当有多种实现方式时，优先选择最容易理解且符合官方 SDK 用法的方案。
15. 修改代码后运行测试、ruff 和必要的类型检查。
16. Project 2 不得从零实现 MCP 协议栈，不得重复开发官方 SDK 已提供的 Transport、Session 和 JSON-RPC 功能。
17. Project 2 应先完成官方 SDK 的最小 Client 示例，再逐步增加 CLI、配置管理和 Adapter。

---

# 八、当前第一项任务

当前只推进 Project 1：Weather MCP Server。

请先完成以下内容：

1. 初始化 Python 项目。
2. 使用 `src` layout。
3. 配置 `pyproject.toml`。
4. 创建最小目录结构。
5. 选择一个适合教学的免费天气 API。
6. 第一阶段只实现：

```python
get_current_weather(city: str)
```

7. 添加最小 Mock 单元测试。
8. 提供本地启动命令。
9. 提供 Codex MCP 配置示例。
10. 列出用户需要亲自手写一遍的文件和代码。

开始前先输出项目结构和第一阶段实施计划，不要直接一次性生成全部文件。
