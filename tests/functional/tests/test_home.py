# tests/functional_tests/tests/test_auth.py
import pytest
from pages.base_page import BasePage
from pages.home_page import HomePage

class TestAuth:
    @pytest.mark.usefixtures("selenium_driver")
    def test_login_logout(self, selenium_driver, base_url):
        base = BasePage(selenium_driver)
        home = HomePage(selenium_driver)
        base.login(base_url, "testuser3", "Password@3")
        assert home.assert_logged_in("testuser3"), "User profile not visible; login may have failed."
        home.logout("testuser3")

    @pytest.mark.usefixtures("selenium_driver")
    def test_incorrectlogin_1(self, selenium_driver, base_url):
        base = BasePage(selenium_driver)
        home = HomePage(selenium_driver)
        base.login(base_url, "incorrect_username", "Password@3")
        assert base.assert_incorrect_login_message(), "Incorrect login message not displayed."

    @pytest.mark.usefixtures("selenium_driver")
    def test_incorrectlogin_2(self, selenium_driver, base_url):
        base = BasePage(selenium_driver)
        home = HomePage(selenium_driver)
        base.login(base_url, "testuser3", "IncorrectPassword")
        assert base.assert_incorrect_login_message(), "Incorrect login message not displayed."

