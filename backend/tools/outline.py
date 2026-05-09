from __future__ import annotations

from backend.llm import llm

def outline_tool(topic: str, search_results: str) -> str:
    """
    Step 2:
    Generate a structured outline based on search results.
    """

    cleaned_topic = topic.strip()
    cleaned_search_results = search_results.strip()

    if not cleaned_topic:
        raise ValueError("topic must not be empty.")
    if not cleaned_search_results:
        raise ValueError("search_results must not be empty.")

    prompt = f"""
你是一个知乎心理学科普文章作者。

用户的问题：
{cleaned_topic}

搜索资料：
{cleaned_search_results}

请生成一篇知乎风格的心理学科普文章大纲。

要求：
1. 逻辑清晰
2. 适合普通人阅读
3. 使用中文
4. 分章节
5. 不要写正文
6.内容简洁
"""

    return llm(prompt)

