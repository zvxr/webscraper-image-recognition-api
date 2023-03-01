from typing import Optional

from pydantic import BaseModel

from app.log import get_logger


# Request


# Response
class DiagnosticsResponse(BaseModel):
    message: Optional[str] = "OK"
