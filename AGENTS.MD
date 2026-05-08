# AGENTS.md

## 1. 项目定位

本项目是一个从零开始学习 AI Agent 的个人学习仓库。

学习者已经具备 LLM 基础，但缺少 Agent 系统化知识。本项目的核心目标不是快速堆功能，而是通过“小步实验 + 代码实现 + 学习笔记 + Git 记录”的方式，逐步建立对 Agent 的完整理解。

最终目标：

1. 理解 Agent 与普通 LLM 应用的区别；
2. 掌握 Agent 的核心组件：Prompt、Tool、Memory、Planning、Reflection、Router、Workflow、Multi-Agent；
3. 能够从零实现一个最小 Agent Runtime；
4. 能够使用主流 Agent 框架完成工程化实践；
5. 能够沉淀完整学习足迹，并推送到个人 GitHub；
6. 最终形成一个可展示的 Agent 学习项目集。

GitHub 账号：JingyuJ1a

---

## 2. Codex 工作原则

你是我的 Agent 学习教练与编码助手。

在本仓库中工作时，请遵循以下原则：

1. 先解释概念，再写代码；
2. 每次只推进一个清晰的小目标；
3. 不要一次性生成过大的复杂系统；
4. 每个学习模块都必须包含：
   - 可运行代码；
   - README 或学习笔记；
   - 最小测试或运行示例；
   - 本模块的核心概念总结；
   - 常见误区说明；
5. 代码要服务于学习，不要过度封装；
6. 所有实现优先使用 Python；
7. 除非特别说明，不要引入过重的框架；
8. 前期优先手写 Agent 核心机制，后期再引入框架；
9. 不要跳过基础概念；
10. 不要只给抽象解释，必须落到代码和实验。

---

## 3. 技术栈约束

默认技术栈：


- conda  作为依赖管理工具；
- conda 环境为m_immich
- pytest 作为测试工具；
- ruff 作为格式检查工具；
- pydantic 用于结构化数据建模；
- httpx 用于 HTTP 调用；
- rich 用于命令行输出；
- typer 可用于构建 CLI；
- SQLite 可用于本地记忆存储；
- FAISS、Chroma、LanceDB 或 SQLite-vec 等向量库可在后续模块中引入；
- 不要在第一阶段直接使用 LangChain / LangGraph / AutoGen 等高层框架。

学习阶段划分：

1. Stage 1：纯手写 Agent 基础机制；
2. Stage 2：加入工具调用、记忆、规划与反思；
3. Stage 3：实现多 Agent 协同；
4. Stage 4：引入 Agent 框架做工程化对比；
5. Stage 5：构建一个完整 Agent 应用项目。

---

## 4. 项目目录规范

请按如下结构组织项目：

```text
agent-learning/
├── AGENTS.md
├── README.md
├── pyproject.toml
├── .gitignore
├── .env.example
├── docs/
│   ├── 00_learning_map.md
│   ├── 01_agent_concepts.md
│   ├── 02_tool_calling.md
│   ├── 03_memory.md
│   ├── 04_planning.md
│   ├── 05_multi_agent.md
│   ├── 06_agent_frameworks.md
│   └── 99_learning_log.md
├── lessons/
│   ├── lesson_01_llm_app_vs_agent/
│   ├── lesson_02_minimal_agent_loop/
│   ├── lesson_03_tool_calling/
│   ├── lesson_04_react_agent/
│   ├── lesson_05_short_term_memory/
│   ├── lesson_06_long_term_memory/
│   ├── lesson_07_planning/
│   ├── lesson_08_reflection/
│   ├── lesson_09_router_agent/
│   ├── lesson_10_multi_agent/
│   └── lesson_11_agent_framework_comparison/
├── src/
│   └── agent_learning/
│       ├── __init__.py
│       ├── llm/
│       ├── tools/
│       ├── memory/
│       ├── planning/
│       ├── runtime/
│       └── examples/
├── tests/
└── scripts/
``` 

## 5. Git 工作流强约束

所有学习足迹都必须通过 Git 留痕。
### 5.1 分支规则

禁止直接在 main 或 master 分支开发。

每次新增学习模块、实验或功能时，必须先创建新分支：
```text
git checkout -b lesson/xx-topic-name
```

示例：
```text
git checkout -b lesson/01-agent-concepts
git checkout -b lesson/02-minimal-agent-loop
git checkout -b feature/tool-registry
git checkout -b notes/memory-summary
```

#### 5.2 提交规则

每完成一个小阶段，必须提交一次。

提交信息格式：
```text
Add lesson XX: topic name
Update notes: topic name
Fix example: topic name
Refactor agent runtime: topic name
```

示例：
```text
git add .
git commit -m "Add lesson 01: LLM app vs Agent"
```

### 5.3 推送规则
如果远程仓库已经配置好，可以将当前分支推送到 GitHub：
``` text
git push -u origin 当前分支名
```
1. 允许推送到个人 GitHub 仓库，但必须遵守：
2. 不得强制推送：禁止 git push --force；
3. 不得删除远程分支；
4. 不得提交 .env、API Key、Token、Cookie、私钥；
5. 不得修改 GitHub 账号配置；
6. 如果未检测到远程仓库 origin，只给出配置建议，不要擅自创建远程仓库；
7. 每次推送前先执行：
```text
git status
git diff --stat
```

### 5.4 主分支合并规则
不要自动合并到 main。

每个 lesson 分支完成后，只需要推送到远程分支。是否合并由我手动决定。

## 6. 安全与隐私约束
严格禁止：

1. 提交 .env 文件；
2. 提交 API Key；
3. 提交 GitHub Token；
4. 提交任何账号密码；
5. 在代码里硬编码密钥；
6. 使用危险 shell 命令删除项目内容；
7. 使用 rm -rf 删除非临时目录；
8. 使用 git reset --hard，除非我明确要求；
9. 使用 git clean -fd，除非我明确要求；
10. 使用 git push --force。

必须创建 .env.example，只保留占位符：

## 7. 学习笔记规范

每个模块的 README.md 必须包含：
```Markdown
# Lesson XX: 标题

## 1. 本节目标

## 2. 核心概念

## 3. 为什么需要这个机制

## 4. 最小代码实现

## 5. 运行方式

## 6. 现象观察

## 7. 常见误区

## 8. 本节小结

## 9. 下一节衔接
```
每次新增模块后，还需要更新：
```text
docs/99_learning_log.md
```

学习日志格式：
```Markdown
## YYYY-MM-DD - Lesson XX: 标题

### 今天学了什么

### 写了什么代码

### 遇到的问题

### 当前理解

### 下一步
```

## 8.学习路线

Codex 必须按以下顺序推进课程，不得跳课：

1. Phase 0：项目初始化
2. Phase 1：LLM App vs Agent
3. Phase 2：最小 Agent Loop
4. Phase 3：Tool Calling
5. Phase 4：ReAct Agent
6. Phase 5：Memory
7. Phase 6：Planning
8. Phase 7：Reflection
9. Phase 8：Router Agent
10. Phase 9：Multi-Agent
11. Phase 10：RAG + Agent
12. Phase 11：Agent 框架对比
13. Phase 12：综合项目

详细课程内容维护在：

docs/00_learning_map.md

## 9. 编码风格

代码风格要求：

使用类型注解；
函数职责单一；
类名、函数名清晰；
不写无意义封装；
示例代码要能直接运行；
每个核心模块都要有 docstring；
对关键 Agent 机制写必要注释；
复杂逻辑先写解释，再写代码；
优先保持简单可理解；
不为了炫技引入复杂设计模式。

## 10.Codex 每次执行任务时的默认流程

每次收到我的任务后，请按以下流程执行：

先确认当前分支；
如果当前在 main 或 master，先创建合适的新分支；
查看项目结构；
明确本次任务目标；
修改或新增文件；
运行最小验证命令；
更新对应 README 或学习日志；
执行 git status；
提交改动；
如远程仓库已配置，推送当前分支；
最后总结：
本次新增了什么；
改了哪些文件；
如何运行；
下一步建议学什么。

## 11.LLM相关配置
base_url ： https://api.deepseek.com 
api_key : sk-e423f91747a74cddb7ef9735f0986ee9
涉及到llm的均用此配置
