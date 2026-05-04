"""
Nested Agent - LangGraphグラフ定義
Orchestrator -> [Coder -> Tester, Documenter] -> Finalizerのネスト呼び出しを実装
"""
import json
from typing import TypedDict, Optional, List, Dict, Annotated
from langgraph.graph import StateGraph, END, START
from langgraph.types import Send

from nested_agent.agents.orchestrator import orchestrator_node, finalizer_node
from nested_agent.agents.coder import coder_node
from nested_agent.agents.tester import tester_node
from nested_agent.agents.documenter import documenter_node


# Reducer定義
def merge_dicts(left: Optional[dict], right: Optional[dict]) -> dict:
    if left is None: left = {}
    if right is None: right = {}
    return {**left, **right}


# State定義
class NestedState(TypedDict):
    requirement: str                              # 元の要件
    plan: Optional[Dict[str, bool]]               # Orchestratorの計画結果
    plan_reason: Optional[str]                    # 計画理由
    
    coder_output: Optional[str]                   # Coder出力
    tester_output: Optional[str]                  # Tester出力
    documenter_output: Optional[str]              # Documenter出力
    
    final_output: Optional[str]                   # 最終統合結果
    model_used_by: Annotated[dict, merge_dicts]


# ルーティング関数
def route_after_plan(state: NestedState):
    """Orchestrator計画後、Coderフェーズに入るかを決定"""
    plan = state.get("plan", {})
    if plan.get("coder"):
        return "coder_agent"
    return "executor_dispatcher"


def executor_dispatcher(state: NestedState) -> List[Send]:
    """
    コア調整ロジック：計画に基づいてTesterとDocumenterを並列呼び出し
    """
    plan = state.get("plan", {})
    sends = []
    
    if plan.get("tester"):
        sends.append(Send("tester_agent", state))
        
    if plan.get("documenter"):
        sends.append(Send("documenter_agent", state))
        
    return sends if sends else [Send("finalizer_agent", state)]


# StateGraphを構築
def build_graph() -> StateGraph:
    workflow = StateGraph(NestedState)

    # ノードを追加
    workflow.add_node("orchestrator_agent", orchestrator_node)
    workflow.add_node("coder_agent", coder_node)
    workflow.add_node("tester_agent", tester_node)
    workflow.add_node("documenter_agent", documenter_node)
    workflow.add_node("finalizer_agent", finalizer_node)

    # エントリーポイントを設定
    workflow.set_entry_point("orchestrator_agent")

    # 1. 計画後のルーティング
    workflow.add_conditional_edges(
        "orchestrator_agent",
        route_after_plan,
        {
            "coder_agent": "coder_agent",
            "executor_dispatcher": "finalizer_agent" # 何も不要な場合は直接最終化へ（論理的にはあり得ないが）
        }
    )
    
    # 2. Coder完了後に並列タスクを分配（またはorchestratorからcoderをスキップして直接分配）
    # 注意：LangGraphはadd_node外でdispatcher関数をSend対象として定義することを直接サポートしない
    # executor_dispatcherを実行するための中継ノードが必要
    def dispatcher_node(state: NestedState):
        return state # 中継のみ
    
    workflow.add_node("dispatcher", dispatcher_node)
    
    workflow.add_edge("coder_agent", "dispatcher")
    
    # orchestratorからcoderが不要な場合もdispatcherへ
    # （上記のroute_after_planロジックの対象をdispatcherに変更）
    
    # dispatcherノードに合わせてルーティングロジックを再定義
    workflow.add_conditional_edges(
        "orchestrator_agent",
        lambda state: "coder_agent" if state.get("plan", {}).get("coder") else "dispatcher",
        {
            "coder_agent": "coder_agent",
            "dispatcher": "dispatcher"
        }
    )

    # 3. Dispatcherからfan-out
    workflow.add_conditional_edges(
        "dispatcher",
        executor_dispatcher,
        ["tester_agent", "documenter_agent", "finalizer_agent"]
    )

    # 4. fan-in：並列タスク完了後にfinalizerへ集約
    workflow.add_edge("tester_agent", "finalizer_agent")
    workflow.add_edge("documenter_agent", "finalizer_agent")

    # 5. 終了
    workflow.add_edge("finalizer_agent", END)

    return workflow.compile()


# ストリーミング実行関数
def stream_nested(requirement: str):
    """
    ネストエージェントワークフローをストリーミング実行
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
