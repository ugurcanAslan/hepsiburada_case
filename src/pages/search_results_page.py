import random
from urllib.parse import urljoin, urlparse

from selenium.webdriver.support.ui import WebDriverWait

from src.utils.locators import L
from src.utils.waits import wait_all


class SearchResultsPage:
    def __init__(self, driver):
        self.driver = driver

    def _is_product_url(self, href: str) -> bool:
        if not href:
            return False

        absolute = urljoin("https://www.hepsiburada.com", href)
        parsed = urlparse(absolute)

        if parsed.netloc not in ("www.hepsiburada.com", "hepsiburada.com"):
            return False

        path = parsed.path.lower()
        if "-p-" not in path and "-pm-" not in path:
            return False

        bad_tokens = ["adservice", "/event/", "/track", "track", "analytics"]
        return not any(token in absolute.lower() for token in bad_tokens)

    def pick_random_product(self, seed=None, max_scan=80):
        anchors = wait_all(self.driver, L.PRODUCT_LINKS, timeout=30)
        if not anchors:
            raise AssertionError("No links were found on search results page.")

        candidates = []
        for anchor in anchors[:max_scan]:
            try:
                href = anchor.get_attribute("href")
                if not self._is_product_url(href):
                    continue
                title = (anchor.get_attribute("title") or anchor.text or "").strip()
                candidates.append((href, title))
            except Exception:
                continue

        if not candidates:
            raise AssertionError("No product link found after filtering result anchors.")

        rng = random.Random(seed) if seed is not None else random
        href, listing_title = rng.choice(candidates)

        absolute_href = urljoin("https://www.hepsiburada.com", href)
        self.driver.get(absolute_href)
        WebDriverWait(self.driver, 20).until(lambda d: "/ara" not in d.current_url)

        return {"listing_title": listing_title, "href": absolute_href}
