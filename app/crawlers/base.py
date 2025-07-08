import atexit
from contextlib import contextmanager
from typing import List

from selenium import webdriver

from app.log import get_logger

logger = get_logger("__name__")


class Crawler:
    def __init__(self):
        self._driver = None
        atexit.register(self.cleanup)

    def cleanup(self):
        logger.info(f"Exiting Crawler during run. Removing {self._driver}.")
        if self._driver:
            self._driver.quit()

    def fetch_urls_by_query(self, query: str, max_records: int = 5) -> List[str]:
        raise NotImplementedError("This must be overridden.")

    @contextmanager
    def get_driver(self):
        options = webdriver.ChromeOptions()
        options.add_argument("--headless")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-gpu")
        options.add_argument("--disable-dev-shm-usage")
        self._driver = webdriver.Remote("http://selenium:4444/wd/hub", options=options)
        yield self._driver
        self._driver.quit()
        self._driver = None
