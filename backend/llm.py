from __future__ import annotations

import json
from typing import Generator

import requests

from backend.config import (
    DEEPSEEK_API_KEY,
    DEEPSEEK_BASE_URL,
    DEEPSEEK_MODEL,
)


class LLMError(Exception):
    """
    Custom exception for LLM related errors.
    """


def llm(prompt: str) -> str:
    """
    Non-streaming LLM call.
    """

    chunks = []

    for chunk in llm_stream(prompt):
        chunks.append(chunk)

    return "".join(chunks)


def llm_stream(prompt: str) -> Generator[str, None, None]:
    """
    True streaming DeepSeek response.
    """

    if not DEEPSEEK_API_KEY:
        raise LLMError("DEEPSEEK_API_KEY is not configured.")

    if not DEEPSEEK_BASE_URL:
        raise LLMError("DEEPSEEK_BASE_URL is not configured.")

    url = f"{DEEPSEEK_BASE_URL.rstrip('/')}/chat/completions"

    headers = {
        "Authorization": f"Bearer {DEEPSEEK_API_KEY}",
        "Content-Type": "application/json",
    }

    payload = {
        "model": DEEPSEEK_MODEL,
        "messages": [
            {
                "role": "user",
                "content": prompt,
            }
        ],
        "temperature": 0.7,
        "stream": True,
    }

    try:

        response = requests.post(
            url=url,
            headers=headers,
            json=payload,
            stream=True,
            timeout=300,
        )

        response.raise_for_status()

    except requests.RequestException as error:
        raise LLMError(f"DeepSeek request failed: {error}") from error

    for line in response.iter_lines():

        if not line:
            continue

        decoded_line = line.decode("utf-8")

        if not decoded_line.startswith("data: "):
            continue

        data_str = decoded_line.removeprefix("data: ").strip()

        if data_str == "[DONE]":
            break

        try:
            data_json = json.loads(data_str)

            delta = (
                data_json["choices"][0]
                .get("delta", {})
                .get("content", "")
            )

            if delta:
                yield delta

        except (
            json.JSONDecodeError,
            KeyError,
            IndexError,
        ):
            continue