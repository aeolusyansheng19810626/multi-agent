import json
from langchain_core.messages import SystemMessage, HumanMessage
from llm import call_with_fallback
from loop_feedback.prompts import REVIEWER_SYSTEM_PROMPT, REVIEWER_HUMAN_PROMPT

def reviewer_node(state: dict) -> dict:
    code_result = state.get("code_result", "")
    
    messages = [
        SystemMessage(content=REVIEWER_SYSTEM_PROMPT),
        HumanMessage(content=REVIEWER_HUMAN_PROMPT.format(code_result=code_result)),
    ]
    
    result = call_with_fallback(messages)
    
    # 尝试解析 JSON
    try:
        content = result.content.strip()
        if content.startswith("```json"):
            content = content[7:]
        if content.startswith("```"):
            content = content[3:]
        if content.endswith("```"):
            content = content[:-3]
        content = content.strip()
        
        parsed = json.loads(content)
        status = parsed.get("status", "fail")
        feedback = parsed.get("feedback", "JSON格式解析失败，请检查并重新生成。")
        
        # 确保 status 只能是 pass 或 fail
        if status not in ["pass", "fail"]:
             status = "fail"
             
    except Exception as e:
        status = "fail"
        feedback = f"JSON解析失败: {str(e)}。原始内容: {result.content}"

    return {
        "status": status,
        "feedback": feedback,
        "current_agent": "lf_reviewer",
        "model_used_by": {**state.get("model_used_by", {}), "lf_reviewer": result.model_used},
    }
