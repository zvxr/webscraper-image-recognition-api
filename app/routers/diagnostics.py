from fastapi import APIRouter

from app.schemas.diagnostics import DiagnosticsResponse
from app.log import get_logger


router = APIRouter(
    prefix="/diagnostics",
)
logger = get_logger(__name__)


@router.get(
    "",
    response_model=DiagnosticsResponse,
)
def get_diagnostics():
    return DiagnosticsResponse()
