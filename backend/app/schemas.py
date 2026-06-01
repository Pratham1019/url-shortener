from pydantic import BaseModel, Field, field_validator

class URLRequest(BaseModel):
    url: str
    duration: int = Field(default=86400, gt=0, le=31536000) # 0 < duration <= 1 year (in seconds)
    
    @field_validator("url")
    @classmethod
    def validate_url(cls, url: str) -> str:
        url = url.strip()
        
        if not url.startswith(("http://", "https://")):
            return f"https://{url}"
    
        return url
    
class URLResponse(BaseModel):
    short_url: str

class MessageResponse(BaseModel):
    message: str