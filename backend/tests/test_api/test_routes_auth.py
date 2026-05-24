import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from app.core.database import Base, get_db
from app.db import models  # noqa: F401
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


def test_register_creates_user_and_sets_cookie(client):
    r = client.post(
        "/auth/register",
        json={
            "email": "alice@example.com",
            "password": "supersecret",
            "display_name": "Alice",
        },
    )
    assert r.status_code == 201
    body = r.json()
    assert body["user"]["email"] == "alice@example.com"
    assert body["user"]["display_name"] == "Alice"
    assert "growthmind_session" in r.cookies


def test_register_rejects_duplicate_email(client):
    payload = {"email": "alice@example.com", "password": "supersecret"}
    client.post("/auth/register", json=payload)
    r = client.post("/auth/register", json=payload)
    assert r.status_code == 409


def test_register_rejects_short_password(client):
    r = client.post(
        "/auth/register",
        json={"email": "alice@example.com", "password": "short"},
    )
    assert r.status_code == 422


def test_login_success(client):
    client.post(
        "/auth/register",
        json={"email": "alice@example.com", "password": "supersecret"},
    )
    client.cookies.clear()
    r = client.post(
        "/auth/login",
        json={"email": "alice@example.com", "password": "supersecret"},
    )
    assert r.status_code == 200
    assert "growthmind_session" in r.cookies


def test_login_bad_password(client):
    client.post(
        "/auth/register",
        json={"email": "alice@example.com", "password": "supersecret"},
    )
    r = client.post(
        "/auth/login",
        json={"email": "alice@example.com", "password": "wrong-password"},
    )
    assert r.status_code == 401


def test_me_returns_current_user(client):
    client.post(
        "/auth/register",
        json={"email": "alice@example.com", "password": "supersecret"},
    )
    r = client.get("/auth/me")
    assert r.status_code == 200
    assert r.json()["email"] == "alice@example.com"


def test_me_without_cookie_returns_401(client):
    r = client.get("/auth/me")
    assert r.status_code == 401


def test_logout_clears_cookie(client):
    client.post(
        "/auth/register",
        json={"email": "alice@example.com", "password": "supersecret"},
    )
    r = client.post("/auth/logout")
    assert r.status_code == 204
    # subsequent /me should fail
    client.cookies.clear()
    assert client.get("/auth/me").status_code == 401
