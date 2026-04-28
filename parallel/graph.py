"""
Parallel Review - LangGraph 图定义
使用 Send API 实现 fan-out → fan-in 并行模式。
三个审查 Agent 同时处理同一份代码，最后由 Merge Agent 汇总。
"""
from typing import TypedDict, Optional, Dict, List, Annotated
from langgraph.graph import StateGraph, END, START
from langgraph.types import Send

from parallel.agents.security import security_node
from parallel.agents.performance import performance_node
from parallel.agents.maintainability import maintainability_node
from parallel.agents.merger import merge_node


# ── Reducer 定义 ──────────────────────────────────────────
def merge_dicts(left: Optional[dict], right: Optional[dict]) -> dict:
    """合并两个字典，用于并行更新同一状态键"""
    if left is None: left = {}
    if right is None: right = {}
    return {**left, **right}


# ── State 定义 ────────────────────────────────────────────
class ParallelReviewState(TypedDict):
    """并行审查的共享状态"""
    code_input: str                               # 用户输入的代码
    language: Optional[str]                       # 代码语言（用于 Prompt）
    security_result: Optional[str]                # 安全审查输出
    performance_result: Optional[str]             # 性能审查输出
    maintainability_result: Optional[str]         # 可维护性审查输出
    merged_report: Optional[str]                  # 合并后的报告
    # 使用 Annotated 配合 reducer 处理并行更新冲突
    model_used_by: Annotated[Dict[str, str], merge_dicts]
    security_issues: Optional[List[str]]          # 安全问题列表（用于UI显示）
    performance_issues: Optional[List[str]]       # 性能问题列表
    maintainability_issues: Optional[List[str]]   # 可维护性问题列表


# ── Dispatcher 路由函数（用于 add_conditional_edges）──────────
def dispatcher_router(state: dict) -> List[Send]:
    """
    路由函数：使用 Send API 将同一状态分发给3个并行 Agent。
    这是实现真正并行的关键：LangGraph 会同时执行所有 Send 目标。
    """
    # 为每个 Agent 创建独立的状态副本
    security_state = dict(state)
    security_state["agent_type"] = "security"
    
    performance_state = dict(state)
    performance_state["agent_type"] = "performance"
    
    maintainability_state = dict(state)
    maintainability_state["agent_type"] = "maintainability"
    
    return [
        Send("security_agent", security_state),
        Send("performance_agent", performance_state),
        Send("maintainability_agent", maintainability_state),
    ]


# ── 构建 StateGraph ───────────────────────────────────────
def build_graph() -> StateGraph:
    """
    构建并行审查工作流图。
    流程：START → [security, performance, maintainability] (并行) → merger → END
    """
    workflow = StateGraph(ParallelReviewState)

    # 添加节点
    workflow.add_node("security_agent", security_node)
    workflow.add_node("performance_agent", performance_node)
    workflow.add_node("maintainability_agent", maintainability_node)
    workflow.add_node("merge_agent", merge_node)

    # 使用 add_conditional_edges 从入口直接分发任务
    workflow.add_conditional_edges(START, dispatcher_router)

    # fan-in: 所有并行 Agent 完成后进入 merge_agent
    # LangGraph 会自动等待所有并行任务完成
    workflow.add_edge("security_agent", "merge_agent")
    workflow.add_edge("performance_agent", "merge_agent")
    workflow.add_edge("maintainability_agent", "merge_agent")

    # 合并完成后结束
    workflow.add_edge("merge_agent", END)

    return workflow.compile()


# ── 流式执行函数 ──────────────────────────────────────────
def stream_parallel(code_input: str, language: str = "python"):
    """
    流式执行并行审查工作流。
    每个节点执行完毕后 yield (node_name, state_update)。

    Args:
        code_input: 需要审查的代码
        language: 代码语言（python, javascript, java 等）
    """
    graph = build_graph()
    initial_state = {
        "code_input": code_input,
        "language": language,
        "security_result": None,
        "performance_result": None,
        "maintainability_result": None,
        "merged_report": None,
        "model_used_by": {},
        "security_issues": None,
        "performance_issues": None,
        "maintainability_issues": None,
    }

    for event in graph.stream(initial_state, stream_mode="updates"):
        # event 格式: {node_name: state_update_dict}
        for node_name, state_update in event.items():
            yield node_name, state_update