"""
协调者 Agent (Orchestrator)
"""
import json
from langchain_core.messages import SystemMessage, HumanMessage
from llm import call_with_fallback
from nested_agent.prompts import (
    ORCHESTRATOR_PLAN_SYSTEM_PROMPT, 
    ORCHESTRATOR_PLAN_HUMAN_PROMPT,
    ORCHESTRATOR_FINALIZE_SYSTEM_PROMPT,
    ORCHESTRATOR_FINALIZE_HUMAN_PROMPT
)

def orchestrator_node(state: dict) -> dict:
    requirement = state["requirement"]
    
    messages = [
        SystemMessage(content=ORCHESTRATOR_PLAN_SYSTEM_PROMPT),
        HumanMessage(content=ORCHESTRATOR_PLAN_HUMAN_PROMPT.format(requirement=requirement)),
    ]

    result = call_with_fallback(messages)
    
    try:
        # 尝试清理和解析 JSON
        clean_content = result.content.strip()
        if "```json" in clean_content:
            clean_content = clean_content.split("```json")[1].split("```")[0].strip()
        elif "```" in clean_content:
            clean_content = clean_content.split("```")[1].split("```")[0].strip()
            
        data = json.loads(clean_content)
        plan = data.get("plan", {})
        reason = data.get("reason", "未提供理由")
    except Exception:
        # 兜底：如果解析失败，默认全部启用
        plan = {"coder": True, "tester": True, "documenter": True}
        reason = "解析规划 JSON 失败，采用默认全量方案。"

    return {
        "plan": plan,
        "plan_reason": reason,
        "model_used_by": {"orchestrator": result.model_used},
    }

def finalizer_node(state: dict) -> dict:
    requirement = state["requirement"]
    results = []
    
    if state.get("coder_output"):
        results.append(f"【实现代码】\n{state['coder_output']}")
    if state.get("tester_output"):
        results.append(f"【单元测试】\n{state['tester_output']}")
    if state.get("documenter_output"):
        results.append(f"【技术文档】\n{state['documenter_output']}")
        
    results_str = "\n\n".join(results)
    
    messages = [
        SystemMessage(content=ORCHESTRATOR_FINALIZE_SYSTEM_PROMPT),
        HumanMessage(content=ORCHESTRATOR_FINALIZE_HUMAN_PROMPT.format(
            requirement=requirement,
            results=results_str
        )),
    ]

    result = call_with_fallback(messages)

    return {
        "final_output": result.content,
        "model_used_by": {"finalizer": result.model_used},
    }
