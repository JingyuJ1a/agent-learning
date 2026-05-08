# Learning Log

## 2026-05-08 - Lesson 01: LLM App vs Agent

### 今天学了什么

普通 LLM App 是一次 prompt 到一次 answer；Agent 会先决策动作，再读取动作返回的 observation，最后生成答案。

### 写了什么代码

- 新增普通 LLM App 与最小 Agent 的对比实验。
- 定义 `LLM` 协议，让应用只依赖 `complete(prompt)` 这个最小接口。
- 定义 `LLMConfig`，默认使用 DeepSeek OpenAI-compatible API 配置。
- 定义 `OpenAICompatibleLLM`，运行时通过 `httpx` 调用真实大模型。

### 遇到的问题

当前本地 Python 环境没有安装 `httpx` 和 `pydantic`，所以测试不直接访问真实网络服务，只验证 Agent 控制流和配置默认值。

### 当前理解

真实 LLM 客户端属于 Agent 的模型层；Agent 本身不应该关心具体供应商，只需要一个稳定的 `LLM` 接口。

### 下一步

进入最小 Agent Loop，增加循环次数、停止条件和更清晰的执行状态。
