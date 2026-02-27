from selenium.webdriver.common.by import By


class L:
    SEARCH_INPUT = (By.CSS_SELECTOR, "[data-test-id='search-bar-input']")
    COOKIE_ACCEPT = (By.ID, "onetrust-accept-btn-handler")

    PRODUCT_LINKS = (By.CSS_SELECTOR, "a[href]")

    PDP_TITLE = (By.CSS_SELECTOR, "h1")
    FS_TITLE = (By.CSS_SELECTOR, "h2[data-test-id='fs-title']")
    FS_PRODUCT_CARDS = (By.CSS_SELECTOR, "a[data-test-id='fs-product-card']")
    FS_TABLE = (By.CSS_SELECTOR, "table[data-test-id='fs-table']")
    FS_PRICE_ROW = (
        By.XPATH,
        "//tr[@data-test-id='fs-classification-row'][.//em[normalize-space()='Fiyat']]",
    )
    FS_PRICE_VALUES = (
        By.XPATH,
        "//tr[@data-test-id='fs-classification-row'][.//em[normalize-space()='Fiyat']]/td[position()>1]",
    )
    FS_ADD_TO_CART_BUTTON = (By.CSS_SELECTOR, '[data-test-id="fs-add-to-cart-button"]')

    PDP_DEFAULT_PRICE = (By.CSS_SELECTOR, '[data-test-id="default-price"]')
    PDP_ADD_TO_CART = (By.CSS_SELECTOR, 'button[data-test-id="addToCart"]')

    REVIEWS_TAB = (By.CSS_SELECTOR, "button[role='tab'][aria-controls='Reviews']")
    REVIEWS_CONTAINER = (By.CSS_SELECTOR, "#hermes-voltran-comments")

    THUMBS_UP = (By.CSS_SELECTOR, ".thumbsUp")
    THUMBS_DOWN = (By.CSS_SELECTOR, ".thumbsDown")

    THANK_YOU = (
        By.XPATH,
        "//*[contains(.,'Te\\u015fekk\\u00fcr') or contains(.,'te\\u015fekk\\u00fcr')]",
    )

    NO_REVIEWS_TEXT = (
        By.XPATH,
        "//*[contains(.,'Hen\\u00fcz de\\u011ferlendirme') "
        "or contains(.,'\\u0130lk de\\u011ferlendiren') "
        "or contains(.,'de\\u011ferlendirme bulunamad\\u0131')]",
    )
