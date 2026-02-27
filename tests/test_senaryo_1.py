import re
from urllib.parse import urlparse

import pytest

from src.pages.home_page import HomePage
from src.pages.product_reviews_page import ProductReviewsPage
from src.pages.search_results_page import SearchResultsPage


def extract_hbc_id(url: str) -> str:
    path = urlparse(url).path
    hbc_match = re.search(r"(HBC[A-Z0-9]+)", path, re.IGNORECASE)
    if hbc_match:
        return hbc_match.group(1).upper()

    # Fallback for product URLs that do not contain an HBC id.
    generic_match = re.search(r"-(?:p|pm)-([A-Z0-9]+)(?:/|$)", path, re.IGNORECASE)
    return generic_match.group(1).upper() if generic_match else ""


@pytest.mark.ui
def test_scenario_1(driver):
    home = HomePage(driver)
    home.open()

    home.search("ps5")
    assert "/ara" in driver.current_url or "q=" in driver.current_url or "query=" in driver.current_url

    search_results = SearchResultsPage(driver)
    chosen = search_results.pick_random_product()

    reviews = ProductReviewsPage(driver)
    reviews.wait_pdp_ready()

    chosen_id = extract_hbc_id(chosen["href"])
    current_id = extract_hbc_id(driver.current_url)
    assert chosen_id and current_id and chosen_id == current_id

    reviews.go_to_reviews()
    reviews.skip_if_no_reviews()
    reviews.sort_by_newest()
    reviews.click_any_thumb()
    reviews.assert_thank_you_if_exists()
