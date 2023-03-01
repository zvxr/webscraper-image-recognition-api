from typing import Optional

from pydantic import BaseModel

# Request


# Response
class DiagnosticsResponse(BaseModel):
    message: Optional[str] = "OK"
