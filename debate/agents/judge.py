"""
裁判 Agent (Judge)
"""
from langchain_core.messages import SystemMessage, HumanMessage
from llm import call_with_fallback
from debate.prompts import JUDGE_SYSTEM_PROMPT, JUDGE_HUMAN_PROMPT

def format_history(history):
    if not history:
        return "无辩论过程。"
    formatted = []
    for item in history:
        role = "支持方" if item["role"] == "pro" else "反对方"
        formatted.append(f"【{role} 第{item['round']}轮】\n{item['content']}")
    return "\n\n".join(formatted)

def judge_node(state: dict) -> dict:
    code = state["code_input"]
    language = state.get("language", "python")
    
    history_str = format_history(state.get("debate_history", []))
    
    messages = [
        SystemMessage(content=JUDGE_SYSTEM_PROMPT),
        HumanMessage(content=JUDGE_HUMAN_PROMPT.format(
            code=code, 
            language=language,
            debate_history=history_str
        )),
    ]

    result = call_with_fallback(messages)

    return {
        "final_conclusion": result.content,
        "model_used_by": {"judge": result.model_used},
    }
