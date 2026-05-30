from fastapi import APIRouter, HTTPException, Request
from fastapi.responses import RedirectResponse

from .redis_client import get_url
from .schemas import URLRequest, URLResponse
from .services import create_short_url

router = APIRouter()

@router.get("/{code}", response_class=RedirectResponse)
def redirect_url(code: str):
    long_url = str(get_url(code))
    
    if long_url is None:
        raise HTTPException(status_code=404, detail="URL not found")
    
    return RedirectResponse(url=long_url, status_code=302)


@router.post("/shorten", response_model=URLResponse)
def shorten_url(data: URLRequest, request: Request):
    code = create_short_url(str(data.url), data.duration)
    short_url = f"{request.base_url}{code}"
    return URLResponse(short_url=short_url)
        