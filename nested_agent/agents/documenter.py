"""
文档生成 Agent (Documenter)
"""
from langchain_core.messages import SystemMessage, HumanMessage
from llm import call_with_fallback
from nested_agent.prompts import DOCUMENTER_SYSTEM_PROMPT, DOCUMENTER_HUMAN_PROMPT

def documenter_node(state: dict) -> dict:
    requirement = state["requirement"]
    code = state.get("coder_output", "未提供代码实现。")
    
    messages = [
        SystemMessage(content=DOCUMENTER_SYSTEM_PROMPT),
        HumanMessage(content=DOCUMENTER_HUMAN_PROMPT.format(
            requirement=requirement,
            code=code
        )),
    ]

    result = call_with_fallback(messages)

    return {
        "documenter_output": result.content,
        "model_used_by": {"documenter": result.model_used},
    }
