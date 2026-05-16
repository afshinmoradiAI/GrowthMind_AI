from types import SimpleNamespace
from unittest.mock import AsyncMock

import pytest

from app.agents import LeadScoringAgent
from app.schemas.leads import DecisionMaker, Lead, LeadScoringInput


def _fake_response(payload: dict) -> SimpleNamespace:
    tool_block = SimpleNamespace(type="tool_use", input=payload)
    usage = SimpleNamespace(input_tokens=30, output_tokens=20)
    return SimpleNamespace(content=[tool_block], usage=usage)


@pytest.mark.asyncio
async def test_scoring_agent_returns_hot_lead():
    payload = {
        "score": 88,
        "tier": "hot",
        "reasons": [
            "4.8 rating with 220 reviews",
            "Named CEO with verified email domain",
            "Website matches Sydney real estate niche",
        ],
    }
    client = SimpleNamespace(
        messages=SimpleNamespace(
            create=AsyncMock(return_value=_fake_response(payload))
        )
    )
    agent = LeadScoringAgent(client=client)  # type: ignore[arg-type]

    result = await agent.run(
        LeadScoringInput(
            lead=Lead(
                name="Harbour Realty",
                address="1 George St, Sydney NSW",
                phone="+61 2 9000 0000",
                website="https://harbourrealty.example",
                rating=4.8,
                review_count=220,
                place_id="abc",
                decision_makers=[
                    DecisionMaker(
                        name="Jane Smith",
                        title="Founder & CEO",
                        email="jane@harbourrealty.example",
                        email_domain_verified=True,
                    )
                ],
            ),
            business_type="real estate agent",
            location="Sydney",
            topic="property investment",
        )
    )

    assert result.score == 88
    assert result.tier == "hot"
    assert len(result.reasons) == 3


@pytest.mark.asyncio
async def test_scoring_agent_rejects_invalid_tier():
    bad_payload = {"score": 50, "tier": "lukewarm", "reasons": []}
    client = SimpleNamespace(
        messages=SimpleNamespace(
            create=AsyncMock(return_value=_fake_response(bad_payload))
        )
    )
    agent = LeadScoringAgent(client=client)  # type: ignore[arg-type]

    with pytest.raises(Exception):
        await agent.run(
            LeadScoringInput(
                lead=Lead(name="X", place_id="x"),
                business_type="cafe",
                location="Sydney",
            )
        )
