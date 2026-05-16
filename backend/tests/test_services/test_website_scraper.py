import httpx
import pytest

from app.services.website_scraper import WebsiteScraper

HOME_HTML = """
<html><head><title>Harbour Realty</title></head>
<body>
  <nav>
    <a href="/about">About Us</a>
    <a href="/team">Our Team</a>
    <a href="/listings">Listings</a>
    <a href="https://other.example/foo">External</a>
  </nav>
  <h1>Welcome</h1>
  <p>We are a Sydney real estate agency.</p>
  <script>var x = 1;</script>
</body></html>
"""

ABOUT_HTML = """
<html><body>
  <h1>About</h1>
  <p>Jane Smith, Founder & CEO. Email: jane@harbourrealty.example</p>
</body></html>
"""

TEAM_HTML = """
<html><body>
  <h1>Team</h1>
  <p>Tom Lee, Head of Sales.</p>
</body></html>
"""


def _make_transport():
    def handler(request: httpx.Request) -> httpx.Response:
        path = request.url.path
        if path in ("", "/"):
            return httpx.Response(200, html=HOME_HTML)
        if path == "/about":
            return httpx.Response(200, html=ABOUT_HTML)
        if path == "/team":
            return httpx.Response(200, html=TEAM_HTML)
        return httpx.Response(404)

    return httpx.MockTransport(handler)


@pytest.mark.asyncio
async def test_scrape_combines_pages(monkeypatch):
    transport = _make_transport()

    class _Patched(httpx.AsyncClient):
        def __init__(self, *args, **kwargs):
            kwargs["transport"] = transport
            super().__init__(*args, **kwargs)

    monkeypatch.setattr("app.services.website_scraper.httpx.AsyncClient", _Patched)

    scraper = WebsiteScraper()
    text = await scraper.scrape("https://harbourrealty.example")

    assert "Jane Smith" in text
    assert "Tom Lee" in text
    assert "var x = 1" not in text


@pytest.mark.asyncio
async def test_scrape_returns_empty_for_blank_url():
    scraper = WebsiteScraper()
    assert await scraper.scrape("") == ""


@pytest.mark.asyncio
async def test_scrape_handles_non_200(monkeypatch):
    def handler(request: httpx.Request) -> httpx.Response:
        return httpx.Response(500)

    transport = httpx.MockTransport(handler)

    class _Patched(httpx.AsyncClient):
        def __init__(self, *args, **kwargs):
            kwargs["transport"] = transport
            super().__init__(*args, **kwargs)

    monkeypatch.setattr("app.services.website_scraper.httpx.AsyncClient", _Patched)

    scraper = WebsiteScraper()
    text = await scraper.scrape("https://broken.example")
    assert text == ""
