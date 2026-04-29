"""
支持方 Orchestrator Agent
负责召唤性能分析子Agent和成本分析子Agent，然后汇总生成支持论点。
"""
import json
from langchain_core.messages import SystemMessage, HumanMessage
from llm import call_with_fallback
from hybrid_b.prompts import (
    PRO_ORCHESTRATOR_SYSTEM_PROMPT, 
    PRO_ORCHESTRATOR_HUMAN_PROMPT
)


def format_history(history):
    """格式化辩论历史"""
    if not history:
        return "辩论刚刚开始。"
    formatted = []
    for item in history:
        role = "支持方" if item["role"] == "pro" else "反对方"
        formatted.append(f"【{role} 第{item['round']}轮】\n{item['content'][:500]}...")
    return "\n\n".join(formatted)


def pro_orchestrator_node(state: dict) -> dict:
    """
    支持方 Orchestrator 节点。
    1. 分析架构方案，制定子Agent分析计划
    2. 返回分析计划，由 graph 负责召唤子Agent
    """
    scheme = state["scheme"]
    current_round = state.get("current_round", 0) + 1
    debate_history = state.get("debate_history", [])
    
    # 获取对方所有论点（用于反驳）
    opponent_info = ""
    con_arguments = [item for item in debate_history if item["role"] == "con"]
    if con_arguments:
        opponent_info = "\n对方所有论点：\n"
        for arg in con_arguments:
            opponent_info += f"【第{arg['round']}轮】{arg['content'][:500]}...\n"
    
    messages = [
        SystemMessage(content=PRO_ORCHESTRATOR_SYSTEM_PROMPT.format(
            current_round=current_round,
            opponent_info=opponent_info
        )),
        HumanMessage(content=PRO_ORCHESTRATOR_HUMAN_PROMPT.format(
            scheme=scheme,
            debate_history=format_history(debate_history)
        )),
    ]

    result = call_with_fallback(messages)
    
    # 解析 JSON 计划
    try:
        plan = json.loads(result.content)
        focus_areas = "\n".join(plan.get("focus_areas", []))
        cost_concerns = "\n".join(plan.get("cost_concerns", []))
        strategy = plan.get("strategy", "")
    except:
        # 如果解析失败，使用默认内容
        focus_areas = "性能分析"
        cost_concerns = "成本分析"
        strategy = result.content[:200]
    
    return {
        "current_round": current_round,
        "performance_focus": focus_areas,
        "cost_focus": cost_concerns,
        "pro_strategy": strategy,
        "model_used_by": {"pro_orchestrator": result.model_used},
    }
