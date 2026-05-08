Phase 0：项目初始化

目标：

初始化 Python 项目；
初始化 Git；
创建 README；
创建 AGENTS.md；
创建基础目录结构；
配置 .gitignore；
配置 .env.example；
配置 pytest；
配置 ruff；
完成第一次提交。
Phase 1：Agent 基础认知

目标：

解释 LLM App 与 Agent 的区别；
解释 Agent 的最小组成；
编写一个普通 LLM 调用示例；
编写一个最小 Agent Loop；
对比两者差异。
Phase 2：Tool Calling

目标：

理解工具调用的本质；
手写 Tool schema；
实现 Calculator Tool；
实现 File Reader Tool；
实现 Tool Registry；
实现 Tool Dispatcher；
让 Agent 根据任务选择工具。
Phase 3：ReAct Agent

目标：

理解 Thought / Action / Observation 模式；
手写 ReAct Prompt；
实现 ReAct Loop；
增加最大步数限制；
增加工具调用错误处理；
记录完整执行轨迹。
Phase 4：Memory

目标：

区分短期记忆与长期记忆；
实现 Conversation Memory；
实现 Summary Memory；
实现 SQLite Memory；
实现 Embedding-based Retrieval Memory；
讨论记忆污染、记忆更新、记忆遗忘机制。
Phase 5：Planning

目标：

理解任务分解；
实现 Plan-and-Execute Agent；
实现任务状态机；
实现计划修正机制；
对比 ReAct 与 Planning Agent。
Phase 6：Reflection

目标：

理解自我反思机制；
实现执行后反思；
实现失败重试；
实现结果评分；
讨论 Reflection 的边界和成本。
Phase 7：Router Agent

目标：

实现意图识别；
实现任务路由；
构建多个专家 Agent；
实现 Router -> Specialist 的调用链。
Phase 8：Multi-Agent

目标：

理解多 Agent 协作模式；
实现 Planner Agent；
实现 Executor Agent；
实现 Reviewer Agent；
实现 Debate / Critic / Supervisor 模式；
讨论多 Agent 的收益与复杂度。
Phase 9：RAG + Agent

目标：

区分 RAG 与 Agent；
实现文档加载；
实现向量检索；
实现 Agent 使用检索工具回答问题；
实现引用来源返回；
讨论幻觉控制。
Phase 10：Agent 框架对比

目标：

对比手写 Agent Runtime 与主流框架；
尝试 OpenAI Agents SDK；
尝试 LangGraph；
尝试 MCP；
总结框架适用边界。
Phase 11：综合项目

目标：

构建一个完整的个人学习助手 Agent，具备：

工具调用；
任务规划；
短期记忆；
长期记忆；
文档检索；
执行轨迹记录；
结果反思；
CLI 交互；
测试用例；
完整 README。