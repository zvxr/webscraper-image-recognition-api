import os
from unittest import mock
import uuid

from fastapi import UploadFile
import jsonschema
from PIL import Image
import pytest

from app.routers.images import TwitterImageCrawler
from app.services.images import ImageService


TEST_IMAGE = "test_cat.jpg"
TEST_IMAGE_PATH = f"{os.path.dirname(os.path.realpath(__file__))}/assets/{TEST_IMAGE}"
TEST_UUID = uuid.UUID('c0ff33c0-ffee-c0ff-eec0-ffeec0ffeec0')
QUERY = "flowers"

DOWNLOADED_PATH = ImageService.get_downloaded_path()
DOWNLOADED_FILE_PATH = f"{DOWNLOADED_PATH}/{QUERY}/{str(TEST_UUID)}.jpg"
UPLOAD_PATH = ImageService.get_upload_path()
UPLOAD_FILE_PATH = f"{UPLOAD_PATH}/{TEST_IMAGE}"


# Validation Schemas
model_prediction_schema = {
    "type": "object",
    "properties": {
        "class_name": {"type": "string"},
        "confidence": {"type": "number", "minimum": 0, "maximum": 1.0},
    },
    "required": ["class_name", "confidence"],
    "additionalProperties": False,
}

model_layer_schema = {
    "type": "object",
    "properties": {
        "name": {"type": "string"},
        "class_name": {"type": "string"},
        "params": {"type": "integer"},
        "output_shape": {"type": "array"},
    },
    "required": ["name", "class_name", "params", "output_shape"],
    "additionalProperties": False,
}

model_summary_schema = {
    "type": "object",
    "properties": {
        "name": {"type": "string"},
        "total_params": {"type": "integer"},
        "trainable_params": {"type": "integer"},
        "non_trainable_params": {"type": "integer"},
        "layers": {
            "type": "array",
            "items": model_layer_schema,
        },
    },
    "required": ["name", "total_params", "trainable_params", "non_trainable_params", "layers"],
    "additionalProperties": False,
}


# Fixtures
@pytest.fixture()
def twitter_image_crawler():
    crawler_mock = mock.Mock()
    crawler_mock.fetch_urls_by_query.return_value = [
        # TODO: may not be very stable--host images or mock.
        "https://fastly.picsum.photos/id/908/300/300.jpg?hmac=Kr9iK9ySwwpN-5dnU7po_rUxEoeoaJrp0bjX21M1sd4"
    ]
    with mock.patch("app.routers.images.TwitterImageCrawler", return_value=crawler_mock):
        yield crawler_mock


@pytest.fixture()
def static_uuid():
    # Remove image from previous runs.
    try:
        os.remove(DOWNLOADED_FILE_PATH)
    except OSError:
        pass

    with mock.patch("app.services.images.uuid4", return_value=TEST_UUID):
        yield TEST_UUID


@pytest.fixture()
def upload_image_file():
    # Remove uploaded image from previous runs.
    try:
        os.remove(UPLOAD_FILE_PATH)
    except OSError:
        pass

    with open(TEST_IMAGE_PATH, "rb") as img:
        yield {"file": (TEST_IMAGE, img, "image/jpeg")}


# Tests
def test_post_images_analyzer_ok(upload_image_file, client):
    resp = client.post("/images/analyzer", files=upload_image_file)

    # Successful response with expected format
    assert resp.status_code == 200
    jsonschema.validate(resp.json(), model_prediction_schema)

    # File generated correctly
    failure_message = f"File was not uploaded to {UPLOAD_FILE_PATH}"
    assert os.path.exists(UPLOAD_FILE_PATH), failure_message


def test_post_images_analyzer_missing_file(client):
    resp = client.post("/images/analyzer")

    assert resp.status_code == 422


def test_post_images_crawler_ok(twitter_image_crawler, static_uuid, client):
    body = {"query": QUERY}
    resp = client.post("/images/crawler", json=body)

    # Successful response with expected format
    assert resp.status_code == 200
    jsonschema.validate(resp.json(), model_summary_schema)

    # Correct (mock) crawler calls
    assert twitter_image_crawler.fetch_urls_by_query.called
    assert twitter_image_crawler.fetch_urls_by_query.call_args_list == [
        mock.call(QUERY)
    ]

    # File generated correctly
    failure_message = f"File was not uploaded to {DOWNLOADED_FILE_PATH}. Check {twitter_image_crawler.fetch_urls_by_query.return_value}"
    assert os.path.exists(DOWNLOADED_FILE_PATH), failure_message


def test_post_images_crawler_invalid_query(twitter_image_crawler, client):
    body = {"query": "<@)1 dl..sé"}
    resp = client.post("/images/crawler", json=body)

    assert resp.status_code == 422
    assert not twitter_image_crawler.fetch_urls_by_query.called
