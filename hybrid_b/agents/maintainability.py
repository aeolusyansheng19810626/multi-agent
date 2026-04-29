"""
可维护性分析子 Agent
分析架构方案的可维护性方面：复杂度、文档完整性、监控和调试、团队技能要求等。
"""
from langchain_core.messages import SystemMessage, HumanMessage
from llm import call_with_fallback
from hybrid_b.prompts import MAINTAINABILITY_SYSTEM_PROMPT, MAINTAINABILITY_HUMAN_PROMPT


def maintainability_node(state: dict) -> dict:
    """
    可维护性分析子 Agent 节点。
    读取 state["scheme"]，输出可维护性分析报告到 state["maintainability_result"]。
    """
    scheme = state["scheme"]
    maintainability_issues = state.get("maintainability_focus", "可维护性分析")

    messages = [
        SystemMessage(content=MAINTAINABILITY_SYSTEM_PROMPT),
        HumanMessage(content=MAINTAINABILITY_HUMAN_PROMPT.format(
            scheme=scheme,
            maintainability_issues=maintainability_issues
        )),
    ]

    result = call_with_fallback(messages)

    return {
        "maintainability_result": result.content,
        "model_used_by": {"maintainability": result.model_used},
    }
