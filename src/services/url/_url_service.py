import validators
from urllib.parse import urljoin
from fastapi import HTTPException
from shortuuid import ShortUUID
from src import models, dtos
from src.config import get_settings
from src.repositories.url import URLRepository


class URLService:

    def __init__(
        self,
        urls: URLRepository,
        url_key_length: int = 10,
    ) -> None:
        self.urls = urls
        self.url_key_length = url_key_length

    def _create_unique_random_key(
        self,
        length: int,
    ) -> str:
        return ShortUUID().random(length=length)

    def create_url(self, request: dtos.CreateURLInput) -> dtos.CreateURLOutput:
        # Validate if the provided URL is valid
        if not validators.url(request.target_url):
            raise HTTPException(
                status_code=400,
                message="Your provided URL is not valid",
            )

        # Create a new URL in the database
        url = self.urls.create(
            url=request.target_url,
            key=self._create_unique_random_key(self.url_key_length),
        )

        # Return the shortened URL
        return dtos.CreateURLOutput(
            shortened_url=urljoin(
                get_settings().base_url,
                url.url_key,
            ),
        )

    def get_url_by_key(self, url_key: str) -> models.URL:
        # Get the URL from the database by its key
        url = self.urls.find_by_key(url_key)

        # Raise an exception if the URL doesn't exist
        if not url:
            raise HTTPException(
                status_code=404,
                detail=f"URL '{url_key}' doesn't exist",
            )

        # If the URL exists, return it
        return url
