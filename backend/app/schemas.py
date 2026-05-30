from pydantic import BaseModel, HttpUrl, Field

class URLRequest(BaseModel):
    url: HttpUrl
    duration: int = Field(default=86400, gt=0, le=31536000) # 0 < duration <= 1 year (in seconds)
    
class URLResponse(BaseModel):
    short_url: str
