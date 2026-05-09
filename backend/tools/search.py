from __future__ import annotations

import json
from typing import Any

from langchain_community.utilities import DuckDuckGoSearchAPIWrapper

from backend.config import max_results, region, safe_search
from backend.llm import llm


def _normalize_search_output(result: Any) -> str:
    """
    Normalize DuckDuckGo search output into a clean string.
    """
    if isinstance(result, str):
        return result.strip()

    return json.dumps(result, ensure_ascii=False, indent=2)


def search_tool(topic: str) -> str:
    """
    Step 1:
    1) Use LLM to rewrite the user's topic into a better search query.
    2) Use DuckDuckGoSearchResults to search the web.
    """

    cleaned_topic = topic.strip()
    if not cleaned_topic:
        raise ValueError("topic must not be empty.")

    rewrite_prompt = f"""
你是一个中文心理学科普文章检索助手。

用户的问题：
{cleaned_topic}

请你根据用户问题设计的题材，抽取出题词并重写成更适合DuckDuckGoSearchResults检索的英文关键词。

要求：
1. 返回一行关键词
2. 不要解释
3. 尽量具体，方便检索
"""

    rewritten_query = llm(rewrite_prompt).strip()
    if not rewritten_query:
        rewritten_query = cleaned_topic

    wrapper = DuckDuckGoSearchAPIWrapper(
        max_results=max_results,
        region=region,
        safesearch=safe_search,
    )

    raw_results = wrapper.results(rewritten_query,max_results)

    # 这里的 raw_results 已经是列表了，直接过滤即可
    filtered_result = [{"title": item["title"], "snippet": item["snippet"]} for item in raw_results]
    return json.dumps(filtered_result, ensure_ascii=False, indent=2)
