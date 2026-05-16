from unittest.mock import AsyncMock

import dns.exception
import pytest

from app.services.email_finder import EmailFinder


def test_extract_domain_strips_www_and_protocol():
    finder = EmailFinder()
    assert finder.extract_domain("https://www.harbourrealty.example/about") == "harbourrealty.example"
    assert finder.extract_domain("harbourrealty.example") == "harbourrealty.example"


def test_extract_domain_rejects_generic_providers():
    finder = EmailFinder()
    assert finder.extract_domain("https://gmail.com") is None
    assert finder.extract_domain("") is None
    assert finder.extract_domain(None) is None


def test_generate_candidates_full_name():
    finder = EmailFinder()
    candidates = finder.generate_candidates("Jane Smith", "harbour.example")
    assert "jane@harbour.example" in candidates
    assert "jane.smith@harbour.example" in candidates
    assert "jsmith@harbour.example" in candidates
    assert len(candidates) == len(set(candidates))


def test_generate_candidates_single_name():
    finder = EmailFinder()
    candidates = finder.generate_candidates("Madonna", "harbour.example")
    assert candidates == ["madonna@harbour.example"]


def test_generate_candidates_strips_non_alpha():
    finder = EmailFinder()
    candidates = finder.generate_candidates("Jean-Luc D'Angelo", "ship.example")
    assert all("@ship.example" in c for c in candidates)
    assert all(c.split("@")[0].replace("-", "").replace(".", "").replace("_", "").isalpha() for c in candidates)


def test_generate_candidates_empty_inputs():
    finder = EmailFinder()
    assert finder.generate_candidates("", "x.example") == []
    assert finder.generate_candidates("Jane", "") == []


@pytest.mark.asyncio
async def test_verify_domain_true_when_mx_records_exist():
    finder = EmailFinder()
    finder._resolver.resolve = AsyncMock(return_value=[object()])  # type: ignore[method-assign]
    assert await finder.verify_domain("harbour.example") is True


@pytest.mark.asyncio
async def test_verify_domain_false_on_dns_failure():
    finder = EmailFinder()
    finder._resolver.resolve = AsyncMock(  # type: ignore[method-assign]
        side_effect=dns.exception.DNSException("no records")
    )
    assert await finder.verify_domain("no-such-domain.example") is False
