from unittest.mock import AsyncMock

import pytest
from fastapi.testclient import TestClient

from app.api.routes_leads import get_icp_agent, get_orchestrator
from app.main import app
from app.schemas.content import Platform
from app.schemas.leads import (
    ICPParsed,
    Lead,
    LeadScore,
    LeadSearchResponse,
    LeadWithOutreach,
    OutreachSequence,
    Touch,
)


@pytest.fixture
def client():
    fake = AsyncMock()
    fake.run = AsyncMock(
        return_value=LeadSearchResponse(
            business_type="real estate agent",
            location="Sydney",
            count=1,
            leads=[
                LeadWithOutreach(
                    lead=Lead(
                        name="Harbour Realty",
                        address="1 George St, Sydney NSW",
                        phone="+61 2 9000 0000",
                        website="https://harbourrealty.example",
                        rating=4.6,
                        review_count=128,
                        place_id="xyz789",
                    ),
                    outreach=OutreachSequence(
                        touches=[
                            Touch(
                                day_offset=1,
                                purpose="Opener",
                                subject="Idea for Harbour Realty",
                                body=(
                                    "Hi team — we help Sydney agencies turn "
                                    "listings into multi-platform social "
                                    "campaigns. Worth a chat next week?"
                                ),
                            ),
                            Touch(
                                day_offset=4,
                                purpose="Follow-up",
                                subject="Re: Idea for Harbour Realty",
                                body=(
                                    "Bumping this. Happy to share a quick "
                                    "Sydney agency case study if useful."
                                ),
                            ),
                            Touch(
                                day_offset=8,
                                purpose="Break-up",
                                subject="Re: Idea for Harbour Realty",
                                body=(
                                    "Last note — if this isn't a priority "
                                    "right now, should I close the loop?"
                                ),
                            ),
                        ]
                    ),
                    score=LeadScore(
                        score=84,
                        tier="hot",
                        reasons=["4.6 rating with 128 reviews", "Has website"],
                    ),
                )
            ],
        )
    )
    fake_icp = AsyncMock()
    fake_icp.run = AsyncMock(
        return_value=ICPParsed(
            business_type="real estate agent",
            location="Sydney",
            topic="property investment",
            outreach_platform=Platform.linkedin,
            rationale="Parsed from user query.",
        )
    )
    app.dependency_overrides[get_orchestrator] = lambda: fake
    app.dependency_overrides[get_icp_agent] = lambda: fake_icp

    # /leads is now auth-gated — bypass auth in tests by overriding the dependency.
    from app.core.dependencies import get_current_user_with_cookie
    from app.db.models import User as UserModel

    fake_user = UserModel(
        id="test-user", email="t@example.com", hashed_password="x"
    )
    app.dependency_overrides[get_current_user_with_cookie] = lambda: fake_user

    with TestClient(app) as c:
        yield c
    app.dependency_overrides.clear()


def test_search_leads(client):
    r = client.post(
        "/leads/search",
        json={
            "business_type": "real estate agent",
            "location": "Sydney",
            "max_results": 5,
            "outreach_platform": "linkedin",
        },
    )
    assert r.status_code == 200
    body = r.json()
    assert body["count"] == 1
    lead = body["leads"][0]
    assert lead["lead"]["name"] == "Harbour Realty"
    assert len(lead["outreach"]["touches"]) == 3
    assert lead["outreach"]["touches"][0]["day_offset"] == 1
    assert lead["score"]["tier"] == "hot"


def test_search_leads_validation_error(client):
    r = client.post(
        "/leads/search",
        json={"business_type": "x", "location": ""},
    )
    assert r.status_code == 422


def test_parse_icp(client):
    r = client.post(
        "/leads/icp/parse",
        json={
            "query": "Find real estate agents in Sydney for a property investment campaign"
        },
    )
    assert r.status_code == 200
    body = r.json()
    assert body["business_type"] == "real estate agent"
    assert body["location"] == "Sydney"
    assert body["outreach_platform"] == "linkedin"


def test_search_from_icp(client):
    r = client.post(
        "/leads/icp/search",
        json={
            "query": "Find real estate agents in Sydney for a property investment campaign",
            "max_results": 5,
        },
    )
    assert r.status_code == 200
    body = r.json()
    assert body["count"] == 1
    assert body["leads"][0]["lead"]["name"] == "Harbour Realty"
