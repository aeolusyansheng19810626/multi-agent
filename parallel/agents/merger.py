"""
合并 Agent
整合三个审查结果（安全、性能、可维护性），生成统一报告。
测试时使用 llama-3.1-8b-instant 单个模型。
"""
from langchain_core.messages import SystemMessage, HumanMessage
from llm import call_with_fallback
from parallel.prompts import MERGER_SYSTEM_PROMPT, MERGER_HUMAN_PROMPT


def merge_node(state: dict) -> dict:
    """
    合并 Agent 节点。
    读取三个审查结果，输出统一报告到 state["merged_report"]。
    测试时使用 llama-3.1-8b-instant 单个模型。
    """
    security_result = state.get("security_result", "未进行安全审查")
    performance_result = state.get("performance_result", "未进行性能审查")
    maintainability_result = state.get("maintainability_result", "未进行可维护性审查")

    messages = [
        SystemMessage(content=MERGER_SYSTEM_PROMPT),
        HumanMessage(content=MERGER_HUMAN_PROMPT.format(
            security_result=security_result,
            performance_result=performance_result,
            maintainability_result=maintainability_result,
        )),
    ]

    # 使用默认模型降级列表
    result = call_with_fallback(messages)

    return {
        "merged_report": result.content,
        "model_used_by": {"merger": result.model_used},
    }