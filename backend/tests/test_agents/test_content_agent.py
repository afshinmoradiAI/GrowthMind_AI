from types import SimpleNamespace
from unittest.mock import AsyncMock

import pytest

from app.agents import ContentAgent
from app.schemas.content import ContentRequest, Platform, Tone


def _fake_response(payload: dict) -> SimpleNamespace:
    tool_block = SimpleNamespace(type="tool_use", input=payload)
    usage = SimpleNamespace(input_tokens=10, output_tokens=20)
    return SimpleNamespace(content=[tool_block], usage=usage)


@pytest.mark.asyncio
async def test_content_agent_returns_one_post_per_platform():
    fake_payload = {
        "posts": [
            {
                "platform": "x",
                "content": "Short hook about AI productivity.",
                "hashtags": ["AI", "Productivity"],
            },
            {
                "platform": "linkedin",
                "content": "A longer professional post about AI.",
                "hashtags": ["AI", "Leadership", "Future"],
            },
        ]
    }
    client = SimpleNamespace(
        messages=SimpleNamespace(create=AsyncMock(return_value=_fake_response(fake_payload)))
    )
    agent = ContentAgent(client=client)  # type: ignore[arg-type]

    result = await agent.run(
        ContentRequest(
            topic="AI for productivity",
            platforms=[Platform.x, Platform.linkedin],
            tone=Tone.professional,
        )
    )

    assert len(result.posts) == 2
    assert {p.platform for p in result.posts} == {Platform.x, Platform.linkedin}
    client.messages.create.assert_awaited_once()
