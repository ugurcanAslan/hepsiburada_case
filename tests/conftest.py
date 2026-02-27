import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

from src.api.http_client import HttpClient


def pytest_addoption(parser):
    parser.addoption(
        "--keep-browser",
        action="store_true",
        default=False,
        help="Keep browser open after test run.",
    )
    parser.addoption(
        "--api-base-url",
        action="store",
        default="https://generator.swagger.io/api",
        help="Base URL for API tests.",
    )
    parser.addoption(
        "--api-verify-ssl",
        action="store_true",
        default=False,
        help="Enable SSL certificate verification for API tests.",
    )


@pytest.fixture
def driver(request):
    keep_browser = request.config.getoption("--keep-browser")

    options = Options()
    options.add_argument("--start-maximized")
    options.add_experimental_option(
        "prefs",
        {"profile.default_content_setting_values.notifications": 2},
    )

    if keep_browser:
        options.add_experimental_option("detach", True)

    web_driver = webdriver.Chrome(options=options)
    yield web_driver

    if not keep_browser:
        web_driver.quit()


@pytest.fixture
def api_client(request):
    base_url = request.config.getoption("--api-base-url")
    verify_ssl = request.config.getoption("--api-verify-ssl")
    return HttpClient(base_url=base_url, timeout=30, verify_ssl=verify_ssl)
