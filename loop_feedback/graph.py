from typing import TypedDict, Optional, Dict
from langgraph.graph import StateGraph, END

from loop_feedback.agents.coder import coder_node
from loop_feedback.agents.reviewer import reviewer_node

class LoopState(TypedDict):
    requirement: str
    language: str
    code_result: Optional[str]
    iteration: int
    status: Optional[str]
    feedback: Optional[str]
    current_agent: Optional[str]
    model_used_by: Optional[Dict[str, str]]

def review_condition(state: LoopState) -> str:
    """次のステップがリトライか終了かを決定"""
    status = state.get("status", "fail")
    iteration = state.get("iteration", 0)
    
    if status == "pass":
        return END
    
    if iteration >= 3:
        return END
        
    return "lf_coder"

def build_graph() -> StateGraph:
    workflow = StateGraph(LoopState)

    workflow.add_node("lf_coder", coder_node)
    workflow.add_node("lf_reviewer", reviewer_node)

    workflow.set_entry_point("lf_coder")

    workflow.add_edge("lf_coder", "lf_reviewer")
    
    workflow.add_conditional_edges(
        "lf_reviewer",
        review_condition,
        {
            "lf_coder": "lf_coder",
            END: END
        }
    )

    return workflow.compile()

def stream_loop(requirement: str, language: str = "en"):
    graph = build_graph()
    initial_state: LoopState = {
        "requirement": requirement,
        "language": language,
        "code_result": None,
        "iteration": 0,
        "status": None,
        "feedback": None,
        "current_agent": None,
        "model_used_by": {},
    }

    for event in graph.stream(initial_state, stream_mode="updates"):
        for node_name, state_update in event.items():
            yield node_name, state_update
