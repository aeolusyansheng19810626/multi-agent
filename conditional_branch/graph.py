from typing import TypedDict, Optional, Dict, Any
from langgraph.graph import StateGraph, END

from conditional_branch.agents.router import router_node
from conditional_branch.agents.workers import (
    cb_analyst_node, cb_architect_node, cb_coder_node,
    cb_reviewer_node, cb_optimizer_node,
    cb_researcher_node, cb_advisor_node
)

class ConditionalState(TypedDict):
    requirement: str
    router_decision: Optional[Dict[str, str]]
    
    # New Feature Path
    analysis_result: Optional[str]
    architecture_result: Optional[str]
    code_result: Optional[str]
    
    # Code Review Path
    review_result: Optional[str]
    optimization_result: Optional[str]
    
    # Tech Question Path
    research_result: Optional[str]
    advice_result: Optional[str]
    
    current_agent: Optional[str]
    model_used_by: Optional[Dict[str, str]]

def route_condition(state: ConditionalState) -> str:
    """路由决策函数，返回要走向的下一个节点名"""
    decision = state.get("router_decision", {})
    route = decision.get("route", "new_feature")
    
    if route == "code_review":
        return "cb_reviewer"
    elif route == "tech_question":
        return "cb_researcher"
    else: # 默认 fallback 到 new_feature
        return "cb_analyst"

def build_graph() -> StateGraph:
    workflow = StateGraph(ConditionalState)

    # 注册所有节点
    workflow.add_node("router", router_node)
    
    workflow.add_node("cb_analyst", cb_analyst_node)
    workflow.add_node("cb_architect", cb_architect_node)
    workflow.add_node("cb_coder", cb_coder_node)
    
    workflow.add_node("cb_reviewer", cb_reviewer_node)
    workflow.add_node("cb_optimizer", cb_optimizer_node)
    
    workflow.add_node("cb_researcher", cb_researcher_node)
    workflow.add_node("cb_advisor", cb_advisor_node)

    # 入口节点
    workflow.set_entry_point("router")

    # 条件分支
    workflow.add_conditional_edges(
        "router",
        route_condition,
        {
            "cb_analyst": "cb_analyst",
            "cb_reviewer": "cb_reviewer",
            "cb_researcher": "cb_researcher"
        }
    )

    # Path 1: New Feature
    workflow.add_edge("cb_analyst", "cb_architect")
    workflow.add_edge("cb_architect", "cb_coder")
    workflow.add_edge("cb_coder", END)

    # Path 2: Code Review
    workflow.add_edge("cb_reviewer", "cb_optimizer")
    workflow.add_edge("cb_optimizer", END)

    # Path 3: Tech Question
    workflow.add_edge("cb_researcher", "cb_advisor")
    workflow.add_edge("cb_advisor", END)

    return workflow.compile()

def stream_conditional(requirement: str):
    graph = build_graph()
    initial_state: ConditionalState = {
        "requirement": requirement,
        "router_decision": None,
        "analysis_result": None,
        "architecture_result": None,
        "code_result": None,
        "review_result": None,
        "optimization_result": None,
        "research_result": None,
        "advice_result": None,
        "current_agent": None,
        "model_used_by": {},
    }

    for event in graph.stream(initial_state, stream_mode="updates"):
        for node_name, state_update in event.items():
            yield node_name, state_update
