from fastapi import APIRouter, HTTPException, Request
from fastapi.responses import RedirectResponse

from .schemas import URLRequest, URLResponse, MessageResponse
from .services import create_short_code, get_long_url, delete_short_code

router = APIRouter()

@router.get("/{code}", response_class=RedirectResponse)
def redirect_url(code: str):
    long_url = get_long_url(code)
    
    if long_url is None:
        return RedirectResponse(url=f"https://url-shortener-1-x8vr.onrender.com/not-found.html?code={code}", status_code=302)
    
    return RedirectResponse(long_url, status_code=302)


@router.post("/shorten", response_model=URLResponse)
def shorten_url(data: URLRequest, request: Request):
    code = create_short_code(data.url, data.duration)
    
    short_url = f"{request.base_url}{code}"
    
    return URLResponse(short_url=short_url)


@router.delete("/{code}", response_model=MessageResponse)
def remove_url(code: str):
    if not delete_short_code(code):
        raise HTTPException(status_code=404, detail="URL not found")
    
    return MessageResponse(message="Deleted Successfully")
