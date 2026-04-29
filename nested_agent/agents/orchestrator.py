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
    req_lower = requirement.lower()
    
    # 规则匹配：检测用户明确的排除意图
    code_only_keywords = ["只要代码", "只需要代码", "仅代码", "只要实现", "只写实现", "only code", "code only"]
    no_test_keywords = ["不需要测试", "不要测试", "无需测试", "no test", "without test"]
    no_doc_keywords = ["不需要文档", "不要文档", "无需文档", "no doc", "without doc"]
    
    force_plan = None
    force_reason = None
    
    # 检测"只要代码"类关键词
    if any(kw in req_lower for kw in code_only_keywords):
        force_plan = {"coder": True, "tester": False, "documenter": False}
        force_reason = "用户明确要求只要代码，跳过测试和文档生成"
    else:
        # 检测单独的排除项
        exclude_tester = any(kw in req_lower for kw in no_test_keywords)
        exclude_documenter = any(kw in req_lower for kw in no_doc_keywords)
        
        if exclude_tester or exclude_documenter:
            force_plan = {
                "coder": True,
                "tester": not exclude_tester,
                "documenter": not exclude_documenter
            }
            reasons = []
            if exclude_tester:
                reasons.append("跳过测试")
            if exclude_documenter:
                reasons.append("跳过文档")
            force_reason = f"用户明确要求{', '.join(reasons)}"
    
    # 如果有强制规划，直接返回
    if force_plan:
        return {
            "plan": force_plan,
            "plan_reason": force_reason,
            "model_used_by": {"orchestrator": "rule-based"},
        }
    
    # 否则调用LLM进行智能规划
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
        # 兜底：简单任务默认只要代码
        plan = {"coder": True, "tester": False, "documenter": False}
        reason = "解析规划 JSON 失败，采用保守方案（仅代码）。"

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
