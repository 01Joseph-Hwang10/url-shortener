from dependency_injector.wiring import inject, Provide
from fastapi import APIRouter, Depends, HTTPException, status, Response
from fastapi.responses import RedirectResponse
from ._dto import CreateShortURLRequest, CreateShortURLResponse
from ._service import URLShortenerService
from ._exception import URLNotFoundExcpetion, InvalidURLException

router = APIRouter()


@router.post(
    "/",
    response_model=CreateShortURLResponse,
    status_code=status.HTTP_201_CREATED,
)
@inject
async def create_short_url(
    request: CreateShortURLRequest,
    response: Response,
    service: URLShortenerService = Depends(Provide["url_shortener"]),
):
    """Create a shortened URL."""
    try:
        creation_result = service.create(request.url)

        if not creation_result["newly_created"]:
            response.status_code = status.HTTP_200_OK
        del creation_result["newly_created"]

        return creation_result
    except InvalidURLException:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid URL.",
        )


@router.get(
    "/{short_slug}",
    response_class=RedirectResponse,
    status_code=status.HTTP_308_PERMANENT_REDIRECT,
)
@inject
async def find_url_and_redirect(
    short_slug: str,
    service: URLShortenerService = Depends(Provide["url_shortener"]),
):
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
