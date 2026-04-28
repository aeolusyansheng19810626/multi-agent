"""
复杂度评估 Agent（新）
读取 code_result，判断代码是 simple 还是 complex，决定后续是否需要安全审查。
"""
import json
from langchain_core.messages import SystemMessage, HumanMessage
from llm import call_with_fallback
from hybrid_a.prompts import COMPLEXITY_SYSTEM_PROMPT, COMPLEXITY_HUMAN_PROMPT


def complexity_node(state: dict) -> dict:
    code = state.get("code_result", "")

    messages = [
        SystemMessage(content=COMPLEXITY_SYSTEM_PROMPT),
        HumanMessage(content=COMPLEXITY_HUMAN_PROMPT.format(code=code)),
    ]

    result = call_with_fallback(messages)

    # 解析 JSON 结果
    complexity = "simple"
    try:
        content = result.content.strip()
        if content.startswith("```json"):
            content = content[7:]
        if content.startswith("```"):
            content = content[3:]
        if content.endswith("```"):
            content = content[:-3]
        parsed = json.loads(content.strip())
        raw = parsed.get("complexity", "simple")
        complexity = raw if raw in ("simple", "complex") else "simple"
    except Exception:
        complexity = "simple"

    return {
        "complexity": complexity,
        "model_used_by": {"complexity": result.model_used},
    }
