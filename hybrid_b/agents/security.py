"""
安全分析子 Agent
分析架构方案的安全方面：数据泄露风险、访问控制、注入攻击等。
"""
from langchain_core.messages import SystemMessage, HumanMessage
from llm import call_with_fallback
from hybrid_b.prompts import SECURITY_SYSTEM_PROMPT, SECURITY_HUMAN_PROMPT


def security_node(state: dict) -> dict:
    """
    安全分析子 Agent 节点。
    读取 state["scheme"]，输出安全分析报告到 state["security_result"]。
    """
    scheme = state["scheme"]
    security_focus = state.get("security_focus", "安全分析")

    messages = [
        SystemMessage(content=SECURITY_SYSTEM_PROMPT),
        HumanMessage(content=SECURITY_HUMAN_PROMPT.format(
            scheme=scheme,
            security_focus=security_focus
        )),
    ]

    result = call_with_fallback(messages)

    return {
        "security_result": result.content,
        "model_used_by": {"security": result.model_used},
    }
