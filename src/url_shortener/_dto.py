from pydantic import BaseModel


class CreateShortURLRequest(BaseModel):
    url: str
    """URL to be shortened."""


class CreateShortURLResponse(BaseModel):
    original_url: str
    """Original URL."""
    short_slug: str
    """Slug of shortened URL.

    This is the part of the URL that comes after the domain name.

    Example:
        - https://example.com/short_slug
    """
    short_url: str
    """Shortened URL including domain name."""
