"""
支持方 Agent (Pro)
"""
from langchain_core.messages import SystemMessage, HumanMessage
from llm import call_with_fallback
from debate.prompts import PRO_SYSTEM_PROMPT, PRO_HUMAN_PROMPT

def format_history(history):
    if not history:
        return "辩论刚刚开始。"
    formatted = []
    for item in history:
        role = "支持方" if item["role"] == "pro" else "反对方"
        formatted.append(f"{role} (第{item['round']}轮): {item['content']}")
    return "\n\n".join(formatted)

def pro_node(state: dict) -> dict:
    code = state["code_input"]
    language = state.get("language", "python")
    # 轮次增加
    new_round = state["current_round"] + 1
    
    history_str = format_history(state.get("debate_history", []))
    
    messages = [
        SystemMessage(content=PRO_SYSTEM_PROMPT),
        HumanMessage(content=PRO_HUMAN_PROMPT.format(
            code=code, 
            language=language,
            debate_history=history_str
        )),
    ]

    result = call_with_fallback(messages)

    return {
        "current_round": new_round,
        "debate_history": [{
            "role": "pro",
            "round": new_round,
            "content": result.content
        }],
        "model_used_by": {"pro": result.model_used},
    }
