import json
import os
import re

from fastapi import FastAPI, HTTPException
from openai import AsyncOpenAI
from pydantic import BaseModel, Field


app = FastAPI(
    title="Todo List AI API",
    description="A FastAPI web service scaffold.",
    version="0.1.0",
)


class InitFromLlmRequest(BaseModel):
    content: str = Field(..., min_length=1)


SYSTEM_PROMPT = (
    "你是一个任务整理助手。"
    "请从用户输入中整理出所有待办任务。"
    "只返回严格合法的 JSON 字符串数组，不要返回任何 JSON 外的内容。"
    '示例：["打扫卫生", "写作业"]。'
    "如果没有整理出任何待办任务，返回空数组 []。"
)


def remove_think_tags(text: str) -> str:
    return re.sub(r"<think>.*?</think>", "", text, flags=re.DOTALL | re.IGNORECASE).strip()


def parse_string_array(text: str) -> list[str]:
    cleaned_text = remove_think_tags(text)

    try:
        raw_items = json.loads(cleaned_text)
    except json.JSONDecodeError as exc:
        raise HTTPException(
            status_code=502,
            detail="OpenAI response was not valid JSON",
        ) from exc

    if not isinstance(raw_items, list) or not all(isinstance(item, str) for item in raw_items):
        raise HTTPException(
            status_code=502,
            detail="OpenAI response was not a valid string array",
        )

    return raw_items


@app.get("/")
def read_root() -> dict[str, str]:
    return {"message": "FastAPI service is running"}


@app.get("/health")
def health_check() -> dict[str, str]:
    return {"status": "ok"}


@app.post("/init_from_llm")
async def init_from_llm(payload: InitFromLlmRequest) -> list[str]:
    api_key = os.getenv("OPENAI_API_KEY")
    base_url = os.getenv("OPENAI_BASE_URL")
    model = os.getenv("OPENAI_MODEL")

    if not api_key or not base_url or not model:
        raise HTTPException(
            status_code=500,
            detail="OPENAI_API_KEY, OPENAI_BASE_URL, and OPENAI_MODEL must be configured",
        )

    client = AsyncOpenAI(api_key=api_key, base_url=base_url, timeout=30.0)

    try:
        completion = await client.chat.completions.create(
            model=model,
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": payload.content},
            ],
        )
    except Exception as exc:
        raise HTTPException(status_code=502, detail=f"OpenAI request failed: {exc}") from exc

    message = completion.choices[0].message.content
    if not message:
        raise HTTPException(status_code=502, detail="OpenAI returned an empty response")

    return parse_string_array(message)
