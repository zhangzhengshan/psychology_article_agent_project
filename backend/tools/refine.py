from __future__ import annotations

from typing import Generator

from backend.llm import llm_stream


def refine_tool_stream(draft: str) -> Generator[str, None, None]:
    """
    True streaming refine tool.
    """

    cleaned_draft = draft.strip()

    if not cleaned_draft:
        raise ValueError("draft must not be empty.")

    prompt = f"""
请优化下面这篇知乎心理学科普文章。

优化要求：
1. 增强逻辑流畅性
2. 增强阅读吸引力
3. 增强开头和结尾质量
4. 优化段落衔接
5. 不要改变核心内容
6. 保持中文知乎风格

文章内容：
{cleaned_draft}
"""

    for chunk in llm_stream(prompt):
        yield chunk

