# 🤖 Multi-Agent Demo

> 基于 **LangGraph + Groq** 的多 Agent 编排演示平台，支持多种编排模式，Streamlit 亮色 UI 实时展示执行过程。

## 功能特性

- **Supervisor Pipeline**（顺序流转）：Supervisor 统一调度，四个子 Agent 顺序流转，每个 Agent 的输出作为下一个的输入上下文
- **Conditional Branch**（动态路由）：根据输入类型（新功能/代码审查/技术方案），动态激活对应的一组 Agent
- **Loop Feedback**（迭代优化）：编码 Agent 生成代码后，质检 Agent 进行评审，不合格则打回重做（最多重试3次）
- **模型自动降级**：依次尝试 6 个模型，成功即返回并在 UI 中标注实际使用的模型名
- **多模式切换**：侧边栏一键切换编排模式，其余模式持续迭代中
- **实时状态展示**：执行中动态更新 Agent 状态徽章，折叠面板展示各 Agent 输出

## 架构

```
用户需求 → Supervisor (LangGraph StateGraph)
              │
              ├─ ① 需求分析 Agent   →  用户故事、功能列表、边界条件
              ├─ ② 架构设计 Agent   →  技术选型、模块划分、数据流
              ├─ ③ 编码 Agent       →  代码框架、类定义、函数签名
              └─ ④ 代码审查 Agent   →  风险评估、改进建议、评分
```

## 技术栈

| 组件 | 技术 |
|------|------|
| Agent 编排 | LangGraph (StateGraph) |
| 推理模型 | Groq（自动降级，支持 6 个模型） |
| 界面 | Streamlit（亮色主题） |
| Prompt 管理 | 模块化 Python 模板 |

## 模型降级列表

按优先级从高到低依次尝试，失败自动切换到下一个：

```
openai/gpt-oss-120b
→ openai/gpt-oss-20b
→ qwen/qwen3-32b
→ meta-llama/llama-4-scout-17b-16e-instruct
→ llama-3.3-70b-versatile
→ llama-3.1-8b-instant
```

每个 Agent 的输出面板旁会显示实际命中的模型名。

## 项目结构

```
multi-agent/
├── app.py                    # 统一 Streamlit 入口（模式切换 + UI）
├── config.py                 # 共享配置（模型列表、Agent 元信息）
├── llm.py                    # call_with_fallback()：模型降级调用层
├── supervisor_pipeline/      # ✅ Supervisor 顺序流转模式
│   ├── __init__.py
│   ├── graph.py              # LangGraph StateGraph 图定义
│   ├── agents/
│   │   ├── analyst.py        # 需求分析 Agent
│   │   ├── architect.py      # 架构设计 Agent
│   │   ├── coder.py          # 编码 Agent
│   │   └── reviewer.py       # 代码审查 Agent
│   └── prompts/
│       ├── analyst_prompt.py
│       ├── architect_prompt.py
│       ├── coder_prompt.py
│       └── reviewer_prompt.py
├── conditional_branch/       # ✅ 条件动态路由模式
│   ├── __init__.py
│   ├── graph.py              # 路由分支图定义
│   ├── agents/               # router, cb_analyst, cb_coder 等
│   └── prompts/              # all_prompts.py
├── loop_feedback/            # ✅ 循环反馈收敛模式
│   ├── __init__.py
│   ├── graph.py              # 含条件反馈循环的图定义
│   ├── agents/               # coder, reviewer
│   └── prompts.py
├── parallel/                 # 🚧 敬请期待
├── debate/                   # 🚧 敬请期待
├── nested_agent/             # 🚧 敬请期待
├── requirements.txt
├── .env.example
└── .env                      # 本地密钥（不提交）
```

## 快速开始

### 1. 创建并激活虚拟环境（推荐）

```bash
# Windows (PowerShell)
python -m venv .venv
.\.venv\Scripts\Activate.ps1

# macOS / Linux
python -m venv .venv
source .venv/bin/activate
```

### 2. 安装依赖

```bash
pip install -r requirements.txt
```

### 2. 配置环境变量

```bash
cp .env.example .env
# 编辑 .env，填入你的 GROQ_API_KEY
```

`.env` 示例：

```
GROQ_API_KEY=your_groq_api_key_here
LLM_TEMPERATURE=0.3
LLM_MAX_TOKENS=4096
```

### 3. 启动应用

```bash
streamlit run app.py
```

浏览器访问 `http://localhost:8501`

## 使用方式

1. 侧边栏选择编排模式（目前 **Supervisor Pipeline**, **Conditional Branch**, **Loop Feedback** 可用）
2. 在主区域输入框中描述软件需求
3. 点击「🚀 开始执行」
4. 四个折叠面板依次展示每个 Agent 的执行结果，顶部显示实际命中的模型名

## 编排模式路线图

| 模式 | 说明 | 状态 |
|------|------|------|
| Supervisor Pipeline | 四个 Agent 顺序流转 | ✅ 已上线 |
| Conditional Branch | 条件动态路由 | ✅ 已上线 |
| Loop Feedback | 迭代反馈收敛 | ✅ 已上线 |
| Parallel | 多 Agent 并行汇总 | 🚧 开发中 |
| Debate | 多 Agent 对抗辩论 | 🚧 开发中 |
| Nested Agent | 嵌套子 Agent 调用 | 🚧 开发中 |

## License

MIT
