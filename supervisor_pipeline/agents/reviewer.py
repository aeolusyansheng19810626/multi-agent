"""
代码审查 Agent
读取编码结果，输出潜在风险、改进建议、评分。
"""
from langchain_core.messages import SystemMessage, HumanMessage

from llm import call_with_fallback
from supervisor_pipeline.prompts.reviewer_prompt import REVIEWER_SYSTEM_PROMPT, REVIEWER_HUMAN_PROMPT
from utils import get_language_instruction


def reviewer_node(state: dict) -> dict:
    """
    LangGraph 节点：代码审查。
    读取 state["code_result"]，输出到 state["review_result"]。
    """
    code_result = state["code_result"]
    lang_instruction = get_language_instruction(state.get("language", "en"))

    messages = [
        SystemMessage(content=lang_instruction + "\n\n" + REVIEWER_SYSTEM_PROMPT),
        HumanMessage(
            content=lang_instruction + "\n\n" + REVIEWER_HUMAN_PROMPT.format(code_result=code_result)
        ),
    ]

    result = call_with_fallback(messages)

    return {
        "review_result": result.content,
        "current_agent": "reviewer",
        "model_used_by": {**state.get("model_used_by", {}), "reviewer": result.model_used},
    }
