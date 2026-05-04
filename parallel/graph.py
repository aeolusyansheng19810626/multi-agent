"""
Parallel Review - LangGraphグラフ定義
Send APIを使用してfan-out → fan-in並列パターンを実装
3つのレビューエージェントが同じコードを同時処理し、最後にMergeエージェントが統合
"""
from typing import TypedDict, Optional, Dict, List, Annotated
from langgraph.graph import StateGraph, END, START
from langgraph.types import Send

from parallel.agents.security import security_node
from parallel.agents.performance import performance_node
from parallel.agents.maintainability import maintainability_node
from parallel.agents.merger import merge_node


# Reducer定義
def merge_dicts(left: Optional[dict], right: Optional[dict]) -> dict:
    """2つの辞書をマージ、並列更新で同じステートキーを処理するために使用"""
    if left is None: left = {}
    if right is None: right = {}
    return {**left, **right}


# State定義
class ParallelReviewState(TypedDict):
    """並列レビューの共有ステート"""
    code_input: str                               # ユーザー入力コード
    language: Optional[str]                       # コード言語（プロンプト用）
    security_result: Optional[str]                # セキュリティレビュー出力
    performance_result: Optional[str]             # パフォーマンスレビュー出力
    maintainability_result: Optional[str]         # 保守性レビュー出力
    merged_report: Optional[str]                  # マージ後のレポート
    # Annotatedとreducerを使用して並列更新の競合を処理
    model_used_by: Annotated[Dict[str, str], merge_dicts]
    security_issues: Optional[List[str]]          # セキュリティ問題リスト（UI表示用）
    performance_issues: Optional[List[str]]       # パフォーマンス問題リスト
    maintainability_issues: Optional[List[str]]   # 保守性問題リスト


# Dispatcherルーティング関数（add_conditional_edges用）
def dispatcher_router(state: dict) -> List[Send]:
    """
    ルーティング関数：Send APIを使用して同じステートを3つの並列エージェントに分配
    これが真の並列処理を実現する鍵：LangGraphは全てのSend対象を同時実行
    """
    # 各エージェント用に独立したステートコピーを作成
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


# StateGraphを構築
def build_graph() -> StateGraph:
    """
    並列レビューワークフローグラフを構築
    フロー：START → [security, performance, maintainability] (並列) → merger → END
    """
    workflow = StateGraph(ParallelReviewState)

    # ノードを追加
    workflow.add_node("security_agent", security_node)
    workflow.add_node("performance_agent", performance_node)
    workflow.add_node("maintainability_agent", maintainability_node)
    workflow.add_node("merge_agent", merge_node)

    # add_conditional_edgesを使用してエントリーから直接タスクを分配
    workflow.add_conditional_edges(START, dispatcher_router)

    # fan-in: 全並列エージェント完了後にmerge_agentへ
    # LangGraphは全並列タスクの完了を自動的に待機
    workflow.add_edge("security_agent", "merge_agent")
    workflow.add_edge("performance_agent", "merge_agent")
    workflow.add_edge("maintainability_agent", "merge_agent")

    # マージ完了後に終了
    workflow.add_edge("merge_agent", END)

    return workflow.compile()


# ストリーミング実行関数
def stream_parallel(code_input: str, language: str = "python"):
    """
    並列レビューワークフローをストリーミング実行
    各ノード実行完了後に(node_name, state_update)をyield

    Args:
        code_input: レビュー対象のコード
        language: コード言語（python, javascript, java等）
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
        # eventフォーマット: {node_name: state_update_dict}
        for node_name, state_update in event.items():
            yield node_name, state_update