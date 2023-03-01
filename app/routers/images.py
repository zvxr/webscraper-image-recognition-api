from fastapi import APIRouter, UploadFile

from app.crawlers.images import TwitterImageCrawler
from app.log import get_logger
from app.schemas.images import ImageCrawlerRequest
from app.schemas.ml import ModelSummaryResponse
from app.services.images import ImageService


router = APIRouter(
    prefix="/images",
)
logger = get_logger(__name__)


@router.post(
    "/crawler",
    response_model=ModelSummaryResponse,
)
async def post_images_crawler(
    payload: ImageCrawlerRequest,
):
    logger.debug(f"received query: {payload.query}")
    crawler = TwitterImageCrawler()
    urls = crawler.fetch_urls_by_query(payload.query)

    service = ImageService()
    file_paths = await service.download_urls(payload.query, urls)

    sequential_image_ml.reset_model()
    return sequential_image_ml.get_summary()
