from types import SimpleNamespace
from unittest.mock import AsyncMock

import pytest

from app.agents import ImagePromptAgent
from app.schemas.content import ImagePromptInput, Platform


def _fake_response(payload: dict) -> SimpleNamespace:
    tool_block = SimpleNamespace(type="tool_use", input=payload)
    usage = SimpleNamespace(input_tokens=5, output_tokens=15)
    return SimpleNamespace(content=[tool_block], usage=usage)


@pytest.mark.asyncio
async def test_image_prompt_agent_returns_structured_output():
    fake_payload = {
        "prompt": "A focused engineer at a sunlit desk, editorial photograph, 35mm",
        "negative_prompt": "text, watermark, blurry",
        "aspect_ratio": "1:1",
    }
    client = SimpleNamespace(
        messages=SimpleNamespace(create=AsyncMock(return_value=_fake_response(fake_payload)))
    )
    agent = ImagePromptAgent(client=client)  # type: ignore[arg-type]

    result = await agent.run(
        ImagePromptInput(
            platform=Platform.instagram,
            post_content="AI helps engineers ship faster.",
            topic="AI for productivity",
        )
    )

    assert result.aspect_ratio == "1:1"
    assert "editorial" in result.prompt
    assert result.negative_prompt is not None
