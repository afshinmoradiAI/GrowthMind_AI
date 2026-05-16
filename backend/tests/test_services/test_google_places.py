import httpx
import pytest

from app.services.google_places import GooglePlacesClient, GooglePlacesError


@pytest.mark.asyncio
async def test_search_text_parses_places(monkeypatch):
    payload = {
        "places": [
            {
                "id": "place-1",
                "displayName": {"text": "Harbour Realty"},
                "formattedAddress": "1 George St, Sydney NSW",
                "nationalPhoneNumber": "02 9000 0000",
                "websiteUri": "https://harbourrealty.example",
                "rating": 4.6,
                "userRatingCount": 128,
            }
        ]
    }

    def handler(request: httpx.Request) -> httpx.Response:
        assert "places:searchText" in str(request.url)
        assert request.headers["X-Goog-Api-Key"] == "fake-key"
        return httpx.Response(200, json=payload)

    transport = httpx.MockTransport(handler)

    class _PatchedAsyncClient(httpx.AsyncClient):
        def __init__(self, *args, **kwargs):
            kwargs["transport"] = transport
            super().__init__(*args, **kwargs)

    monkeypatch.setattr("app.services.google_places.httpx.AsyncClient", _PatchedAsyncClient)

    client = GooglePlacesClient(api_key="fake-key")
    leads = await client.search_text("real estate agent", "Sydney", max_results=5)

    assert len(leads) == 1
    assert leads[0].name == "Harbour Realty"
    assert leads[0].rating == 4.6
    assert leads[0].place_id == "place-1"


@pytest.mark.asyncio
async def test_search_text_raises_without_api_key():
    client = GooglePlacesClient(api_key="")
    with pytest.raises(GooglePlacesError):
        await client.search_text("cafe", "Sydney")


@pytest.mark.asyncio
async def test_search_text_raises_on_non_200(monkeypatch):
    def handler(request: httpx.Request) -> httpx.Response:
        return httpx.Response(403, text="forbidden")

    transport = httpx.MockTransport(handler)

    class _PatchedAsyncClient(httpx.AsyncClient):
        def __init__(self, *args, **kwargs):
            kwargs["transport"] = transport
            super().__init__(*args, **kwargs)

    monkeypatch.setattr("app.services.google_places.httpx.AsyncClient", _PatchedAsyncClient)

    client = GooglePlacesClient(api_key="fake-key")
    with pytest.raises(GooglePlacesError):
        await client.search_text("cafe", "Sydney")
