"""
Supervisor + LangGraph 图定义
使用 StateGraph 编排四个子 Agent，实现顺序流转的 Supervisor 模式。
"""
from __future__ import annotations

from typing import TypedDict, Optional, Dict
from langgraph.graph import StateGraph, END

from supervisor_pipeline.agents.analyst import analyst_node
from supervisor_pipeline.agents.architect import architect_node
from supervisor_pipeline.agents.coder import coder_node
from supervisor_pipeline.agents.reviewer import reviewer_node


# ── State 定义 ────────────────────────────────────────────
class SupervisorState(TypedDict):
    """贯穿整个图的共享状态"""
    requirement: str                          # 用户原始需求
    analysis_result: Optional[str]            # 需求分析输出
    architecture_result: Optional[str]        # 架构设计输出
    code_result: Optional[str]               # 编码输出
    review_result: Optional[str]             # 代码审查输出
    current_agent: Optional[str]             # 当前执行的 Agent 名称
    model_used_by: Optional[Dict[str, str]]  # 每个 Agent 实际使用的模型名


# ── 构建 StateGraph ───────────────────────────────────────
def build_graph() -> StateGraph:
    """
    构建 Supervisor 工作流图。
    流转顺序：analyst → architect → coder → reviewer → END
    """
    workflow = StateGraph(SupervisorState)

    # 添加节点
    workflow.add_node("analyst", analyst_node)
    workflow.add_node("architect", architect_node)
    workflow.add_node("coder", coder_node)
    workflow.add_node("reviewer", reviewer_node)

    # 设置入口
    workflow.set_entry_point("analyst")

    # 顺序边
    workflow.add_edge("analyst", "architect")
    workflow.add_edge("architect", "coder")
    workflow.add_edge("coder", "reviewer")
    workflow.add_edge("reviewer", END)

    return workflow.compile()


# ── 便捷执行函数 ──────────────────────────────────────────
def run_supervisor(requirement: str) -> dict:
    """
    同步执行整个 Supervisor 工作流。
    返回最终 state，包含所有 Agent 的输出。
    """
    graph = build_graph()
    initial_state: SupervisorState = {
        "requirement": requirement,
        "analysis_result": None,
        "architecture_result": None,
        "code_result": None,
        "review_result": None,
        "current_agent": None,
        "model_used_by": {},
    }
    result = graph.invoke(initial_state)
    return result


def stream_supervisor(requirement: str):
    """
    流式执行 Supervisor 工作流。
    每个节点执行完毕后 yield (node_name, state_update)。
    """
    graph = build_graph()
    initial_state: SupervisorState = {
        "requirement": requirement,
        "analysis_result": None,
        "architecture_result": None,
        "code_result": None,
        "review_result": None,
        "current_agent": None,
        "model_used_by": {},
    }

    for event in graph.stream(initial_state, stream_mode="updates"):
        # event 格式: {node_name: state_update_dict}
        for node_name, state_update in event.items():
            yield node_name, state_update
