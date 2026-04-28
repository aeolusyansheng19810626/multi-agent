"""
代码生成 Agent (Coder)
"""
from langchain_core.messages import SystemMessage, HumanMessage
from llm import call_with_fallback
from nested_agent.prompts import CODER_SYSTEM_PROMPT, CODER_HUMAN_PROMPT

def coder_node(state: dict) -> dict:
    requirement = state["requirement"]
    
    messages = [
        SystemMessage(content=CODER_SYSTEM_PROMPT),
        HumanMessage(content=CODER_HUMAN_PROMPT.format(requirement=requirement)),
    ]

    result = call_with_fallback(messages)

    return {
        "coder_output": result.content,
        "model_used_by": {"coder": result.model_used},
    }
