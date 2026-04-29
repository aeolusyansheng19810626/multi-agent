"""
性能分析子 Agent
分析架构方案的性能方面：响应时间、资源消耗、可扩展性、缓存策略等。
"""
from langchain_core.messages import SystemMessage, HumanMessage
from llm import call_with_fallback
from hybrid_b.prompts import PERFORMANCE_SYSTEM_PROMPT, PERFORMANCE_HUMAN_PROMPT


def performance_node(state: dict) -> dict:
    """
    性能分析子 Agent 节点。
    读取 state["scheme"]，输出性能分析报告到 state["performance_result"]。
    """
    scheme = state["scheme"]
    focus_areas = state.get("performance_focus", "性能分析")

    messages = [
        SystemMessage(content=PERFORMANCE_SYSTEM_PROMPT),
        HumanMessage(content=PERFORMANCE_HUMAN_PROMPT.format(
            scheme=scheme,
            focus_areas=focus_areas
        )),
    ]

    result = call_with_fallback(messages)

    return {
        "performance_result": result.content,
        "model_used_by": {"performance": result.model_used},
    }
