from fastapi import APIRouter, UploadFile

from app.crawlers.images import TwitterImageCrawler
from app.log import get_logger
from app.ml.images import sequential_image_ml
from app.schemas.images import ImageCrawlerRequest
from app.schemas.ml import ModelPrediction, ModelSummaryResponse
from app.services.images import ImageService

router = APIRouter(
    prefix="/images",
)
logger = get_logger(__name__)


@router.post(
    "/analyzer",
    response_model=ModelPrediction,
)
async def post_images_analyzer(
    file: UploadFile,
):
    logger.debug(f"received file: {file.filename}.")
    service = ImageService()
    file_path = await service.upload(
        file, (sequential_image_ml.IMG_HEIGHT, sequential_image_ml.IMG_WIDTH)
    )
    return sequential_image_ml.get_prediction(file_path)


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
    await service.download_urls(payload.query, urls)

    sequential_image_ml.reset_model()
    return sequential_image_ml.get_summary()
