"""
LLM統一呼び出し層 - モデルフォールバック機構
全エージェントはcall_with_fallback()経由でモデルを呼び出し、直接LLMをインスタンス化しない
"""
from __future__ import annotations

import logging
from dataclasses import dataclass
from typing import List

from langchain_groq import ChatGroq
from langchain_core.messages import BaseMessage

from config import GROQ_API_KEY, MODEL_FALLBACK_LIST, LLM_TEMPERATURE, LLM_MAX_TOKENS

logger = logging.getLogger(__name__)


@dataclass
class LLMResponse:
    """LLM呼び出し結果をカプセル化、コンテンツと実際に使用されたモデル名を含む"""
    content: str
    model_used: str


def call_with_fallback(
    messages: List[BaseMessage],
    fallback_list: List[str] | None = None,
    temperature: float | None = None,
    max_tokens: int | None = None,
) -> LLMResponse:
    """
    フォールバックリストのモデルを順次試行し、成功したら結果を返して実際に使用したモデル名を記録、
    失敗したら次のモデルを自動的に試行

    Args:
        messages: LangChainメッセージリスト (SystemMessage + HumanMessage)
        fallback_list: モデルフォールバックリスト、デフォルトはconfig.MODEL_FALLBACK_LIST
        temperature: デフォルト温度を上書き
        max_tokens: デフォルトmax_tokensを上書き

    Returns:
        LLMResponse: contentとmodel_usedを含む

    Raises:
        RuntimeError: 全モデルの呼び出しが失敗
    """
    models = fallback_list or MODEL_FALLBACK_LIST
    temp = temperature if temperature is not None else LLM_TEMPERATURE
    tokens = max_tokens if max_tokens is not None else LLM_MAX_TOKENS

    errors: list[tuple[str, str]] = []

    for model_name in models:
        try:
            logger.info(f"モデル呼び出し試行: {model_name}")

            llm = ChatGroq(
                api_key=GROQ_API_KEY,
                model=model_name,
                temperature=temp,
                max_tokens=tokens,
            )

            response = llm.invoke(messages)

            logger.info(f"✓ モデル呼び出し成功: {model_name}")
            return LLMResponse(
                content=response.content,
                model_used=model_name,
            )

        except Exception as e:
            error_msg = f"{type(e).__name__}: {str(e)[:200]}"
            errors.append((model_name, error_msg))
            logger.warning(f"✗ モデル {model_name} 呼び出し失敗: {error_msg}")
            continue

    # 全モデル失敗
    error_details = "\n".join(f"  - {m}: {e}" for m, e in errors)
    raise RuntimeError(
        f"全 {len(models)} モデルの呼び出しが失敗:\n{error_details}"
    )
