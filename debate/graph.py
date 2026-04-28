"""
Debate Mode - LangGraph 图定义
实现 Pro -> Con -> Loop -> Judge 的辩论工作流。
"""
from typing import TypedDict, Optional, List, Annotated
import operator
from langgraph.graph import StateGraph, END, START

from debate.agents.pro_agent import pro_node
from debate.agents.con_agent import con_node
from debate.agents.judge import judge_node


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
class DebateState(TypedDict):
    code_input: str                               # 用户输入的代码
    language: str                                 # 代码语言
    current_round: int                            # 当前轮次
    max_rounds: int                               # 最大轮次
    # 使用 Annotated 记录辩论过程
    debate_history: Annotated[List[dict], append_history] 
    final_conclusion: Optional[str]
    model_used_by: Annotated[dict, merge_dicts]


# ── 路由函数 ──────────────────────────────────────────────
def router_logic(state: DebateState):
    """判断是继续辩论还是进入裁判环节"""
    if state["current_round"] < state["max_rounds"]:
        return "pro_agent"
    return "judge_agent"


# ── 构建 StateGraph ───────────────────────────────────────
def build_graph() -> StateGraph:
    workflow = StateGraph(DebateState)

    # 添加节点
    workflow.add_node("pro_agent", pro_node)
    workflow.add_node("con_agent", con_node)
    workflow.add_node("judge_agent", judge_node)

    # 设置流程
    workflow.set_entry_point("pro_agent")

    # Pro -> Con (每轮 Pro 说完 Con 接着说)
    workflow.add_edge("pro_agent", "con_agent")

    # Con 之后判断是否继续下一轮
    workflow.add_conditional_edges(
        "con_agent",
        router_logic,
        {
            "pro_agent": "pro_agent",
            "judge_agent": "judge_agent"
        }
    )

    # 裁判完结束
    workflow.add_edge("judge_agent", END)

    return workflow.compile()


# ── 流式执行函数 ──────────────────────────────────────────
def stream_debate(code_input: str, language: str = "python", max_rounds: int = 2):
    """
    流式执行辩论工作流。
    """
    graph = build_graph()
    initial_state = {
        "code_input": code_input,
        "language": language,
        "current_round": 0, # 开始第1轮前是0
        "max_rounds": max_rounds,
        "debate_history": [],
        "final_conclusion": None,
        "model_used_by": {},
    }

    for event in graph.stream(initial_state, stream_mode="updates"):
        for node_name, state_update in event.items():
            yield node_name, state_update
