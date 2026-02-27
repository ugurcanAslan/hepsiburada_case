from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait


def wait_visible(driver, locator, timeout=30):
    return WebDriverWait(driver, timeout).until(EC.visibility_of_element_located(locator))


def wait_clickable(driver, locator, timeout=30):
    return WebDriverWait(driver, timeout).until(EC.element_to_be_clickable(locator))


def wait_all(driver, locator, timeout=30):
    return WebDriverWait(driver, timeout).until(EC.presence_of_all_elements_located(locator))


def wait_interactable(driver, locator, timeout=30):
    def _predicate(drv):
        for element in drv.find_elements(*locator):
            try:
                if not element.is_displayed() or not element.is_enabled():
                    continue
                rect = element.rect or {}
                if (rect.get("width", 0) or 0) <= 0:
                    continue
                if (rect.get("height", 0) or 0) <= 0:
                    continue
                return element
            except Exception:
                continue
        return False

    return WebDriverWait(driver, timeout).until(_predicate)
