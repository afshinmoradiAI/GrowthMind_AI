from types import SimpleNamespace
from unittest.mock import AsyncMock

import pytest

from app.agents import ICPBuilderAgent
from app.schemas.content import Platform
from app.schemas.leads import ICPQuery


def _fake_response(payload: dict) -> SimpleNamespace:
    tool_block = SimpleNamespace(type="tool_use", input=payload)
    usage = SimpleNamespace(input_tokens=15, output_tokens=10)
    return SimpleNamespace(content=[tool_block], usage=usage)


@pytest.mark.asyncio
async def test_icp_builder_parses_full_query():
    payload = {
        "business_type": "dental clinic",
        "location": "Melbourne",
        "topic": "cosmetic dentistry",
        "outreach_platform": "linkedin",
        "rationale": "User explicitly named dental clinics in Melbourne, cosmetic dentistry topic, LinkedIn channel.",
    }
    client = SimpleNamespace(
        messages=SimpleNamespace(
            create=AsyncMock(return_value=_fake_response(payload))
        )
    )
    agent = ICPBuilderAgent(client=client)  # type: ignore[arg-type]
    result = await agent.run(
        ICPQuery(
            query="Find me dental clinics in Melbourne to pitch cosmetic dentistry services on LinkedIn",
            max_results=10,
        )
    )
    assert result.business_type == "dental clinic"
    assert result.location == "Melbourne"
    assert result.topic == "cosmetic dentistry"
    assert result.outreach_platform == Platform.linkedin


@pytest.mark.asyncio
async def test_icp_builder_defaults_to_linkedin_when_unspecified():
    payload = {
        "business_type": "cafe",
        "location": "Sydney",
        "topic": None,
        "outreach_platform": "linkedin",
        "rationale": "User did not specify a channel — defaulted to LinkedIn.",
    }
    client = SimpleNamespace(
        messages=SimpleNamespace(
            create=AsyncMock(return_value=_fake_response(payload))
        )
    )
    agent = ICPBuilderAgent(client=client)  # type: ignore[arg-type]
    result = await agent.run(ICPQuery(query="Find cafes in Sydney"))
    assert result.outreach_platform == Platform.linkedin
    assert result.topic is None
