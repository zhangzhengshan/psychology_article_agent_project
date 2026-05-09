from __future__ import annotations

import asyncio
import json
from typing import AsyncGenerator

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse
from pydantic import BaseModel

from backend.agent import run_agent_stream

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class GenerateRequest(BaseModel):
    topic: str


def format_sse(event: str, message: str) -> str:
    """
    Standard SSE format:
    event: xxx
    data: {"message":"..."}

    """
    payload = json.dumps({"message": message}, ensure_ascii=False)
    return f"event: {event}\ndata: {payload}\n\n"


@app.get("/")
def health_check() -> dict[str, str]:
    return {"status": "ok"}


@app.post("/generate")
async def generate(request: GenerateRequest) -> StreamingResponse:
    topic = request.topic.strip()
    if not topic:
        raise HTTPException(status_code=400, detail="topic must not be empty.")

    async def event_generator() -> AsyncGenerator[str, None]:
        try:
            for item in run_agent_stream(topic):
                yield format_sse(item["event"], item["message"])
                # 让出事件循环，帮助浏览器尽快收到流式数据
                await asyncio.sleep(0)

        except Exception as error:
            yield format_sse("error", f"发生错误: {error}")

    return StreamingResponse(
        event_generator(),
        media_type="text/event-stream",
        headers={
            "Cache-Control": "no-cache",
            "Connection": "keep-alive",
            "X-Accel-Buffering": "no",
        },
    )


# =========================
# Test Code
# =========================
# 使用方法：
#
# 1. 安装依赖：
#    pip install -r requirements.txt
#
# 2. 配置环境变量：
#    Windows PowerShell:
#    $env:DEEPSEEK_API_KEY="你的key"
#    $env:DEEPSEEK_BASE_URL="https://api.deepseek.com/v1"
#    $env:DEEPSEEK_MODEL="deepseek-chat"
#
# 3. 启动后端：
#    uvicorn backend.main:app --reload
#
# 4. 测试接口：
#    POST http://127.0.0.1:8000/generate
#    JSON:
#    {"topic":"拖延症的心理学解释"}
#
# 5. 返回内容会按 SSE 逐步推送。
# =========================
if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        "backend.main:app",
        host="127.0.0.1",
        port=8000,
        reload=True,
    )