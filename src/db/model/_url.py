from .._base import BaseModel
from peewee import CharField


class URL(BaseModel):
    original_url = CharField(unique=True)
    """Original URL."""
    short_slug = CharField(unique=True)
    """Slug of shortened URL.

    This is the part of the URL that comes after the domain name.

    Example:
        - https://example.com/short_slug
    """

    class Meta:
        db_table = "urls"
