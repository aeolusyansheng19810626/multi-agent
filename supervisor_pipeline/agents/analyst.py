"""
需求分析 Agent
将用户原始需求拆解为用户故事、功能列表、边界条件。
"""
from langchain_core.messages import SystemMessage, HumanMessage

from llm import call_with_fallback
from supervisor_pipeline.prompts.analyst_prompt import ANALYST_SYSTEM_PROMPT, ANALYST_HUMAN_PROMPT


def analyst_node(state: dict) -> dict:
    """
    LangGraph 节点：需求分析。
    读取 state["requirement"]，输出分析结果到 state["analysis_result"]。
    """
    requirement = state["requirement"]

    messages = [
        SystemMessage(content=ANALYST_SYSTEM_PROMPT),
        HumanMessage(content=ANALYST_HUMAN_PROMPT.format(requirement=requirement)),
    ]

    result = call_with_fallback(messages)

    return {
        "analysis_result": result.content,
        "current_agent": "analyst",
        "model_used_by": {**state.get("model_used_by", {}), "analyst": result.model_used},
    }
