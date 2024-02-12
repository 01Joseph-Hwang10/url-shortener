from sqlalchemy.orm import Session
from src import models
from ._repository import URLRepository


class SQLAlchemyURLRepository(URLRepository):
    def __init__(self, db: Session):
        self.db = db

    def create(self, url: str, key: str) -> models.URL:
        # Create a new URL in the database
        url = models.URL(
            target_url=url,
            key=key,
        )
        self.db.add(url)
        self.db.commit()
        self.db.refresh(url)

        return url

    def find_by_key(self, key: str) -> models.URL | None:
        # Get the URL from the database by its key
        url = self.db.query(models.URL).filter(models.URL.key == key).first()

        return url
