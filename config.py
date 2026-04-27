"""
Multi-Agent Supervisor 项目配置
"""
import os
from dotenv import load_dotenv

load_dotenv()

# ── Groq 配置 ────────────────────────────────────────────
GROQ_API_KEY = os.getenv("GROQ_API_KEY", "")

# ── 模型降级列表（按优先级从高到低）─────────────────────
# call_with_fallback 会依次尝试，成功即返回，失败自动降级
MODEL_FALLBACK_LIST = [
    "openai/gpt-oss-120b",
    "openai/gpt-oss-20b",
    "qwen/qwen3-32b",
    "meta-llama/llama-4-scout-17b-16e-instruct",
    "llama-3.3-70b-versatile",
    "llama-3.1-8b-instant",
]

# ── LLM 通用参数 ─────────────────────────────────────────
LLM_TEMPERATURE = float(os.getenv("LLM_TEMPERATURE", "0.3"))
LLM_MAX_TOKENS = int(os.getenv("LLM_MAX_TOKENS", "4096"))

# ── Agent 名称映射（中文展示用）─────────────────────────
AGENT_NAMES = {
    "analyst": "需求分析 Agent",
    "architect": "架构设计 Agent",
    "coder": "编码 Agent",
    "reviewer": "代码审查 Agent",
}

# ── 执行顺序 ──────────────────────────────────────────────
AGENT_ORDER = ["analyst", "architect", "coder", "reviewer"]
