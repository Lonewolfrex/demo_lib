from .base_page import BasePage
from selenium.webdriver.common.by import By


class HomePage(BasePage):
    BOOKS_TAB = (By.ID, "books-tab")
    DONATE_BTN = (By.XPATH, "//button[contains(text(), 'Donate')]")
    RENT_BTN = (By.XPATH, "//button[contains(text(), 'Rent')]")
    USER_PROFILE_XPATH = "//div//button[contains(text(), '{username}')]"
    LOGOUT_XPATH = (
        "//div//button[contains(text(), '{username}')]/..//div//a[@href='/logout/']"
    )

    def click_donate(self):
        self.find_element(self.DONATE_BTN).click()

    def user_profile_locator(self, username: str):
        xpath = self.USER_PROFILE_XPATH.format(username=username)
        return (By.XPATH, xpath)

    def logout_link_locator(self, username: str):
        xpath = self.LOGOUT_XPATH.format(username=username)
        return (By.XPATH, xpath)

    def click_user_profile(self, username: str):
        locator = self.user_profile_locator(username)
        self.click(locator)

    def logout(self, username: str):
        self.click_user_profile(username=username)
        logout_locator = self.logout_link_locator(username=username)
        self.click(logout_locator)
        
    def assert_logged_in(self, username: str) -> bool:
        locator = self.user_profile_locator(username=username)
        return self.is_present(locator)