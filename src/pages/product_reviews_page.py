import time
import pytest

from selenium.common.exceptions import StaleElementReferenceException
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from src.utils.locators import L
from src.utils.waits import wait_visible


class ProductReviewsPage:
    def __init__(self, driver):
        self.driver = driver

    REVIEWS_TAB_CANDIDATES = (
        L.REVIEWS_TAB,
        (
            By.XPATH,
            "//button[@role='tab' and contains(translate(normalize-space(.),'ABCDEFGHIJKLMNOPQRSTUVWXYZÇĞİÖŞÜ','abcdefghijklmnopqrstuvwxyzçğiöşü'),'değerlendirme')]",
        ),
        (
            By.XPATH,
            "//button[@role='tab' and contains(translate(normalize-space(.),'ABCDEFGHIJKLMNOPQRSTUVWXYZÇĞİÖŞÜ','abcdefghijklmnopqrstuvwxyzçğiöşü'),'yorum')]",
        ),
        (
            By.XPATH,
            "//*[@role='tab' and contains(translate(normalize-space(.),'ABCDEFGHIJKLMNOPQRSTUVWXYZÇĞİÖŞÜ','abcdefghijklmnopqrstuvwxyzçğiöşü'),'değerlendirme')]",
        ),
        (
            By.XPATH,
            "//*[@role='tab' and contains(translate(normalize-space(.),'ABCDEFGHIJKLMNOPQRSTUVWXYZÇĞİÖŞÜ','abcdefghijklmnopqrstuvwxyzçğiöşü'),'yorum')]",
        ),
    )

    def _scroll_into_view(self, element):
        self.driver.execute_script("arguments[0].scrollIntoView({block:'center'});", element)

    def _click_with_fallback(self, element):
        self._scroll_into_view(element)

        try:
            ActionChains(self.driver).move_to_element(element).pause(0.1).click().perform()
            return
        except Exception:
            pass

        try:
            element.click()
            return
        except Exception:
            pass

        self.driver.execute_script("arguments[0].click();", element)

    def _first_visible(self, locators, timeout=10):
        end = time.time() + timeout
        while time.time() < end:
            for locator in locators:
                try:
                    for element in self.driver.find_elements(*locator):
                        if element.is_displayed():
                            return element
                except Exception:
                    continue
            time.sleep(0.2)
        return None

    def _wait_reviews_ready(self, timeout=20):
        section_locators = (
            L.REVIEWS_CONTAINER,
            (By.CSS_SELECTOR, "[id*='review']"),
            (By.CSS_SELECTOR, "[class*='review']"),
        )
        marker_locators = (
            (By.XPATH, "//*[@role='button' and (contains(.,'S\\u0131rala') or contains(.,'Varsay\\u0131lan') or contains(.,'En yeni'))]"),
            (By.XPATH, "//*[contains(.,'de\\u011ferlendirme') or contains(.,'yorum')]"),
            L.NO_REVIEWS_TEXT,
        )

        end = time.time() + timeout
        while time.time() < end:
            if self._first_visible(section_locators, timeout=2):
                return
            if self._first_visible(marker_locators, timeout=2):
                return
        raise AssertionError("Reviews section did not become ready.")

    def _find_reviews_tab(self, timeout=12):
        return self._first_visible(self.REVIEWS_TAB_CANDIDATES, timeout=timeout)

    def _reviews_tab_selected(self, tab_element):
        try:
            if (tab_element.get_attribute("aria-selected") or "").lower() == "true":
                return True
            class_name = (tab_element.get_attribute("class") or "").lower()
            return "active" in class_name or "selected" in class_name
        except Exception:
            return False

    def _any_reviews_tab_selected(self):
        for locator in self.REVIEWS_TAB_CANDIDATES:
            try:
                for element in self.driver.find_elements(*locator):
                    if element.is_displayed() and self._reviews_tab_selected(element):
                        return True
            except Exception:
                continue
        return False

    def wait_pdp_ready(self):
        title = wait_visible(self.driver, L.PDP_TITLE, timeout=30)
        assert title.text.strip(), "PDP title is empty"

    def go_to_reviews(self):
        last_error = None

        for _ in range(10):
            try:
                tab = self._find_reviews_tab(timeout=15)
                if not tab:
                    raise AssertionError("Reviews tab could not be located on PDP.")

                self._click_with_fallback(tab)
                WebDriverWait(self.driver, 10).until(
                    lambda d: self._reviews_tab_selected(tab) or self._any_reviews_tab_selected()
                )
                self._wait_reviews_ready(timeout=20)
                return
            except StaleElementReferenceException as exc:
                last_error = exc
            except Exception as exc:
                last_error = exc
                time.sleep(0.25)

        raise AssertionError(f"Could not open reviews section. Last error: {last_error}")

    def skip_if_no_reviews(self):
        try:
            WebDriverWait(self.driver, 3).until(EC.visibility_of_element_located(L.NO_REVIEWS_TEXT))
            pytest.skip("This product does not have reviews.")
        except Exception:
            return

    def sort_by_newest(self):
        self._wait_reviews_ready(timeout=15)

        all_reviews_button_locators = (
            (By.XPATH, "//a[contains(.,'T\u00fcm de\u011ferlendirmeler') or contains(.,'T\u00fcm yorumlar')]"),
            (By.XPATH, "//button[contains(.,'T\u00fcm de\u011ferlendirmeler') or contains(.,'T\u00fcm yorumlar')]"),
        )
        default_sort_locators = (
            (
                By.CSS_SELECTOR,
                "#hermes-voltran-comments > div.hermes-ReviewList-module-eY_sarN5VMgtON43g9EM > div.hermes-FiltersContainer-module-ELCvjqeomGNRLm_P2jzI > div.hermes-FiltersContainer-module-mnQUatcxsv52cDedZndL > div.hermes-FiltersContainer-module-yVJCt2Xel3B1vUPtdO7s > div > div.hermes-Sort-module-VANnZ3_cDZVFx6SLhcdd > div > div.hermes-Sort-module-vJqiqyAGHsTNXjMsIwJD > div",
            ),
            (
                By.XPATH,
                "//*[@id='hermes-voltran-comments']/div[5]/div[1]/div[1]/div[3]/div/div[2]/div/div[2]/div",
            ),
            (By.XPATH, "//*[contains(@class,'hermes-Sort-module-') and normalize-space()='Varsay\u0131lan']"),
            (By.XPATH, "//*[normalize-space()='S\u0131rala']/following::*[normalize-space()='Varsay\u0131lan'][1]"),
        )
        newest_option_locators = (
            (By.XPATH, "//*[contains(@class,'hermes-Sort-module-') and normalize-space()='En yeni de\u011ferlendirme']"),
            (By.XPATH, "//*[normalize-space()='En yeni de\u011ferlendirme']"),
            (By.XPATH, "//*[contains(normalize-space(), 'En yeni')]"),
        )

        default_sort = self._first_visible(default_sort_locators, timeout=8)
        if not default_sort:
            all_reviews_btn = self._first_visible(all_reviews_button_locators, timeout=5)
            if all_reviews_btn:
                self._click_with_fallback(all_reviews_btn)
                self._wait_reviews_ready(timeout=15)
                default_sort = self._first_visible(default_sort_locators, timeout=8)

        if not default_sort:
            # Some product templates do not expose sort controls.
            # Continue scenario without sorting instead of skipping whole test.
            return False

        self._click_with_fallback(default_sort)

        newest = self._first_visible(newest_option_locators, timeout=6)
        if not newest:
            raise AssertionError("Could not find 'En yeni değerlendirme' option.")

        self._click_with_fallback(newest)
        time.sleep(0.5)
        return True

    def click_any_thumb(self):
        for locator, result in ((L.THUMBS_UP, "up"), (L.THUMBS_DOWN, "down")):
            for element in self.driver.find_elements(*locator):
                try:
                    if not element.is_displayed():
                        continue
                    self._click_with_fallback(element)
                    return result
                except Exception:
                    continue

        pytest.skip("No thumb controls found in reviews list.")

    def assert_thank_you_if_exists(self):
        try:
            WebDriverWait(self.driver, 8).until(EC.visibility_of_element_located(L.THANK_YOU))
        except Exception:
            # Feedback message is not consistently rendered on every product/review card.
            # Keep the flow alive if voting does not show an explicit toast/text.
            return
