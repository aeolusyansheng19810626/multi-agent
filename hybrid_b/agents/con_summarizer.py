"""
反对方汇总 Agent
基于安全分析和可维护性分析的数据，生成反对论点。
"""
from langchain_core.messages import SystemMessage, HumanMessage
from llm import call_with_fallback
from hybrid_b.prompts import CON_SUMMARIZER_SYSTEM_PROMPT, CON_SUMMARIZER_HUMAN_PROMPT


def format_history(history):
    """格式化辩论历史"""
    if not history:
        return "辩论刚刚开始。"
    formatted = []
    for item in history:
        role = "支持方" if item["role"] == "pro" else "反对方"
        formatted.append(f"【{role} 第{item['round']}轮】\n{item['content']}")
    return "\n\n" + "=" * 50 + "\n\n".join(formatted)


def con_summarizer_node(state: dict) -> dict:
    """
    反对方汇总节点。
    读取 state 中的安全分析和可维护性分析结果，生成反对论点。
    """
    scheme = state["scheme"]
    current_round = state["current_round"]
    security_result = state.get("security_result", "未获得安全分析数据")
    maintainability_result = state.get("maintainability_result", "未获得可维护性分析数据")
    debate_history = state.get("debate_history", [])
    
    # 获取对方上一轮论点
    opponent_info = ""
    if debate_history:
        last_entry = debate_history[-1]
        if last_entry["role"] == "pro":
            opponent_info = f"\n对方上一轮论点：\n{last_entry['content']}"
    
    messages = [
        SystemMessage(content=CON_SUMMARIZER_SYSTEM_PROMPT.format(
            current_round=current_round,
            opponent_info=opponent_info
        )),
        HumanMessage(content=CON_SUMMARIZER_HUMAN_PROMPT.format(
            scheme=scheme,
            security_result=security_result,
            maintainability_result=maintainability_result,
            debate_history=format_history(debate_history)
        )),
    ]

    result = call_with_fallback(messages)

    return {
        "debate_history": [{
            "role": "con",
            "round": current_round,
            "content": result.content,
            "security_result": security_result,
            "maintainability_result": maintainability_result,
        }],
        "model_used_by": {"con_summarizer": result.model_used},
    }
