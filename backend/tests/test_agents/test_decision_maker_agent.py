from types import SimpleNamespace
from unittest.mock import AsyncMock

import pytest

from app.agents import DecisionMakerAgent
from app.schemas.leads import DecisionMakerExtractionInput


def _fake_response(payload: dict) -> SimpleNamespace:
    tool_block = SimpleNamespace(type="tool_use", input=payload)
    usage = SimpleNamespace(input_tokens=20, output_tokens=15)
    return SimpleNamespace(content=[tool_block], usage=usage)


@pytest.mark.asyncio
async def test_decision_maker_agent_returns_people():
    fake_payload = {
        "decision_makers": [
            {
                "name": "Jane Smith",
                "title": "Founder & CEO",
                "email": "jane@harbourrealty.example",
            },
            {"name": "Tom Lee", "title": "Head of Sales", "email": None},
        ]
    }
    client = SimpleNamespace(
        messages=SimpleNamespace(
            create=AsyncMock(return_value=_fake_response(fake_payload))
        )
    )
    agent = DecisionMakerAgent(client=client)  # type: ignore[arg-type]

    result = await agent.run(
        DecisionMakerExtractionInput(
            business_name="Harbour Realty",
            website_url="https://harbourrealty.example",
            page_text="Our founder Jane Smith leads the team alongside Tom Lee, Head of Sales.",
        )
    )

    assert len(result.decision_makers) == 2
    assert result.decision_makers[0].name == "Jane Smith"
    assert result.decision_makers[0].title == "Founder & CEO"


@pytest.mark.asyncio
async def test_decision_maker_agent_handles_empty_list():
    client = SimpleNamespace(
        messages=SimpleNamespace(
            create=AsyncMock(return_value=_fake_response({"decision_makers": []}))
        )
    )
    agent = DecisionMakerAgent(client=client)  # type: ignore[arg-type]
    result = await agent.run(
        DecisionMakerExtractionInput(
            business_name="Quiet Co",
            website_url="https://quiet.example",
            page_text="We are a small team. Contact us.",
        )
    )
    assert result.decision_makers == []
