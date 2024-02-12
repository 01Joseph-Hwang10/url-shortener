from ._repository import URLRepository
from src import models


class MockURLRepository(URLRepository):
    def __init__(
        self,
        db=None,
    ):
        self.db: list[models.URL] = db or []

    def create(self, url: str, key: str) -> models.URL:
        url = models.URL(
            target_url=url,
            url_key=key,
        )
        self.db.append(url)
        return url

    def find_by_key(self, key: str) -> models.URL | None:
        for url in self.db:
            if url.url_key == key:
                return url
        return None
