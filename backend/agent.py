from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, Generator, Iterator

from backend.tools.draft import draft_tool
from backend.tools.outline import outline_tool
from backend.tools.refine import refine_tool_stream
from backend.tools.search import search_tool


@dataclass
class AgentState:
    """
    Store all intermediate states in the fixed workflow.
    """

    topic: str
    search_results: str = ""
    outline: str = ""
    draft: str = ""
    final_article: str = ""


def _chunk_text(text: str, chunk_size: int = 80) -> Iterator[str]:
    """
    Split long text into smaller chunks for streaming.
    """
    cleaned_text = text.strip()
    if not cleaned_text:
        return

    for index in range(0, len(cleaned_text), chunk_size):
        yield cleaned_text[index : index + chunk_size]


def run_agent_stream(topic: str) -> Generator[Dict[str, str], None, None]:
    """
    Fixed workflow:
    search -> outline -> draft -> refine
    Then stream the final article in chunks.
    """

    cleaned_topic = topic.strip()
    if not cleaned_topic:
        raise ValueError("topic must not be empty.")

    state = AgentState(topic=cleaned_topic)

    yield {"event": "status", "message": "正在搜索资料..."}
    state.search_results = search_tool(state.topic)
    yield {"event": "status", "message": "搜索完成。"}

    yield {"event": "status", "message": "正在生成文章大纲..."}
    state.outline = outline_tool(
        topic=state.topic,
        search_results=state.search_results,
    )
    yield {"event": "status", "message": "大纲生成完成。"}

    yield {"event": "status", "message": "正在生成文章初稿..."}
    state.draft = draft_tool(
        topic=state.topic,
        outline=state.outline,
    )
    yield {"event": "status", "message": "初稿生成完成。"}

    yield {"event": "status", "message": "正在润色文章..."}

    article_chunks = []

    for chunk in refine_tool_stream(state.draft):
        article_chunks.append(chunk)

        yield {
            "event": "article",
            "message": chunk,
        }

    state.final_article = "".join(article_chunks)

    yield {"event": "status", "message": "文章润色完成。"}

    yield {"event": "done", "message": "全部流程执行完成"}


# =========================
# Test Code
# =========================
# 使用方法：
#
# 1. 先配置环境变量：
#    Windows PowerShell:
#    $env:DEEPSEEK_API_KEY="你的key"
#    $env:DEEPSEEK_BASE_URL="https://api.deepseek.com/v1"
#    $env:DEEPSEEK_MODEL="deepseek-chat"
#
# 2. 在项目根目录执行：
#    python -m backend.agent
#
# 3. 你会看到状态流和最终文章分块输出。
# =========================
if __name__ == "__main__":
    test_topic = "为什么人会拖延"

    for event in run_agent_stream(test_topic):
        print(event)