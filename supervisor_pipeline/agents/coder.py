"""
编码 Agent
读取架构设计结果，输出核心模块的代码框架。
"""
from langchain_core.messages import SystemMessage, HumanMessage

from llm import call_with_fallback
from supervisor_pipeline.prompts.coder_prompt import CODER_SYSTEM_PROMPT, CODER_HUMAN_PROMPT
from utils import get_language_instruction


def coder_node(state: dict) -> dict:
    """
    LangGraph 节点：编码。
    读取 state["architecture_result"]，输出到 state["code_result"]。
    """
    architecture_result = state["architecture_result"]
    lang_instruction = get_language_instruction(state.get("language", "en"))

    messages = [
        SystemMessage(content=lang_instruction + "\n\n" + CODER_SYSTEM_PROMPT),
        HumanMessage(
            content=lang_instruction + "\n\n" + CODER_HUMAN_PROMPT.format(architecture_result=architecture_result)
        ),
    ]

    result = call_with_fallback(messages)

    return {
        "code_result": result.content,
        "current_agent": "coder",
        "model_used_by": {**state.get("model_used_by", {}), "coder": result.model_used},
    }
