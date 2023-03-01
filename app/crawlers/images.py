from typing import List

from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


from app.crawlers.base import Crawler
from app.log import get_logger


logger = get_logger("__name__")


class TwitterImageCrawler(Crawler):

    def fetch_urls_by_query(self, query: str, max_records: int = 5) -> List[str]:
        # Perform Twitter query.
        url = f"https://twitter.com/search?q={query}&src=typed_query&f=image"
        with self.get_driver() as driver:
            driver.get(url)

            # Wait at most 10 seconds for img path to load.
            WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.XPATH, "//img"))
            )

            # Iterate over images, adding only those that are stored in CDN.
            records = []
            for element in driver.find_elements(By.XPATH, "//img"):
                image_url = element.get_attribute('src')
                logger.debug(f"record image url is {image_url}, {type(image_url)}")
                if image_url.startswith("https://pbs.twimg.com/media"):
                    records.append(image_url)
                    # Exit early if we hit the max_records threshold.
                    if len(records) == max_records:
                        return records
            return records
