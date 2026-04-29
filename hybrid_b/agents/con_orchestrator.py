"""
反对方 Orchestrator Agent
负责召唤安全分析子Agent和可维护性分析子Agent，然后汇总生成反对论点。
"""
import json
from langchain_core.messages import SystemMessage, HumanMessage
from llm import call_with_fallback
from hybrid_b.prompts import (
    CON_ORCHESTRATOR_SYSTEM_PROMPT, 
    CON_ORCHESTRATOR_HUMAN_PROMPT
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


def con_orchestrator_node(state: dict) -> dict:
    """
    反对方 Orchestrator 节点。
    1. 分析架构方案，制定子Agent分析计划
    2. 返回分析计划，由 graph 负责召唤子Agent
    """
    scheme = state["scheme"]
    current_round = state["current_round"]  # 保持当前轮次，与支持方相同
    debate_history = state.get("debate_history", [])
    
    # 获取对方所有论点（用于反驳）
    opponent_info = ""
    pro_arguments = [item for item in debate_history if item["role"] == "pro"]
    if pro_arguments:
        opponent_info = "\n对方所有论点：\n"
        for arg in pro_arguments:
            opponent_info += f"【第{arg['round']}轮】{arg['content'][:500]}...\n"
    
    messages = [
        SystemMessage(content=CON_ORCHESTRATOR_SYSTEM_PROMPT.format(
            current_round=current_round,
            opponent_info=opponent_info
        )),
        HumanMessage(content=CON_ORCHESTRATOR_HUMAN_PROMPT.format(
            scheme=scheme,
            debate_history=format_history(debate_history)
        )),
    ]

    result = call_with_fallback(messages)
    
    # 解析 JSON 计划
    try:
        plan = json.loads(result.content)
        security_focus = "\n".join(plan.get("security_focus", []))
        maintainability_issues = "\n".join(plan.get("maintainability_issues", []))
        strategy = plan.get("strategy", "")
    except:
        # 如果解析失败，使用默认内容
        security_focus = "安全分析"
        maintainability_issues = "可维护性分析"
        strategy = result.content[:200]
    
    return {
        "security_focus": security_focus,
        "maintainability_focus": maintainability_issues,
        "con_strategy": strategy,
        "model_used_by": {"con_orchestrator": result.model_used},
    }
