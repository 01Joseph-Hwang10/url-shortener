import validators
from urllib.parse import urljoin
from fastapi import HTTPException
from sqlalchemy.orm import Session
from shortuuid import ShortUUID
from ..config import get_settings
from .. import models, dtos


class URLService:

    def __init__(
        self,
        db: Session,
    ) -> None:
        self.db = db

    def _create_unique_random_key(
        self,
        length: int = 10,
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
        url = models.URL(
            target_url=request.target_url,
            key=self._create_unique_random_key(),
        )
        self.db.add(url)
        self.db.commit()
        self.db.refresh(url)

        # Return the shortened URL
        return dtos.CreateURLOutput(
            shortened_url=urljoin(
                get_settings().base_url,
                url.key,
            ),
        )

    def get_db_url_by_key(self, url_key: str) -> models.URL:
        # Get the URL from the database by its key
        url = self.db.query(models.URL).filter(models.URL.key == url_key).first()

        # Raise an exception if the URL doesn't exist
        if not url:
            raise HTTPException(
                status_code=404,
                detail=f"URL '{url_key}' doesn't exist",
            )

        # If the URL exists, return it
        return url
