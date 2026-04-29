"""
Hybrid A - 混合编排图
三阶段流水线：并行生成 → 循环质检 → 条件分支安全审查 → 最终交付

阶段一（并行）：
  ha_coder → dispatcher → [ha_tester, ha_documenter]（同时）→ ha_reviewer（fan-in）

阶段二（循环反馈）：
  ha_reviewer 不合格 → ha_coder（最多3轮）→ ha_reviewer（直接，跳过并行）

阶段三（条件分支）：
  ha_complexity → simple: ha_finalizer
               → complex: ha_security → ha_finalizer

复用说明：
  ha_coder      → loop_feedback/agents/coder.py
  ha_reviewer   → loop_feedback/agents/reviewer.py
  ha_tester     → nested_agent/agents/tester.py
  ha_documenter → nested_agent/agents/documenter.py
  ha_security   → parallel/agents/security.py
  ha_complexity → hybrid_a/agents/complexity.py（新）
  ha_finalizer  → hybrid_a/agents/finalizer.py（新）
"""
from typing import TypedDict, Optional, Dict, List, Annotated
from langgraph.graph import StateGraph, END, START
from langgraph.types import Send

from loop_feedback.agents.coder import coder_node as _lf_coder
from loop_feedback.agents.reviewer import reviewer_node as _lf_reviewer
from nested_agent.agents.tester import tester_node as _tester
from nested_agent.agents.documenter import documenter_node as _documenter
from parallel.agents.security import security_node as _security
from hybrid_a.agents.complexity import complexity_node
from hybrid_a.agents.finalizer import finalizer_node


# ── Reducer ───────────────────────────────────────────────
def merge_dicts(left: Optional[dict], right: Optional[dict]) -> dict:
    """并行节点同时写 model_used_by 时安全合并"""
    if left is None:
        left = {}
    if right is None:
        right = {}
    return {**left, **right}


# ── State ─────────────────────────────────────────────────
class HybridAState(TypedDict):
    requirement: str

    # 阶段一：并行生成
    code_result: Optional[str]          # lf_coder 写入；lf_reviewer 读取
    coder_output: Optional[str]         # 桥接字段：tester/documenter 读取
    tester_output: Optional[str]
    documenter_output: Optional[str]

    # 阶段二：循环质检
    iteration: int                      # lf_coder 递增
    status: Optional[str]               # lf_reviewer 写入：pass / fail
    feedback: Optional[str]             # lf_reviewer → lf_coder 传递

    # 阶段三：条件分支
    complexity: Optional[str]           # simple / complex
    security_result: Optional[str]
    security_issues: Optional[List[str]]

    # 最终交付
    final_output: Optional[str]

    # 并行安全合并
    model_used_by: Annotated[Dict[str, str], merge_dicts]


# ── 适配器节点（薄包装，不重复业务逻辑）────────────────────

def ha_coder_node(state: dict) -> dict:
    """调用 lf_coder，同时填充桥接字段 coder_output 供 tester/documenter 使用"""
    result = _lf_coder(state)
    # 重新映射 model_used_by 键名：lf_coder → ha_coder
    model_used_by = result.get("model_used_by", {})
    if "lf_coder" in model_used_by:
        model_used_by["ha_coder"] = model_used_by["lf_coder"]
    return {**result, "coder_output": result["code_result"], "model_used_by": model_used_by}


def ha_tester_node(state: dict) -> dict:
    """直接调用 nested_agent tester（读 coder_output，由 ha_coder 已填充）"""
    result = _tester(state)
    # 重新映射 model_used_by 键名：tester → ha_tester
    model_used_by = result.get("model_used_by", {})
    if "tester" in model_used_by:
        model_used_by = {**model_used_by, "ha_tester": model_used_by["tester"]}
    return {**result, "model_used_by": model_used_by}


def ha_documenter_node(state: dict) -> dict:
    """直接调用 nested_agent documenter（读 coder_output，由 ha_coder 已填充）"""
    result = _documenter(state)
    # 重新映射 model_used_by 键名：documenter → ha_documenter
    model_used_by = result.get("model_used_by", {})
    if "documenter" in model_used_by:
        model_used_by = {**model_used_by, "ha_documenter": model_used_by["documenter"]}
    return {**result, "model_used_by": model_used_by}


def ha_reviewer_node(state: dict) -> dict:
    """直接调用 lf_reviewer（读 code_result）"""
    result = _lf_reviewer(state)
    # 重新映射 model_used_by 键名：lf_reviewer → ha_reviewer
    model_used_by = result.get("model_used_by", {})
    if "lf_reviewer" in model_used_by:
        model_used_by = {**model_used_by, "ha_reviewer": model_used_by["lf_reviewer"]}
    return {**result, "model_used_by": model_used_by}


def ha_security_node(state: dict) -> dict:
    """桥接 code_result → code_input，再调用 parallel security"""
    adapted = {
        **state,
        "code_input": state.get("code_result", ""),
        "language": "python",
    }
    result = _security(adapted)
    # 重新映射 model_used_by 键名：security → ha_security
    model_used_by = result.get("model_used_by", {})
    if "security" in model_used_by:
        model_used_by = {**model_used_by, "ha_security": model_used_by["security"]}
    return {**result, "model_used_by": model_used_by}


def _dispatcher_node(state: dict) -> dict:
    """并行分发中转节点，状态透传"""
    return {"model_used_by": {}}


# ── 路由函数 ──────────────────────────────────────────────

def route_after_coder(state: dict) -> str:
    """
    第 1 轮（iteration==1）→ dispatcher 启动并行 tester/documenter
    后续轮次（iteration>=2）→ 直接进 ha_reviewer（跳过并行，避免重复生成）
    """
    iteration = state.get("iteration", 1)
    if iteration <= 1:
        return "dispatcher"
    return "ha_reviewer"


def parallel_dispatcher(state: dict) -> List[Send]:
    """Fan-out：同时派发 ha_tester 和 ha_documenter"""
    return [
        Send("ha_tester", state),
        Send("ha_documenter", state),
    ]


def review_condition(state: dict) -> str:
    """质检结果路由：通过或到达最大轮次 → 进入复杂度判断；否则打回重做"""
    status = state.get("status", "fail")
    iteration = state.get("iteration", 0)
    if status == "pass" or iteration >= 3:
        return "ha_complexity"
    return "ha_coder"


def complexity_route(state: dict) -> str:
    """复杂度路由：复杂 → 安全审查；简单 → 直接交付"""
    complexity = state.get("complexity", "simple")
    if complexity == "complex":
        return "ha_security"
    return "ha_finalizer"


# ── 构建 StateGraph ───────────────────────────────────────

def build_graph():
    workflow = StateGraph(HybridAState)

    # 注册节点
    workflow.add_node("ha_coder", ha_coder_node)
    workflow.add_node("dispatcher", _dispatcher_node)
    workflow.add_node("ha_tester", ha_tester_node)
    workflow.add_node("ha_documenter", ha_documenter_node)
    workflow.add_node("ha_reviewer", ha_reviewer_node)
    workflow.add_node("ha_complexity", complexity_node)
    workflow.add_node("ha_security", ha_security_node)
    workflow.add_node("ha_finalizer", finalizer_node)

    # 入口
    workflow.set_entry_point("ha_coder")

    # 阶段一路由：第1轮 → 并行，后续轮 → 直接审查
    workflow.add_conditional_edges(
        "ha_coder",
        route_after_coder,
        {
            "dispatcher": "dispatcher",
            "ha_reviewer": "ha_reviewer",
        },
    )

    # 并行 fan-out
    workflow.add_conditional_edges(
        "dispatcher",
        parallel_dispatcher,
        ["ha_tester", "ha_documenter"],
    )

    # fan-in：两个并行节点都完成后才进入 ha_reviewer
    workflow.add_edge("ha_tester", "ha_reviewer")
    workflow.add_edge("ha_documenter", "ha_reviewer")

    # 阶段二路由：质检通过/超限 → 复杂度判断；否则打回
    workflow.add_conditional_edges(
        "ha_reviewer",
        review_condition,
        {
            "ha_complexity": "ha_complexity",
            "ha_coder": "ha_coder",
        },
    )

    # 阶段三路由：复杂 → 安全审查；简单 → 直接交付
    workflow.add_conditional_edges(
        "ha_complexity",
        complexity_route,
        {
            "ha_security": "ha_security",
            "ha_finalizer": "ha_finalizer",
        },
    )

    workflow.add_edge("ha_security", "ha_finalizer")
    workflow.add_edge("ha_finalizer", END)

    return workflow.compile()


# ── 流式执行函数 ──────────────────────────────────────────

def stream_hybrid_a(requirement: str):
    """
    流式执行混合 A 工作流。
    每个节点完成后 yield (node_name, state_update)。
    """
    graph = build_graph()
    initial_state: HybridAState = {
        "requirement": requirement,
        "code_result": None,
        "coder_output": None,
        "tester_output": None,
        "documenter_output": None,
        "iteration": 0,
        "status": None,
        "feedback": None,
        "complexity": None,
        "security_result": None,
        "security_issues": None,
        "final_output": None,
        "model_used_by": {},
    }

    for event in graph.stream(initial_state, stream_mode="updates"):
        for node_name, state_update in event.items():
            yield node_name, state_update
