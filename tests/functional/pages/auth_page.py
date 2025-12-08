from .base_page import BasePage
from selenium.webdriver.common.by import By

class AuthPage(BasePage):
    REGISTER_LINK = (By.LINK_TEXT, "Register")
    USERNAME = (By.NAME, "username")
    EMAIL = (By.NAME, "email")
    PASSWORD = (By.NAME, "password")
    SUBMIT_BTN = (By.XPATH, "//button[@type='submit']")
    
    def register_user(self, username, email, password):
        self.find_element(self.REGISTER_LINK).click()
        self.find_element(self.USERNAME).send_keys(username)
        self.find_element(self.EMAIL).send_keys(email)
        self.find_element(self.PASSWORD).send_keys(password)
        self.find_element(self.SUBMIT_BTN).click()
