from langchain_core.messages import SystemMessage, HumanMessage
from llm import call_with_fallback
from loop_feedback.prompts import CODER_SYSTEM_PROMPT, CODER_HUMAN_PROMPT

def coder_node(state: dict) -> dict:
    requirement = state.get("requirement", "")
    feedback = state.get("feedback", "无")
    iteration = state.get("iteration", 0)
    
    # 当前轮次+1
    new_iteration = iteration + 1
    
    messages = [
        SystemMessage(content=CODER_SYSTEM_PROMPT),
        HumanMessage(content=CODER_HUMAN_PROMPT.format(requirement=requirement, feedback=feedback)),
    ]
    
    result = call_with_fallback(messages)
    
    return {
        "code_result": result.content,
        "iteration": new_iteration,
        "current_agent": "lf_coder",
        "model_used_by": {**state.get("model_used_by", {}), "lf_coder": result.model_used},
    }
