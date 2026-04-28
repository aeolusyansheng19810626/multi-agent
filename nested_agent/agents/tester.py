"""
测试生成 Agent (Tester)
"""
from langchain_core.messages import SystemMessage, HumanMessage
from llm import call_with_fallback
from nested_agent.prompts import TESTER_SYSTEM_PROMPT, TESTER_HUMAN_PROMPT

def tester_node(state: dict) -> dict:
    requirement = state["requirement"]
    code = state.get("coder_output", "未提供代码实现。")
    
    messages = [
        SystemMessage(content=TESTER_SYSTEM_PROMPT),
        HumanMessage(content=TESTER_HUMAN_PROMPT.format(
            requirement=requirement,
            code=code
        )),
    ]

    result = call_with_fallback(messages)

    return {
        "tester_output": result.content,
        "model_used_by": {"tester": result.model_used},
    }
