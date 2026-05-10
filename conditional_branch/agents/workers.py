from langchain_core.messages import SystemMessage, HumanMessage
from llm import call_with_fallback
from conditional_branch.prompts.all_prompts import (
    ANALYST_SYSTEM_PROMPT, ARCHITECT_SYSTEM_PROMPT, CODER_SYSTEM_PROMPT,
    REVIEWER_SYSTEM_PROMPT, OPTIMIZER_SYSTEM_PROMPT,
    RESEARCHER_SYSTEM_PROMPT, ADVISOR_SYSTEM_PROMPT,
    GENERIC_HUMAN_PROMPT
)
from utils import get_language_instruction


def create_worker_node(agent_name: str, system_prompt: str, input_key: str, output_key: str):
    def node(state: dict) -> dict:
        input_text = state.get(input_key, "")
        if not input_text and input_key == "requirement":
            input_text = state.get("requirement", "")

        lang_instruction = get_language_instruction(state.get("language", "en"))
        messages = [
            SystemMessage(content=lang_instruction + "\n\n" + system_prompt),
            HumanMessage(content=lang_instruction + "\n\n" + GENERIC_HUMAN_PROMPT.format(input_text=input_text)),
        ]

        result = call_with_fallback(messages)

        return {
            output_key: result.content,
            "current_agent": agent_name,
            "model_used_by": {**state.get("model_used_by", {}), agent_name: result.model_used},
        }
    return node

# New Feature Path
cb_analyst_node = create_worker_node("cb_analyst", ANALYST_SYSTEM_PROMPT, "requirement", "analysis_result")
cb_architect_node = create_worker_node("cb_architect", ARCHITECT_SYSTEM_PROMPT, "analysis_result", "architecture_result")
cb_coder_node = create_worker_node("cb_coder", CODER_SYSTEM_PROMPT, "architecture_result", "code_result")

# Code Review Path
cb_reviewer_node = create_worker_node("cb_reviewer", REVIEWER_SYSTEM_PROMPT, "requirement", "review_result")
cb_optimizer_node = create_worker_node("cb_optimizer", OPTIMIZER_SYSTEM_PROMPT, "review_result", "optimization_result")

# Tech Question Path
cb_researcher_node = create_worker_node("cb_researcher", RESEARCHER_SYSTEM_PROMPT, "requirement", "research_result")
cb_advisor_node = create_worker_node("cb_advisor", ADVISOR_SYSTEM_PROMPT, "research_result", "advice_result")
