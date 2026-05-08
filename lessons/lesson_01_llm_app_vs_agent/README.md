# Lesson 01: LLM App vs Agent

## 1. 本节目标

本节只解决一个问题：普通 LLM App 和 Agent 到底差在哪里。

完成本节后，你应该能说清楚：

- LLM App 是一次性“输入 prompt，输出 answer”的调用；
- Agent 是一个带控制流的系统，会决定是否行动、调用工具、观察结果，再继续生成答案；
- Agent 的核心不是“更聪明的 prompt”，而是“模型 + 动作 + 环境反馈 + 循环”。

## 2. 核心概念

普通 LLM App：

```text
User Question -> Prompt -> LLM -> Answer
```

最小 Agent：

```text
User Question -> LLM decides action -> Tool/Environment -> Observation -> LLM final answer
```

二者最大的区别：

- LLM App 只生成文本；
- Agent 可以把文本决策转成动作；
- Agent 会把动作结果重新放回上下文；
- Agent 通常有循环、状态、工具和退出条件。

## 3. 为什么需要这个机制

普通 LLM App 适合回答模型已经知道、或者只需要语言处理的问题。

但很多真实任务需要外部动作，比如：

- 查天气；
- 读文件；
- 调用数据库；
- 执行代码；
- 拆解多步骤任务；
- 根据中间结果调整下一步。

这时只靠一次 LLM 调用不够。Agent 的价值在于让模型不只是“说”，还可以“决定下一步做什么”。

## 4. 最小代码实现

本节代码在：

```text
lessons/lesson_01_llm_app_vs_agent/llm_app_vs_agent.py
```

代码包含三个部分：

- `simple_llm_app`：普通 LLM App，一次调用直接回答；
- `minimal_agent`：最小 Agent Loop，先决定动作，再调用工具，最后回答；
- `LLMConfig`：大模型配置，默认使用本仓库 `AGENTS.MD` 中约定的 DeepSeek 兼容接口；
- `OpenAICompatibleLLM`：最小真实 LLM 客户端，通过 OpenAI-compatible Chat Completions API 调用模型。

## 5. 运行方式

在项目根目录运行：

```bash
export DEEPSEEK_API_KEY="你的 API Key"
python3 lessons/lesson_01_llm_app_vs_agent/llm_app_vs_agent.py
```

默认配置：

```text
DEEPSEEK_BASE_URL=https://api.deepseek.com
DEEPSEEK_MODEL=deepseek-chat
```

如果要临时覆盖，可以设置：

```bash
export DEEPSEEK_BASE_URL="https://你的服务地址"
export DEEPSEEK_MODEL="你的模型名"
```

运行测试：

```bash
python3 -m pytest tests/test_lesson_01.py
```

## 6. 现象观察

普通 LLM App 的输出类似：

```text
I can answer from the prompt, but I cannot check the outside world.
```

最小 Agent 的输出会多出执行轨迹：

```text
Thought: The question needs information outside the prompt.
Action: USE_TOOL:get_weather:Shanghai
Observation: Shanghai: sunny
Answer: Shanghai is sunny today, based on the tool observation.
```

你要重点观察的是：Agent 的答案不是直接从第一次 prompt 来的，而是先产生动作，再把动作结果作为观察输入最终回答。

## 7. 常见误区

误区一：Agent 等于一个很长很复杂的 Prompt。

不是。Prompt 很重要，但 Agent 的关键是控制流。没有动作、观察和循环，通常只是一个 LLM App。

误区二：只要调用工具就是 Agent。

不一定。如果工具调用是程序员硬编码的，而模型没有参与决策，那更像普通工作流。Agent 的特点是模型参与“下一步做什么”的选择。

误区三：Agent 一定要很复杂。

不需要。第一课里的 Agent 只有一步动作，但已经具备 Agent 的基本形状：决定、行动、观察、回答。

## 8. 本节小结

普通 LLM App 的核心是：

```text
Prompt -> Completion
```

Agent 的核心是：

```text
State -> Decide -> Act -> Observe -> Update State -> Answer or Continue
```

本节先用最小代码建立直觉。后续课程会逐步加入工具注册、ReAct、多轮记忆、规划、反思和多 Agent 协作。

## 9. 下一节衔接

下一节会进入最小 Agent Loop：不只做一次工具调用，而是加入循环和退出条件，让 Agent 能够多步执行任务。
