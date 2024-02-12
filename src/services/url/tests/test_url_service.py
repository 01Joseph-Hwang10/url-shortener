import pytest
from src import models, dtos
from src.services.url import URLService
from src.repositories.url import MockURLRepository
from src.config import get_settings


@pytest.fixture()
def service():
    repository = MockURLRepository(
        db=[
            models.URL(
                target_url="https://www.abc.com",
                key="abc",
            ),
        ],
    )
    return URLService(urls=repository)


def test_create_url(service: URLService):
    # Arrange
    request = dtos.CreateURLInput(
        target_url="https://www.example.com",
    )

    # Act
    result = service.create_url(request)
    shortened_url = result.shortened_url

    # Assert
    assert shortened_url.startswith(get_settings().base_url)
    assert (
        len(shortened_url.replace(get_settings().base_url, "").replace("/", ""))
        == service.url_key_length
    )


def test_get_url_by_key(service: URLService):
    # Arrange
    url_key = "abc"

    # Act
    result = service.get_url_by_key(url_key)

    # Assert
    assert result.target_url == "https://www.abc.com"
