"""
裁判 Agent (Judge)
综合所有轮次的辩论数据，给出最终采纳/否决建议。
"""
from langchain_core.messages import SystemMessage, HumanMessage
from llm import call_with_fallback
from hybrid_b.prompts import JUDGE_SYSTEM_PROMPT, JUDGE_HUMAN_PROMPT


def format_history(history):
    """格式化完整辩论历史，包含子Agent数据"""
    if not history:
        return "无辩论过程。"
    
    formatted = []
    for item in history:
        role = "支持方" if item["role"] == "pro" else "反对方"
        entry = f"【{role} 第{item['round']}轮】\n"
        entry += f"论点：\n{item['content']}\n"
        
        # 添加子Agent数据
        if item.get("performance_result"):
            entry += f"\n性能分析数据：\n{item['performance_result'][:500]}...\n"
        if item.get("cost_result"):
            entry += f"\n成本分析数据：\n{item['cost_result'][:500]}...\n"
        if item.get("security_result"):
            entry += f"\n安全分析数据：\n{item['security_result'][:500]}...\n"
        if item.get("maintainability_result"):
            entry += f"\n可维护性分析数据：\n{item['maintainability_result'][:500]}...\n"
        
        formatted.append(entry)
    
    return "\n\n" + "="*50 + "\n\n".join(formatted)


def judge_node(state: dict) -> dict:
    """
    裁判节点。
    读取完整辩论历史，输出最终裁决。
    """
    scheme = state["scheme"]
    debate_history = state.get("debate_history", [])
    
    messages = [
        SystemMessage(content=JUDGE_SYSTEM_PROMPT),
        HumanMessage(content=JUDGE_HUMAN_PROMPT.format(
            scheme=scheme,
            debate_history=format_history(debate_history)
        )),
    ]

    result = call_with_fallback(messages)

    return {
        "final_conclusion": result.content,
        "model_used_by": {"judge": result.model_used},
    }
