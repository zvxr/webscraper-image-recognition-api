from pydantic import BaseModel, constr

URL_SAFE_REGEX = r"^[a-zA-Z0-9_-]*$"


# Request
class ImageCrawlerRequest(BaseModel):
    query: constr(regex=URL_SAFE_REGEX)

    class Config:
        schema_extra = {
            "example": {
                "query": "cat",
            }
        }
