from urllib.parse import urljoin
from dependency_injector.wiring import Provide
from shortuuid import ShortUUID
from src.db.model import URL
from src.app.config import Config
from ._dto import CreateShortURLRequest, CreateShortURLResponse
from ._exception import URLNotFoundExcpetion


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
        url: URL = self.url.get(short_slug=short_slug)
        if url is None:
            raise URLNotFoundExcpetion(f"URL with short slug {short_slug} not found")
        return url.original_url

    def create(self, request: CreateShortURLRequest) -> CreateShortURLResponse:
        """Create a shortened URL.
        If given url is already shortened, return the existing short url.

        Args:
            request: CreateShortURLRequest object.

        Returns:
            CreateShortURLResponse object.
        """
        url: URL = self.url.get(original_url=request.url) or self.url.create(
            original_url=request.url,
            short_slug=ShortUUID().random(length=8),
        )

        return CreateShortURLResponse(
            original_url=url.original_url,
            short_slug=url.short_slug,
            short_url=urljoin(f"https://{self.config.server_name}", url.short_slug),
        )
