import re
import time

import pytest

from src.pages.home_page import HomePage
from src.pages.product_reviews_page import ProductReviewsPage
from src.pages.search_results_page import SearchResultsPage
from src.utils.locators import L
from src.utils.waits import wait_all, wait_visible


def reveal_comparison_section(driver, max_scroll=30):
    for _ in range(max_scroll):
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(0.8)
        if (
            driver.find_elements(*L.FS_TITLE)
            or driver.find_elements(*L.FS_TABLE)
            or driver.find_elements(*L.FS_PRODUCT_CARDS)
        ):
            return True
    return bool(
        driver.find_elements(*L.FS_TITLE)
        or driver.find_elements(*L.FS_TABLE)
        or driver.find_elements(*L.FS_PRODUCT_CARDS)
    )


def parse_price(text):
    if not text:
        return None

    compact = re.sub(r"[^0-9,\.]", "", text)
    if not compact:
        return None

    if "," in compact and "." in compact:
        normalized = compact.replace(".", "").replace(",", ".")
    elif "," in compact:
        normalized = compact.replace(".", "").replace(",", ".")
    else:
        parts = compact.split(".")
        if len(parts) > 1 and len(parts[-1]) == 2:
            normalized = compact
        else:
            normalized = compact.replace(".", "")

    try:
        return float(normalized)
    except Exception:
        return None


def normalize_turkish(text):
    return (
        text.casefold()
        .replace("ş", "s")
        .replace("ı", "i")
        .replace("ç", "c")
        .replace("ö", "o")
        .replace("ü", "u")
        .replace("ğ", "g")
    )


def click_with_fallback(driver, element):
    driver.execute_script("arguments[0].scrollIntoView({block:'center'});", element)
    try:
        element.click()
        return
    except Exception:
        pass
    driver.execute_script("arguments[0].click();", element)


@pytest.mark.ui
def test_scenario_2(driver):
    home = HomePage(driver)
    home.open()

    home.search("iphone")
    assert "/ara" in driver.current_url or "q=" in driver.current_url or "query=" in driver.current_url

    search_results = SearchResultsPage(driver)
    pdp = ProductReviewsPage(driver)
    search_results.pick_random_product()
    pdp.wait_pdp_ready()
    reveal_comparison_section(driver)

    fs_title = wait_visible(driver, L.FS_TITLE, timeout=12)
    fs_table = wait_visible(driver, L.FS_TABLE, timeout=12)
    product_cards = wait_all(driver, L.FS_PRODUCT_CARDS, timeout=12)

    assert fs_title.is_displayed()
    assert "karsilastirilanlar" in normalize_turkish(
        fs_title.text
    ), "Baslik en cok karsilastirilanlar alani degil."
    assert fs_table.is_displayed()
    assert product_cards, "Karsilastirilan urun kartlari bulunamadi."

    pdp_price_text = wait_visible(driver, L.PDP_DEFAULT_PRICE, timeout=12).text
    pdp_price = parse_price(pdp_price_text)
    assert pdp_price is not None, "PDP fiyati parse edilemedi."

    fs_price_values = []
    for price_cell in driver.find_elements(*L.FS_PRICE_VALUES):
        parsed = parse_price(price_cell.text)
        if parsed is not None:
            fs_price_values.append(parsed)

    fs_buttons = driver.find_elements(*L.FS_ADD_TO_CART_BUTTON)
    overlay_has_products = bool(product_cards and fs_price_values and fs_buttons)

    if not overlay_has_products:
        pdp_add_to_cart = wait_visible(driver, L.PDP_ADD_TO_CART, timeout=12)
        click_with_fallback(driver, pdp_add_to_cart)
        return

    lowest_overlay_index = min(range(len(fs_price_values)), key=lambda idx: fs_price_values[idx])
    lowest_overlay_price = fs_price_values[lowest_overlay_index]

    if pdp_price <= lowest_overlay_price:
        pdp_add_to_cart = wait_visible(driver, L.PDP_ADD_TO_CART, timeout=12)
        click_with_fallback(driver, pdp_add_to_cart)
        return

    target_index = min(lowest_overlay_index, len(fs_buttons) - 1)
    click_with_fallback(driver, fs_buttons[target_index])
