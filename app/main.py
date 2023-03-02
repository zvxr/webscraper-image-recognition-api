from fastapi import FastAPI
from fastapi.responses import JSONResponse

from app.log import get_logger, setup_logging
from app.routers import diagnostics, images
from app.version import __version__

setup_logging()
logger = get_logger(__name__)


app = FastAPI(
    title="Image Crawler API",
    version=__version__,
    default_response_class=JSONResponse,
    debug=True,
)
app.include_router(diagnostics.router)
app.include_router(images.router)
