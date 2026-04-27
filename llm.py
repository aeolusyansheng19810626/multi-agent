"""
LLM 统一调用层 — 模型降级 Fallback 机制
所有 Agent 统一通过 call_with_fallback() 调用模型，不直接实例化 LLM。
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
    """封装 LLM 调用结果，包含内容和实际使用的模型名"""
    content: str
    model_used: str


def call_with_fallback(
    messages: List[BaseMessage],
    fallback_list: List[str] | None = None,
    temperature: float | None = None,
    max_tokens: int | None = None,
) -> LLMResponse:
    """
    依次尝试降级列表中的模型，成功则返回结果并记录实际使用的模型名，
    失败则自动尝试下一个。

    Args:
        messages: LangChain 消息列表 (SystemMessage + HumanMessage)
        fallback_list: 模型降级列表，默认使用 config.MODEL_FALLBACK_LIST
        temperature: 覆盖默认温度
        max_tokens: 覆盖默认 max_tokens

    Returns:
        LLMResponse: 包含 content 和 model_used

    Raises:
        RuntimeError: 所有模型均调用失败
    """
    models = fallback_list or MODEL_FALLBACK_LIST
    temp = temperature if temperature is not None else LLM_TEMPERATURE
    tokens = max_tokens if max_tokens is not None else LLM_MAX_TOKENS

    errors: list[tuple[str, str]] = []

    for model_name in models:
        try:
            logger.info(f"尝试调用模型: {model_name}")

            llm = ChatGroq(
                api_key=GROQ_API_KEY,
                model=model_name,
                temperature=temp,
                max_tokens=tokens,
            )

            response = llm.invoke(messages)

            logger.info(f"✓ 模型调用成功: {model_name}")
            return LLMResponse(
                content=response.content,
                model_used=model_name,
            )

        except Exception as e:
            error_msg = f"{type(e).__name__}: {str(e)[:200]}"
            errors.append((model_name, error_msg))
            logger.warning(f"✗ 模型 {model_name} 调用失败: {error_msg}")
            continue

    # 所有模型均失败
    error_details = "\n".join(f"  - {m}: {e}" for m, e in errors)
    raise RuntimeError(
        f"所有 {len(models)} 个模型均调用失败:\n{error_details}"
    )
