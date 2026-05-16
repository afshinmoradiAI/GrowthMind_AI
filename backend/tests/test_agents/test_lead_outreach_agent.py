from types import SimpleNamespace
from unittest.mock import AsyncMock

import pytest

from app.agents import LeadOutreachAgent
from app.schemas.content import Platform
from app.schemas.leads import Lead, OutreachInput


def _fake_response(payload: dict) -> SimpleNamespace:
    tool_block = SimpleNamespace(type="tool_use", input=payload)
    usage = SimpleNamespace(input_tokens=12, output_tokens=34)
    return SimpleNamespace(content=[tool_block], usage=usage)


@pytest.mark.asyncio
async def test_lead_outreach_agent_returns_three_touch_sequence():
    fake_payload = {
        "touches": [
            {
                "day_offset": 1,
                "purpose": "Opener — relevance hook",
                "subject": "Idea for Surry Hills Coffee",
                "body": (
                    "Hi team — noticed you run a cafe in Surry Hills. We help "
                    "venues like yours grow weekday foot traffic with targeted "
                    "local social campaigns. Worth a quick 15-min chat next "
                    "week?"
                ),
            },
            {
                "day_offset": 4,
                "purpose": "Follow-up — new angle",
                "subject": "Re: Idea for Surry Hills Coffee",
                "body": (
                    "Bumping this up. Curious — what does your weekday lunch "
                    "rush look like compared to weekends? Happy to share a "
                    "Sydney cafe case study if useful."
                ),
            },
            {
                "day_offset": 8,
                "purpose": "Break-up — permission close",
                "subject": "Re: Idea for Surry Hills Coffee",
                "body": (
                    "Last note from me — if growing weekday traffic isn't a "
                    "priority right now, no problem. Should I close the loop?"
                ),
            },
        ]
    }
    client = SimpleNamespace(
        messages=SimpleNamespace(
            create=AsyncMock(return_value=_fake_response(fake_payload))
        )
    )
    agent = LeadOutreachAgent(client=client)  # type: ignore[arg-type]

    result = await agent.run(
        OutreachInput(
            lead=Lead(
                name="Surry Hills Coffee",
                address="123 Crown St, Surry Hills NSW",
                rating=4.7,
                review_count=312,
                place_id="abc123",
            ),
            business_type="cafe",
            topic="local foot traffic",
            outreach_platform=Platform.linkedin,
        )
    )

    assert len(result.touches) == 3
    assert [t.day_offset for t in result.touches] == [1, 4, 8]
    assert result.touches[0].subject == "Idea for Surry Hills Coffee"
    assert "Re:" in result.touches[1].subject
    client.messages.create.assert_awaited_once()
