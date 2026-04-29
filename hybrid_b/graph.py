"""
Hybrid B - LangGraph 图定义
辩论模式 + 嵌套 Agent 的结合。
每一方辩论时召唤专项子 Agent 收集数据，再基于数据发言。

流程：
第1轮：支持方(召唤性能+成本) → 反对方(召唤安全+维护性)
第2轮：支持方(反驳+召唤子Agent) → 反对方(反驳+召唤子Agent)
裁判：综合所有数据给出最终建议
"""
from typing import TypedDict, Optional, List, Dict, Annotated
import operator
from langgraph.graph import StateGraph, END, START
from langgraph.types import Send

from hybrid_b.agents.pro_orchestrator import pro_orchestrator_node
from hybrid_b.agents.con_orchestrator import con_orchestrator_node
from hybrid_b.agents.performance import performance_node
from hybrid_b.agents.cost import cost_node
from hybrid_b.agents.security import security_node
from hybrid_b.agents.maintainability import maintainability_node
from hybrid_b.agents.pro_summarizer import pro_summarizer_node
from hybrid_b.agents.con_summarizer import con_summarizer_node
from hybrid_b.agents.judge import judge_node


# ── Reducer 定义 ──────────────────────────────────────────
def merge_dicts(left: Optional[dict], right: Optional[dict]) -> dict:
    """合并字典，用于追踪模型使用情况"""
    if left is None: left = {}
    if right is None: right = {}
    return {**left, **right}


def append_history(left: List[dict], right: List[dict]) -> List[dict]:
    """累加辩论历史"""
    return left + right


# ── State 定义 ────────────────────────────────────────────
class HybridBState(TypedDict):
    """Hybrid B 的共享状态"""
    scheme: str                                    # 用户输入的架构方案
    current_round: int                             # 当前轮次
    max_rounds: int                                # 最大轮次（默认2）
    
    # 支持方数据
    performance_focus: Optional[str]               # 性能分析重点
    cost_focus: Optional[str]                      # 成本分析重点
    performance_result: Optional[str]               # 性能分析结果
    cost_result: Optional[str]                     # 成本分析结果
    pro_strategy: Optional[str]                    # 支持方策略
    
    # 反对方数据
    security_focus: Optional[str]                  # 安全分析重点
    maintainability_focus: Optional[str]           # 可维护性分析重点
    security_result: Optional[str]                 # 安全分析结果
    maintainability_result: Optional[str]          # 可维护性分析结果
    con_strategy: Optional[str]                    # 反对方策略
    
    # 辩论历史（使用 Annotated + reducer 累加）
    debate_history: Annotated[List[dict], append_history]
    
    # 最终裁决
    final_conclusion: Optional[str]
    
    # 模型使用记录（使用 Annotated + reducer 合并）
    model_used_by: Annotated[Dict[str, str], merge_dicts]


# ── Dispatcher 路由函数（用于 Send API）────────────────────
def pro_dispatcher(state: HybridBState) -> List[Send]:
    """
    支持方调度器：使用 Send API 将状态分发给性能Agent和成本Agent。
    """
    return [
        Send("performance_agent", state),
        Send("cost_agent", state),
    ]


def con_dispatcher(state: HybridBState) -> List[Send]:
    """
    反对方调度器：使用 Send API 将状态分发给安全Agent和可维护性Agent。
    """
    return [
        Send("security_agent", state),
        Send("maintainability_agent", state),
    ]


# ── 循环条件判断 ──────────────────────────────────────────
def should_continue(state: HybridBState) -> str:
    """判断是继续下一轮辩论还是进入裁判环节"""
    if state["current_round"] < state["max_rounds"]:
        return "pro_orchestrator"
    return "judge_agent"


# ── 构建 StateGraph ───────────────────────────────────────
def build_graph() -> StateGraph:
    """
    构建 Hybrid B 工作流图。
    
    流程：
    START → pro_orchestrator → pro_dispatcher → [performance, cost] → pro_summarizer
          → con_orchestrator → con_dispatcher → [security, maintainability] → con_summarizer
          → (循环或进入裁判)
          → judge_agent → END
    """
    workflow = StateGraph(HybridBState)
    
    # 添加所有节点
    workflow.add_node("pro_orchestrator", pro_orchestrator_node)
    workflow.add_node("con_orchestrator", con_orchestrator_node)
    workflow.add_node("performance_agent", performance_node)
    workflow.add_node("cost_agent", cost_node)
    workflow.add_node("security_agent", security_node)
    workflow.add_node("maintainability_agent", maintainability_node)
    workflow.add_node("pro_summarizer", pro_summarizer_node)
    workflow.add_node("con_summarizer", con_summarizer_node)
    workflow.add_node("judge_agent", judge_node)
    
    # 设置入口
    workflow.set_entry_point("pro_orchestrator")
    
    # 1. 支持方 Orchestrator 之后，调度子Agent（并行）
    workflow.add_conditional_edges(
        "pro_orchestrator",
        pro_dispatcher,
        ["performance_agent", "cost_agent"]
    )
    
    # 2. 子Agent 完成后，进入汇总器（LangGraph 会等待所有并行任务完成）
    workflow.add_edge("performance_agent", "pro_summarizer")
    workflow.add_edge("cost_agent", "pro_summarizer")
    
    # 3. 支持方汇总后，进入反对方 Orchestrator
    workflow.add_edge("pro_summarizer", "con_orchestrator")
    
    # 4. 反对方 Orchestrator 之后，调度子Agent（并行）
    workflow.add_conditional_edges(
        "con_orchestrator",
        con_dispatcher,
        ["security_agent", "maintainability_agent"]
    )
    
    # 5. 子Agent 完成后，进入汇总器
    workflow.add_edge("security_agent", "con_summarizer")
    workflow.add_edge("maintainability_agent", "con_summarizer")
    
    # 6. 反对方汇总后，判断是否继续循环
    workflow.add_conditional_edges(
        "con_summarizer",
        should_continue,
        {
            "pro_orchestrator": "pro_orchestrator",
            "judge_agent": "judge_agent",
        }
    )
    
    # 7. 裁判完后结束
    workflow.add_edge("judge_agent", END)
    
    return workflow.compile()


# ── 流式执行函数 ──────────────────────────────────────────
def stream_hybrid_b(scheme: str, max_rounds: int = 2):
    """
    流式执行 Hybrid B 工作流。
    
    Args:
        scheme: 架构方案
        max_rounds: 最大辩论轮次（默认2轮）
    
    Yields:
        (node_name, state_update) 元组
    """
    graph = build_graph()
    initial_state: HybridBState = {
        "scheme": scheme,
        "current_round": 0,  # 开始第1轮前是0，pro_orchestrator会+1
        "max_rounds": max_rounds,
        "performance_focus": None,
        "cost_focus": None,
        "performance_result": None,
        "cost_result": None,
        "pro_strategy": None,
        "security_focus": None,
        "maintainability_focus": None,
        "security_result": None,
        "maintainability_result": None,
        "con_strategy": None,
        "debate_history": [],
        "final_conclusion": None,
        "model_used_by": {},
    }
    
    for event in graph.stream(initial_state, stream_mode="updates"):
        for node_name, state_update in event.items():
            yield node_name, state_update
