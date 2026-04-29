import json
import re
from langchain_core.messages import SystemMessage, HumanMessage
from llm import call_with_fallback
from conditional_branch.prompts.all_prompts import ROUTER_SYSTEM_PROMPT, ROUTER_HUMAN_PROMPT


def _extract_json_object(content: str) -> str:
    """Extract the first JSON object from an LLM response."""
    text = content.strip()
    if text.startswith("```json"):
        text = text[7:]
    if text.startswith("```"):
        text = text[3:]
    if text.endswith("```"):
        text = text[:-3]
    text = text.strip()

    if text.startswith("{") and text.endswith("}"):
        return text

    match = re.search(r"\{.*\}", text, re.DOTALL)
    if match:
        return match.group(0)
    return text


def _fallback_route(requirement: str) -> tuple[str, str]:
    """Choose a safer route when the model response cannot be parsed."""
    text = requirement.strip()
    lowered = text.lower()

    code_markers = [
        "```",
        "def ",
        "class ",
        "function ",
        "const ",
        "let ",
        "var ",
        "import ",
        "from ",
        "return ",
        "public ",
        "private ",
        "console.log",
    ]
    review_markers = ["审查", "review", "bug", "优化", "报错", "有没有坑", "看看这段"]
    tech_question_markers = ["选型", "哪个好", "对比", "方案", "架构", "为什么", "如何", "怎么"]

    if any(marker in lowered for marker in code_markers) or any(marker in text for marker in review_markers):
        return "code_review", "JSON解析失败，但输入包含明显代码或审查意图，兜底走 code_review。"

    if any(marker in text for marker in tech_question_markers) or " vs " in lowered or "?" in text or "？" in text:
        return "tech_question", "JSON解析失败，但输入更像技术问题或方案选型，兜底走 tech_question。"

    return "new_feature", "JSON解析失败，未发现明显代码或技术问答特征，兜底走 new_feature。"


def router_node(state: dict) -> dict:
    requirement = state["requirement"]
    messages = [
        SystemMessage(content=ROUTER_SYSTEM_PROMPT),
        HumanMessage(content=ROUTER_HUMAN_PROMPT.format(requirement=requirement)),
    ]
    
    result = call_with_fallback(messages)
    
    # 尝试解析 JSON
    try:
        content = _extract_json_object(result.content)
        parsed = json.loads(content)
        route = parsed.get("route", "new_feature")
        reason = parsed.get("reason", "解析成功")
        if route not in {"new_feature", "code_review", "tech_question"}:
            route, reason = _fallback_route(requirement)
            reason = f"模型返回了未知 route，{reason}"
    except Exception as e:
        route, fallback_reason = _fallback_route(requirement)
        reason = f"{fallback_reason} 错误: {str(e)}"

    return {
        "router_decision": {"route": route, "reason": reason},
        "current_agent": "router",
        "model_used_by": {**state.get("model_used_by", {}), "router": result.model_used},
    }
