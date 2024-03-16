from dependency_injector.wiring import Provide
from fastapi import APIRouter, Depends, HTTPException, status
from ._dto import CreateShortURLRequest, CreateShortURLResponse
from ._service import URLShortenerService
from ._exception import URLNotFoundExcpetion

router = APIRouter()


@router.post("/")
def create_short_url(
    request: CreateShortURLRequest,
    service: URLShortenerService = Depends(Provide["url_shortener"]),
) -> CreateShortURLResponse:
    """Create a shortened URL."""
    return service.create(request)


@router.get("/{short_slug}")
def find_url_and_redirect(
    short_slug: str,
    service: URLShortenerService = Depends(Provide["url_shortener"]),
) -> str:
    """Find URL by short slug
    and redirect the user to the original URL.
    """
    try:
        return service.find_by_short_slug(short_slug)
    except URLNotFoundExcpetion:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="URL not found.",
        )
