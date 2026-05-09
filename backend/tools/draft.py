from __future__ import annotations

from backend.llm import llm


def draft_tool(topic: str, outline: str) -> str:
    """
    Step 3:
    Generate the first draft based on the outline.
    """

    cleaned_topic = topic.strip()
    cleaned_outline = outline.strip()

    if not cleaned_topic:
        raise ValueError("topic must not be empty.")
    if not cleaned_outline:
        raise ValueError("outline must not be empty.")

    prompt = f"""
你是一个知乎心理学科普专栏作者。

用户的问题：
{cleaned_topic}

文章大纲：
{cleaned_outline}

请根据大纲生成完整文章。

要求：
1. 中文输出
2. 通俗易懂
3. 有案例感
4. 有逻辑递进
5. 不要过于学术化
6. 符合知乎科普文章风格
"""

    return llm(prompt)

