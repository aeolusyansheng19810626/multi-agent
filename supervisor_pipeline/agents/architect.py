"""
架构设计 Agent
读取需求分析结果，输出技术选型、模块划分、数据流设计。
"""
from langchain_core.messages import SystemMessage, HumanMessage

from llm import call_with_fallback
from supervisor_pipeline.prompts.architect_prompt import ARCHITECT_SYSTEM_PROMPT, ARCHITECT_HUMAN_PROMPT
from utils import get_language_instruction


def architect_node(state: dict) -> dict:
    """
    LangGraph 节点：架构设计。
    读取 state["analysis_result"]，输出到 state["architecture_result"]。
    """
    analysis_result = state["analysis_result"]
    lang_instruction = get_language_instruction(state.get("language", "en"))

    messages = [
        SystemMessage(content=lang_instruction + "\n\n" + ARCHITECT_SYSTEM_PROMPT),
        HumanMessage(
            content=lang_instruction + "\n\n" + ARCHITECT_HUMAN_PROMPT.format(analysis_result=analysis_result)
        ),
    ]

    result = call_with_fallback(messages)

    return {
        "architecture_result": result.content,
        "current_agent": "architect",
        "model_used_by": {**state.get("model_used_by", {}), "architect": result.model_used},
    }
