"""
支持方汇总 Agent
基于性能分析和成本分析的数据，生成支持论点。
"""
from langchain_core.messages import SystemMessage, HumanMessage
from llm import call_with_fallback
from hybrid_b.prompts import PRO_SUMMARIZER_SYSTEM_PROMPT, PRO_SUMMARIZER_HUMAN_PROMPT


def format_history(history):
    """格式化辩论历史"""
    if not history:
        return "辩论刚刚开始。"
    formatted = []
    for item in history:
        role = "支持方" if item["role"] == "pro" else "反对方"
        formatted.append(f"【{role} 第{item['round']}轮】\n{item['content']}")
    return "\n\n" + "=" * 50 + "\n\n".join(formatted)


def pro_summarizer_node(state: dict) -> dict:
    """
    支持方汇总节点。
    读取 state 中的性能分析和成本分析结果，生成支持论点。
    """
    scheme = state["scheme"]
    current_round = state["current_round"]
    performance_result = state.get("performance_result", "未获得性能分析数据")
    cost_result = state.get("cost_result", "未获得成本分析数据")
    debate_history = state.get("debate_history", [])
    
    # 获取对方上一轮论点
    opponent_info = ""
    if debate_history:
        last_entry = debate_history[-1]
        if last_entry["role"] == "con":
            opponent_info = f"\n对方上一轮论点：\n{last_entry['content']}"
    
    messages = [
        SystemMessage(content=PRO_SUMMARIZER_SYSTEM_PROMPT.format(
            current_round=current_round,
            opponent_info=opponent_info
        )),
        HumanMessage(content=PRO_SUMMARIZER_HUMAN_PROMPT.format(
            scheme=scheme,
            performance_result=performance_result,
            cost_result=cost_result,
            debate_history=format_history(debate_history)
        )),
    ]

    result = call_with_fallback(messages)

    return {
        "debate_history": [{
            "role": "pro",
            "round": current_round,
            "content": result.content,
            "performance_result": performance_result,
            "cost_result": cost_result,
        }],
        "model_used_by": {"pro_summarizer": result.model_used},
    }
