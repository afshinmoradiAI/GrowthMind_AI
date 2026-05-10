from unittest.mock import AsyncMock

import pytest
from fastapi.testclient import TestClient

from app.api.routes_content import get_orchestrator
from app.main import app
from app.schemas.content import ContentResponse, Platform, PlatformPost


@pytest.fixture
def client():
    fake = AsyncMock()
    fake.run = AsyncMock(
        return_value=ContentResponse(
            topic="AI productivity",
            posts=[
                PlatformPost(
                    platform=Platform.x,
                    content="Hook about AI.",
                    hashtags=["AI"],
                    image_prompt="A glowing brain, editorial photograph",
                    image_negative_prompt="text, watermark",
                    image_aspect_ratio="16:9",
                )
            ],
        )
    )
    app.dependency_overrides[get_orchestrator] = lambda: fake
    with TestClient(app) as c:
        yield c
    app.dependency_overrides.clear()


def test_health(client):
    r = client.get("/health")
    assert r.status_code == 200
    assert r.json() == {"status": "ok"}


def test_generate_content(client):
    r = client.post(
        "/content/generate",
        json={
            "topic": "AI productivity",
            "platforms": ["x"],
            "tone": "professional",
        },
    )
    assert r.status_code == 200
    body = r.json()
    assert body["topic"] == "AI productivity"
    assert len(body["posts"]) == 1
    assert body["posts"][0]["platform"] == "x"
    assert body["posts"][0]["image_aspect_ratio"] == "16:9"


def test_generate_content_validation_error(client):
    r = client.post(
        "/content/generate",
        json={"topic": "x", "platforms": []},
    )
    assert r.status_code == 422
