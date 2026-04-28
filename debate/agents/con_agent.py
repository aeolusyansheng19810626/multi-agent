"""
反对方 Agent (Con)
"""
from langchain_core.messages import SystemMessage, HumanMessage
from llm import call_with_fallback
from debate.prompts import CON_SYSTEM_PROMPT, CON_HUMAN_PROMPT

def format_history(history):
    if not history:
        return "辩论刚刚开始。"
    formatted = []
    for item in history:
        role = "支持方" if item["role"] == "pro" else "反对方"
        formatted.append(f"{role} (第{item['round']}轮): {item['content']}")
    return "\n\n".join(formatted)

def con_node(state: dict) -> dict:
    code = state["code_input"]
    language = state.get("language", "python")
    current_round = state["current_round"]

    history_str = format_history(state.get("debate_history", []))

    messages = [
        SystemMessage(content=CON_SYSTEM_PROMPT),
        HumanMessage(content=CON_HUMAN_PROMPT.format(
            code=code,
            language=language,
            debate_history=history_str
        )),
    ]

    result = call_with_fallback(messages)

    return {
        "debate_history": [{
            "role": "con",
            "round": current_round,
            "content": result.content
        }],
        "model_used_by": {"con": result.model_used},
    }
