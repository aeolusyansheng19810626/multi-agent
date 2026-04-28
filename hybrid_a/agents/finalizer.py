"""
最终交付 Agent（新）
将代码、测试、文档、质检状态、安全报告整合为完整的项目交付报告。
"""
from langchain_core.messages import SystemMessage, HumanMessage
from llm import call_with_fallback
from hybrid_a.prompts import FINALIZER_SYSTEM_PROMPT, FINALIZER_HUMAN_PROMPT


def finalizer_node(state: dict) -> dict:
    requirement = state.get("requirement", "")
    code = state.get("code_result", "（未生成）")
    tests = state.get("tester_output", "（未生成）")
    docs = state.get("documenter_output", "（未生成）")
    status = state.get("status", "unknown")
    iteration = state.get("iteration", 0)
    complexity = state.get("complexity", "unknown")
    security_report = state.get("security_result", "未进行安全审查（代码复杂度为简单）")

    review_status = (
        f"✅ 质检通过（第 {iteration} 轮）"
        if status == "pass"
        else f"⚠️ 达到最大迭代次数（{iteration} 轮），强制交付"
    )

    complexity_label = (
        "简单（simple）— 已跳过安全审查"
        if complexity == "simple"
        else "复杂（complex）— 已完成安全审查"
    )

    messages = [
        SystemMessage(content=FINALIZER_SYSTEM_PROMPT),
        HumanMessage(content=FINALIZER_HUMAN_PROMPT.format(
            requirement=requirement,
            code=code,
            tests=tests,
            docs=docs,
            review_status=review_status,
            complexity=complexity_label,
            security_report=security_report,
        )),
    ]

    result = call_with_fallback(messages)

    return {
        "final_output": result.content,
        "model_used_by": {"finalizer": result.model_used},
    }
