"""
Debate Mode - LangGraphグラフ定義
Pro -> Con -> Loop -> Judgeのディベートワークフローを実装
"""
from typing import TypedDict, Optional, List, Annotated
import operator
from langgraph.graph import StateGraph, END, START

from debate.agents.pro_agent import pro_node
from debate.agents.con_agent import con_node
from debate.agents.judge import judge_node


# Reducer定義
def merge_dicts(left: Optional[dict], right: Optional[dict]) -> dict:
    """辞書をマージ、モデル使用状況を追跡するために使用"""
    if left is None: left = {}
    if right is None: right = {}
    return {**left, **right}

def append_history(left: List[dict], right: List[dict]) -> List[dict]:
    """ディベート履歴を累積"""
    return left + right


# State定義
class DebateState(TypedDict):
    code_input: str                               # ユーザー入力コード
    language: str                                 # コード言語
    current_round: int                            # 現在のラウンド
    max_rounds: int                               # 最大ラウンド数
    # Annotatedを使用してディベートプロセスを記録
    debate_history: Annotated[List[dict], append_history]
    final_conclusion: Optional[str]
    model_used_by: Annotated[dict, merge_dicts]


# ルーティング関数
def router_logic(state: DebateState):
    """ディベートを続けるか審判フェーズに入るかを判定"""
    if state["current_round"] < state["max_rounds"]:
        return "pro_agent"
    return "judge_agent"


# StateGraphを構築
def build_graph() -> StateGraph:
    workflow = StateGraph(DebateState)

    # ノードを追加
    workflow.add_node("pro_agent", pro_node)
    workflow.add_node("con_agent", con_node)
    workflow.add_node("judge_agent", judge_node)

    # フローを設定
    workflow.set_entry_point("pro_agent")

    # Pro -> Con (各ラウンドでProが発言後Conが続く)
    workflow.add_edge("pro_agent", "con_agent")

    # Con後に次のラウンドを続けるか判定
    workflow.add_conditional_edges(
        "con_agent",
        router_logic,
        {
            "pro_agent": "pro_agent",
            "judge_agent": "judge_agent"
        }
    )

    # 審判完了後に終了
    workflow.add_edge("judge_agent", END)

    return workflow.compile()


# ストリーミング実行関数
def stream_debate(code_input: str, language: str = "python", max_rounds: int = 2):
    """
    ディベートワークフローをストリーミング実行
    """
    graph = build_graph()
    initial_state = {
        "code_input": code_input,
        "language": language,
        "current_round": 0, # 第1ラウンド開始前は0
        "max_rounds": max_rounds,
        "debate_history": [],
        "final_conclusion": None,
        "model_used_by": {},
    }

    for event in graph.stream(initial_state, stream_mode="updates"):
        for node_name, state_update in event.items():
            yield node_name, state_update
