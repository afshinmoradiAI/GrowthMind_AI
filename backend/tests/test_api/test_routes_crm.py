import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from app.core.database import Base, get_db
from app.db import models  # noqa: F401 — register models
from app.main import app


@pytest.fixture
def client():
    engine = create_engine(
        "sqlite:///:memory:",
        future=True,
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    Base.metadata.create_all(bind=engine)
    SessionLocal = sessionmaker(engine, expire_on_commit=False)

    def _override_get_db():
        with SessionLocal() as session:
            yield session

    app.dependency_overrides[get_db] = _override_get_db
    with TestClient(app) as c:
        yield c
    app.dependency_overrides.clear()
    engine.dispose()


def _import_payload() -> dict:
    return {
        "channel": "linkedin",
        "search": {
            "business_type": "real estate agent",
            "location": "Sydney",
            "count": 1,
            "leads": [
                {
                    "lead": {
                        "name": "Harbour Realty",
                        "address": "1 George St, Sydney NSW",
                        "phone": "+61 2 9000 0000",
                        "website": "https://harbourrealty.example",
                        "rating": 4.6,
                        "review_count": 128,
                        "place_id": "place-1",
                        "decision_makers": [
                            {
                                "name": "Jane Smith",
                                "title": "Founder & CEO",
                                "email": "jane@harbourrealty.example",
                                "email_candidates": [],
                                "email_domain_verified": True,
                            }
                        ],
                    },
                    "outreach": {
                        "touches": [
                            {
                                "day_offset": 1,
                                "purpose": "Opener",
                                "subject": "Idea for Harbour Realty",
                                "body": "Hi Jane — we help agencies grow on social. Worth a chat next week?",
                            },
                            {
                                "day_offset": 4,
                                "purpose": "Follow-up",
                                "subject": "Re: Idea for Harbour Realty",
                                "body": "Bumping this. Happy to share a Sydney case study.",
                            },
                            {
                                "day_offset": 8,
                                "purpose": "Break-up",
                                "subject": "Re: Idea for Harbour Realty",
                                "body": "Last note — should I close the loop on this?",
                            },
                        ]
                    },
                    "score": {
                        "score": 84,
                        "tier": "hot",
                        "reasons": ["4.6 rating", "Named CEO"],
                    },
                }
            ],
        },
    }


def test_import_creates_lead(client):
    r = client.post("/crm/import", json=_import_payload())
    assert r.status_code == 201
    body = r.json()
    assert body["imported"] == 1
    assert body["skipped"] == 0
    assert len(body["lead_ids"]) == 1


def test_import_skips_duplicate_place_id(client):
    client.post("/crm/import", json=_import_payload())
    r = client.post("/crm/import", json=_import_payload())
    assert r.status_code == 201
    assert r.json() == {"imported": 0, "skipped": 1, "lead_ids": []}


def test_list_filter_and_get_lead(client):
    import_resp = client.post("/crm/import", json=_import_payload()).json()
    lead_id = import_resp["lead_ids"][0]

    r_all = client.get("/crm/leads")
    assert r_all.status_code == 200
    assert len(r_all.json()) == 1

    r_hot = client.get("/crm/leads", params={"tier": "hot"})
    assert len(r_hot.json()) == 1

    r_cold = client.get("/crm/leads", params={"tier": "cold"})
    assert len(r_cold.json()) == 0

    r_detail = client.get(f"/crm/leads/{lead_id}")
    assert r_detail.status_code == 200
    detail = r_detail.json()
    assert detail["name"] == "Harbour Realty"
    assert len(detail["touches"]) == 3
    assert len(detail["decision_makers"]) == 1


def test_update_status_and_notes(client):
    lead_id = client.post("/crm/import", json=_import_payload()).json()["lead_ids"][0]
    r = client.patch(
        f"/crm/leads/{lead_id}",
        json={"status": "contacted", "notes": "Sent intro email"},
    )
    assert r.status_code == 200
    body = r.json()
    assert body["status"] == "contacted"
    assert body["notes"] == "Sent intro email"


def test_mark_touch_sent(client):
    detail = client.post("/crm/import", json=_import_payload()).json()
    lead_id = detail["lead_ids"][0]
    full = client.get(f"/crm/leads/{lead_id}").json()
    touch_id = full["touches"][0]["id"]

    r = client.post(f"/crm/leads/{lead_id}/touches/{touch_id}/sent", json={})
    assert r.status_code == 200
    assert r.json()["sent_at"] is not None


def test_delete_lead(client):
    lead_id = client.post("/crm/import", json=_import_payload()).json()["lead_ids"][0]
    r = client.delete(f"/crm/leads/{lead_id}")
    assert r.status_code == 204
    assert client.get(f"/crm/leads/{lead_id}").status_code == 404


def test_get_missing_lead_returns_404(client):
    r = client.get("/crm/leads/does-not-exist")
    assert r.status_code == 404
