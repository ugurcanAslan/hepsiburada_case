from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait

from src.utils.locators import L
from src.utils.waits import wait_clickable, wait_interactable


class HomePage:
    URL = "https://www.hepsiburada.com/"
    SEARCH_URL_MARKERS = ("/ara", "q=", "query=")

    def __init__(self, driver):
        self.driver = driver

    def open(self):
        self.driver.get(self.URL)
        self.accept_cookies_if_present()

    def accept_cookies_if_present(self):
        try:
            button = wait_clickable(self.driver, L.COOKIE_ACCEPT, timeout=5)
            self.driver.execute_script("arguments[0].click();", button)
        except Exception:
            pass

        try:
            self.driver.switch_to.active_element.send_keys(Keys.ESCAPE)
        except Exception:
            pass

    def _set_value_js(self, element, text: str):
        self.driver.execute_script(
            """
            const el = arguments[0];
            const val = arguments[1];
            el.value = val;
            el.dispatchEvent(new Event('input', { bubbles: true }));
            el.dispatchEvent(new Event('change', { bubbles: true }));
            """,
            element,
            text,
        )

    def search(self, term: str):
        self.accept_cookies_if_present()
        last_error = None

        for _ in range(10):
            try:
                box = wait_interactable(self.driver, L.SEARCH_INPUT, timeout=10)
                self.driver.execute_script("arguments[0].scrollIntoView({block:'center'});", box)
                self.driver.execute_script("arguments[0].focus();", box)

                try:
                    box.send_keys(Keys.CONTROL, "a")
                    box.send_keys(Keys.DELETE)
                except Exception:
                    pass

                try:
                    box.send_keys(term)
                except Exception:
                    pass

                value = (box.get_attribute("value") or "").strip()
                if term.lower() not in value.lower():
                    self._set_value_js(box, term)
                    value = (box.get_attribute("value") or "").strip()

                if term.lower() not in value.lower():
                    last_error = f"Could not set search input value, current value='{value}'"
                    continue

                box.send_keys(Keys.ENTER)
                WebDriverWait(self.driver, 20).until(
                    lambda d: any(marker in d.current_url for marker in self.SEARCH_URL_MARKERS)
                )
                return

            except Exception as exc:
                last_error = exc
                try:
                    self.driver.switch_to.active_element.send_keys(Keys.ESCAPE)
                except Exception:
                    pass

        raise AssertionError(f"Search could not stabilize. Last error: {last_error}")
