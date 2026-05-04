"""
Multi-Agent Supervisor プロジェクト設定
"""
import os
from dotenv import load_dotenv

load_dotenv()

# Groq設定
GROQ_API_KEY = os.getenv("GROQ_API_KEY", "")

# モデルフォールバックリスト（優先度順）
# call_with_fallbackが順次試行し、成功したら返却、失敗したら次のモデルへ
MODEL_FALLBACK_LIST = [
    "openai/gpt-oss-120b",
    "openai/gpt-oss-20b",
    "qwen/qwen3-32b",
    "meta-llama/llama-4-scout-17b-16e-instruct",
    "llama-3.3-70b-versatile",
    "llama-3.1-8b-instant",
]

# LLM共通パラメータ
LLM_TEMPERATURE = float(os.getenv("LLM_TEMPERATURE", "0.3"))
LLM_MAX_TOKENS = int(os.getenv("LLM_MAX_TOKENS", "4096"))

# エージェント名マッピング（表示用）
AGENT_NAMES = {
    "analyst": "需求分析 Agent",
    "architect": "架构设计 Agent",
    "coder": "编码 Agent",
    "reviewer": "代码审查 Agent",
}

# 実行順序
AGENT_ORDER = ["analyst", "architect", "coder", "reviewer"]
