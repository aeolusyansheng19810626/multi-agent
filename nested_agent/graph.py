"""
Nested Agent - LangGraph 图定义
实现 Orchestrator -> [Coder -> Tester, Documenter] -> Finalizer 的嵌套调用。
"""
import json
from typing import TypedDict, Optional, List, Dict, Annotated
from langgraph.graph import StateGraph, END, START
from langgraph.types import Send

from nested_agent.agents.orchestrator import orchestrator_node, finalizer_node
from nested_agent.agents.coder import coder_node
from nested_agent.agents.tester import tester_node
from nested_agent.agents.documenter import documenter_node


# ── Reducer 定义 ──────────────────────────────────────────
def merge_dicts(left: Optional[dict], right: Optional[dict]) -> dict:
    if left is None: left = {}
    if right is None: right = {}
    return {**left, **right}


# ── State 定义 ────────────────────────────────────────────
class NestedState(TypedDict):
    requirement: str                              # 原始需求
    plan: Optional[Dict[str, bool]]               # Orchestrator 的规划结果
    plan_reason: Optional[str]                    # 规划理由
    
    coder_output: Optional[str]                   # Coder 产出
    tester_output: Optional[str]                  # Tester 产出
    documenter_output: Optional[str]              # Documenter 产出
    
    final_output: Optional[str]                   # 最终整合结果
    model_used_by: Annotated[dict, merge_dicts]


# ── 路由函数 ──────────────────────────────────────────────
def route_after_plan(state: NestedState):
    """Orchestrator 规划后，决定是否进入 Coder 阶段"""
    plan = state.get("plan", {})
    if plan.get("coder"):
        return "coder_agent"
    return "executor_dispatcher"


def executor_dispatcher(state: NestedState) -> List[Send]:
    """
    核心调度逻辑：根据规划并行召唤 Tester 和 Documenter。
    """
    plan = state.get("plan", {})
    sends = []
    
    if plan.get("tester"):
        sends.append(Send("tester_agent", state))
        
    if plan.get("documenter"):
        sends.append(Send("documenter_agent", state))
        
    return sends if sends else [Send("finalizer_agent", state)]


# ── 构建 StateGraph ───────────────────────────────────────
def build_graph() -> StateGraph:
    workflow = StateGraph(NestedState)

    # 添加节点
    workflow.add_node("orchestrator_agent", orchestrator_node)
    workflow.add_node("coder_agent", coder_node)
    workflow.add_node("tester_agent", tester_node)
    workflow.add_node("documenter_agent", documenter_node)
    workflow.add_node("finalizer_agent", finalizer_node)

    # 设置入口
    workflow.set_entry_point("orchestrator_agent")

    # 1. 规划后路由
    workflow.add_conditional_edges(
        "orchestrator_agent",
        route_after_plan,
        {
            "coder_agent": "coder_agent",
            "executor_dispatcher": "finalizer_agent" # 如果什么都不需要，直接去最终化 (虽然逻辑上不太可能)
        }
    )
    
    # 2. Coder 完后去分发并行任务 (或者从 orchestrator 跳过 coder 直接去分发)
    # 注意：LangGraph 不直接支持在 add_node 之外定义 dispatcher 函数作为 Send 目标
    # 我们需要一个中转节点来执行 executor_dispatcher
    def dispatcher_node(state: NestedState):
        return state # 仅仅作为中转
    
    workflow.add_node("dispatcher", dispatcher_node)
    
    workflow.add_edge("coder_agent", "dispatcher")
    
    # 从 orchestrator 如果不需要 coder，也去 dispatcher
    # (修改上面的 route_after_plan 逻辑中的目标为 dispatcher)
    
    # 重新定义路由逻辑以配合 dispatcher 节点
    workflow.add_conditional_edges(
        "orchestrator_agent",
        lambda state: "coder_agent" if state.get("plan", {}).get("coder") else "dispatcher",
        {
            "coder_agent": "coder_agent",
            "dispatcher": "dispatcher"
        }
    )

    # 3. 从 Dispatcher 扇出
    workflow.add_conditional_edges(
        "dispatcher",
        executor_dispatcher,
        ["tester_agent", "documenter_agent", "finalizer_agent"]
    )

    # 4. 扇入：并行任务完成后汇聚到 finalizer
    workflow.add_edge("tester_agent", "finalizer_agent")
    workflow.add_edge("documenter_agent", "finalizer_agent")

    # 5. 结束
    workflow.add_edge("finalizer_agent", END)

    return workflow.compile()


# ── 流式执行函数 ──────────────────────────────────────────
def stream_nested(requirement: str):
    """
    流式执行嵌套 Agent 工作流。
    """
    graph = build_graph()
    initial_state = {
        "requirement": requirement,
        "plan": None,
        "plan_reason": None,
        "coder_output": None,
        "tester_output": None,
        "documenter_output": None,
        "final_output": None,
        "model_used_by": {},
    }

    for event in graph.stream(initial_state, stream_mode="updates"):
        for node_name, state_update in event.items():
            yield node_name, state_update
