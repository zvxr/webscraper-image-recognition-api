from fastapi import APIRouter

from app.log import get_logger
from app.schemas.diagnostics import DiagnosticsResponse

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
