import os
import pytest
import shutil
from selenium import webdriver
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from selenium.webdriver.firefox.service import Service as FirefoxService
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.firefox import GeckoDriverManager

@pytest.fixture(scope="session")
def base_url():
    """Django app URL - auto-detects CI/Docker"""
    return os.environ.get("APP_BASE_URL", "http://localhost:8001").rstrip("/")

@pytest.fixture(params=["chrome", "firefox"], scope="class")
def selenium_driver(request, base_url):
    """Docker-ready Selenium driver - headless in CI"""
    browser = request.param
    options = None
    
    if browser == "chrome":
        options = ChromeOptions()
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        if os.environ.get("CI"):
            options.add_argument("--headless")
        service = ChromeService(ChromeDriverManager().install())
        driver = webdriver.Chrome(service=service, options=options)
    
    else:  # firefox
        options = FirefoxOptions()
        if os.environ.get("CI"):
            options.add_argument("--headless")
        service = FirefoxService(GeckoDriverManager().install())
        driver = webdriver.Firefox(service=service, options=options)
    
    driver.maximize_window()
    driver.implicitly_wait(10)
    driver.get(base_url)
    yield driver
    driver.quit()

@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """Screenshot on failure"""
    outcome = yield
    rep = outcome.get_result()
    if rep.when == "call" and rep.failed:
        driver = item.funcargs.get("selenium_driver")
        if driver:
            os.makedirs("screenshots", exist_ok=True)
            driver.save_screenshot(f"screenshots/{item.name}_{rep.when}.png")
