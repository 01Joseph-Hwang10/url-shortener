import validators
from urllib.parse import urljoin
from dependency_injector.wiring import Provide
from shortuuid import ShortUUID
from src.db.model import URL
from src.app.config import Config
from ._exception import URLNotFoundExcpetion, InvalidURLException


class URLShortenerService:
    """URL shortener service.

    Provides methods to create and find URLs.
    """

    url: URL = Provide["url"]
    config: Config = Provide["config"]

    def find_by_short_slug(self, short_slug: str) -> str:
        """Find URL by short slug.

        Args:
            short_slug: Short slug of URL.

        Returns:
            Original URL.

        Raises:
            URLNotFoundException: If URL is not found.
        """
        url: URL = self.url.select().where(URL.short_slug == short_slug).first()
        if url is None:
            raise URLNotFoundExcpetion(f"URL with short slug {short_slug} not found")
        return url.original_url

    def create(self, original_url: str) -> dict:
        """Create a shortened URL.
        If given url is already shortened, return the existing short url.

        Args:
            request: CreateShortURLRequest object.

        Returns:
            CreateShortURLResponse object.

        Raises:
            InvalidURLException: If given URL is invalid.
        """
        if not validators.url(original_url):
            raise InvalidURLException(f"Invalid URL: {original_url}")

        newly_created: bool = False
        url: URL = self.url.select().where(URL.original_url == original_url).first()
        if not url:
            url = self.url.create(
                original_url=original_url,
                short_slug=ShortUUID().random(length=8),
            )
            newly_created = True

        protocol = "https" if self.config.ssl_enabled else "http"
        return {
            "original_url": url.original_url,
            "short_slug": url.short_slug,
            "short_url": urljoin(
                protocol + "://" + self.config.server_name,
                url.short_slug,
            ),
            "newly_created": newly_created,
        }
