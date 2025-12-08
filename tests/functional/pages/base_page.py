import logging
from selenium.common.exceptions import (
    TimeoutException,
    NoSuchElementException,
    ElementClickInterceptedException,
    ElementNotInteractableException,
)
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

logger = logging.getLogger(__name__)


class BasePage:
    """Shared Selenium helpers with safe waits, interaction, and auth helpers."""

    # Generic auth locators – update to match your HTML
    LOGIN_LINK = (By.LINK_TEXT, "Login")
    LOGOUT_LINK = (By.LINK_TEXT, "Logout")
    USERNAME_INPUT = (By.NAME, "username")
    PASSWORD_INPUT = (By.NAME, "password")
    SUBMIT_BUTTON = (By.XPATH, "//button[@type='submit']")
    INCORRECT_CREDS_MSG = (By.XPATH, "//p[contains(text(),'Invalid username or password')]")

    def __init__(self, driver, timeout: int = 10):
        self.driver = driver
        self.timeout = timeout

    def _wait(self, condition):
        try:
            wait = WebDriverWait(self.driver, self.timeout)
            return wait.until(condition)
        except TimeoutException as e:
            logger.error(f"Timeout waiting for condition: {condition}", exc_info=True)
            raise

    def wait_visible(self, locator: tuple):
        try:
            return self._wait(EC.visibility_of_element_located(locator))
        except (TimeoutException, NoSuchElementException):
            logger.error(f"Element not visible: {locator}", exc_info=True)
            raise

    def wait_clickable(self, locator: tuple):
        try:
            return self._wait(EC.element_to_be_clickable(locator))
        except (TimeoutException, NoSuchElementException):
            logger.error(f"Element not clickable: {locator}", exc_info=True)
            raise

    def click(self, locator: tuple):
        try:
            element = self.wait_clickable(locator)
            try:
                element.click()
            except (ElementClickInterceptedException, ElementNotInteractableException):
                logger.warning(f"Normal click failed, trying JS click for: {locator}")
                self.driver.execute_script("arguments[0].click();", element)
        except Exception:
            logger.error(f"Click failed for locator: {locator}", exc_info=True)
            raise

    def type(self, locator: tuple, text: str, clear: bool = True):
        try:
            element = self.wait_visible(locator)
            if clear:
                element.clear()
            element.send_keys(text)
        except Exception:
            logger.error(f"Typing into element failed: {locator}", exc_info=True)
            raise

    def get_text(self, locator: tuple) -> str:
        try:
            element = self.wait_visible(locator)
            return element.text
        except Exception:
            logger.error(f"Get text failed for: {locator}", exc_info=True)
            raise

    def is_present(self, locator: tuple) -> bool:
        try:
            self._wait(EC.presence_of_element_located(locator))
            return True
        except TimeoutException:
            return False

    # -------- Auth helpers --------

    def login(self, base_url: str, username: str, password: str):
        """
        Navigate to login page and perform login.
        Assumes:
          - Login link is visible from the current page OR
          - Direct /login/ URL is available.
        """
        try:
            # Option A: direct URL (recommended for stability)
            self.driver.get(f"{base_url}/login/")

            # Option B (if you want link click instead):
            # self.click(self.LOGIN_LINK)

            self.type(self.USERNAME_INPUT, username)
            self.type(self.PASSWORD_INPUT, password)
            self.click(self.SUBMIT_BUTTON)
        except Exception:
            logger.error(
                f"Login failed for user '{username}' at {base_url}", exc_info=True
            )
            raise

    def logout(self, base_url: str = None):
        """
        Perform logout if logout link is present.
        Optionally navigate to home page first if base_url provided.
        """
        try:
            if base_url:
                self.driver.get(f"{base_url}/")

            if self.is_present(self.LOGOUT_LINK):
                self.click(self.LOGOUT_LINK)
            else:
                logger.warning("Logout link not present on the current page.")
        except Exception:
            logger.error("Logout failed.", exc_info=True)
            raise

    def assert_incorrect_login_message(self) -> bool:
        return self.is_present(self.INCORRECT_CREDS_MSG)