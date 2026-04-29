"""
成本分析子 Agent
分析架构方案的成本方面：基础设施成本、许可费用、运维成本、扩展成本等。
"""
from langchain_core.messages import SystemMessage, HumanMessage
from llm import call_with_fallback
from hybrid_b.prompts import COST_SYSTEM_PROMPT, COST_HUMAN_PROMPT


def cost_node(state: dict) -> dict:
    """
    成本分析子 Agent 节点。
    读取 state["scheme"]，输出成本分析报告到 state["cost_result"]。
    """
    scheme = state["scheme"]
    cost_concerns = state.get("cost_focus", "成本分析")

    messages = [
        SystemMessage(content=COST_SYSTEM_PROMPT),
        HumanMessage(content=COST_HUMAN_PROMPT.format(
            scheme=scheme,
            cost_concerns=cost_concerns
        )),
    ]

    result = call_with_fallback(messages)

    return {
        "cost_result": result.content,
        "model_used_by": {"cost": result.model_used},
    }
