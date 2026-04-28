"""
安全审查 Agent
审查代码中的安全问题：SQL注入、硬编码密码、未校验输入等。
测试时使用 llama-3.1-8b-instant 单个模型。
"""
from langchain_core.messages import SystemMessage, HumanMessage
from llm import call_with_fallback
from parallel.prompts import SECURITY_SYSTEM_PROMPT, SECURITY_HUMAN_PROMPT


def extract_issues(content: str) -> list:
    """从审查结果中提取问题列表，用于UI显示数量"""
    issues = []
    lines = content.split('\n')
    for line in lines:
        stripped = line.strip()
        # 匹配编号列表项（1. 2. 3. 或 - *）
        if stripped.startswith(('1.', '2.', '3.', '4.', '5.', '6.', '7.', '8.', '9.')):
            issues.append(stripped)
        elif stripped.startswith(('- ', '* ')):
            issues.append(stripped)
    return issues


def security_node(state: dict) -> dict:
    """
    安全审查 Agent 节点。
    读取 state["code_input"]，输出审查结果到 state["security_result"]。
    测试时使用 llama-3.1-8b-instant 单个模型。
    """
    code = state["code_input"]
    language = state.get("language", "python")

    messages = [
        SystemMessage(content=SECURITY_SYSTEM_PROMPT),
        HumanMessage(content=SECURITY_HUMAN_PROMPT.format(code=code, language=language)),
    ]

    # 使用默认模型降级列表
    result = call_with_fallback(messages)

    issues = extract_issues(result.content)

    return {
        "security_result": result.content,
        "security_issues": issues,
        "model_used_by": {"security": result.model_used},
    }