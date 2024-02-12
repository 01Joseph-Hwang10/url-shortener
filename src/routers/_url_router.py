from fastapi.routing import APIRouter
from fastapi import Depends, Request
from fastapi import status
from fastapi.responses import RedirectResponse
from sqlalchemy.orm import Session
from src import dtos
from src.config import get_db
from src.services.url import URLService
from src.repositories.url import URLRepository

router = APIRouter()


@router.post("/url", response_model=dtos.CreateURLOutput)
def create_url(
    url: dtos.CreateURLInput,
    db: Session = Depends(get_db),
):
    service = URLService(urls=URLRepository(db=db))
    return service.create_url(request=url)


@router.get("/{url_key}")
def forward_to_target_url(
    url_key: str,
    request: Request,
    db: Session = Depends(get_db),
):
    service = URLService(urls=URLRepository(db=db))
    url = service.get_url_by_key(url_key=url_key)
    return RedirectResponse(
        url=url.target_url,
        status_code=status.HTTP_308_PERMANENT_REDIRECT,
    )
