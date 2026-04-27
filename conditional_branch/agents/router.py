import json
from langchain_core.messages import SystemMessage, HumanMessage
from llm import call_with_fallback
from conditional_branch.prompts.all_prompts import ROUTER_SYSTEM_PROMPT, ROUTER_HUMAN_PROMPT

def router_node(state: dict) -> dict:
    requirement = state["requirement"]
    messages = [
        SystemMessage(content=ROUTER_SYSTEM_PROMPT),
        HumanMessage(content=ROUTER_HUMAN_PROMPT.format(requirement=requirement)),
    ]
    
    result = call_with_fallback(messages)
    
    # 尝试解析 JSON
    try:
        # 清理可能被 Markdown 代码块包裹的 JSON
        content = result.content.strip()
        if content.startswith("```json"):
            content = content[7:]
        if content.startswith("```"):
            content = content[3:]
        if content.endswith("```"):
            content = content[:-3]
        content = content.strip()
        
        parsed = json.loads(content)
        route = parsed.get("route", "new_feature")
        reason = parsed.get("reason", "解析成功")
    except Exception as e:
        # 解析失败时的后备默认值
        route = "new_feature"
        reason = f"JSON解析失败，默认走 new_feature。错误: {str(e)}"

    return {
        "router_decision": {"route": route, "reason": reason},
        "current_agent": "router",
        "model_used_by": {**state.get("model_used_by", {}), "router": result.model_used},
    }
