from io import BytesIO
import os
from PIL import Image
from typing import List, Tuple
from uuid import uuid4

from fastapi import UploadFile
from httpx import AsyncClient

from app.log import get_logger


logger = get_logger("__name__")


class ImageService:

    def _setup_download_path(self, query: str) -> str:
        """Makes sure that download path (based on query) exists, then returns it."""
        base_path = self.get_downloaded_path()
        path = f"{base_path}/{query}"
        if not os.path.exists(path):
            os.makedirs(path)
        return path

    async def download_urls(self, query: str, urls: List[str]) -> List[str]:
        base_path = self._setup_download_path(query)
        file_paths = []
        async with AsyncClient() as client:
            for url in urls:
                uid = uuid4()
                dest = f"{base_path}/{uid}.jpg"
                success = await self.download_url(url, dest, client)
                if success:
                    file_paths.append(dest)
        logger.info(f"Completed downloads with [{len(file_paths)} / {len(urls)}] downloaded.")
        return file_paths

    async def download_url(self, url: str, dest: str, client: AsyncClient) -> bool:
        logger.info(f"Downloading {url} to {dest}...")
        resp = await client.get(url)
        if not 200 <= resp.status_code < 300:
            logger.warning(f"Non 2xx response from {url}: {resp.content}")
            return False
        with open(dest, "wb") as fl:
            fl.write(resp.content)
        logger.info(f"Finished writing {url} to {dest}")
        return True

    @classmethod
    def get_downloaded_path(cls) -> str:
        return f"{os.path.abspath(os.getcwd())}/app/data/images/downloaded"
