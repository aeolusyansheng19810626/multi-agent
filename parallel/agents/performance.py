"""
性能审查 Agent
审查代码中的性能问题：循环嵌套、重复查询、内存分配等。
测试时使用 llama-3.1-8b-instant 单个模型。
"""
from langchain_core.messages import SystemMessage, HumanMessage
from llm import call_with_fallback
from parallel.prompts import PERFORMANCE_SYSTEM_PROMPT, PERFORMANCE_HUMAN_PROMPT


def extract_issues(content: str) -> list:
    """从审查结果中提取问题列表，用于UI显示数量"""
    issues = []
    lines = content.split('\n')
    for line in lines:
        stripped = line.strip()
        if stripped.startswith(('1.', '2.', '3.', '4.', '5.', '6.', '7.', '8.', '9.')):
            issues.append(stripped)
        elif stripped.startswith(('- ', '* ')):
            issues.append(stripped)
    return issues


def performance_node(state: dict) -> dict:
    """
    性能审查 Agent 节点。
    读取 state["code_input"]，输出审查结果到 state["performance_result"]。
    测试时使用 llama-3.1-8b-instant 单个模型。
    """
    code = state["code_input"]
    language = state.get("language", "python")

    messages = [
        SystemMessage(content=PERFORMANCE_SYSTEM_PROMPT),
        HumanMessage(content=PERFORMANCE_HUMAN_PROMPT.format(code=code, language=language)),
    ]

    # 使用默认模型降级列表
    result = call_with_fallback(messages)

    issues = extract_issues(result.content)

    return {
        "performance_result": result.content,
        "performance_issues": issues,
        "model_used_by": {"performance": result.model_used},
    }