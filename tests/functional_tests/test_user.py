import pytest
from selenium.webdriver.support.ui import WebDriverWait

from .base import LmkpFunctionalTestCase
from ..base import (
    FEEDBACK_FORM_ERROR,
    FEEDBACK_LOGIN_FAILED,
    FEEDBACK_USER_SETTINGS_UPDATED,
    PASSWORD,
    TITLE_USER_ACCOUNT_VIEW,
)


@pytest.mark.usefixtures('app_functional')
@pytest.mark.functional
@pytest.mark.user
class UserTests(LmkpFunctionalTestCase):

    def test_change_password(self):
        """
        Test that the user can change his password.
        """
        new_pwd = 'asdfasdf2'
        account_url = '/users/account'

        # Login first using the default password and go the user details page
        self.login(redirect=self.url(account_url))
        self.assertIn(TITLE_USER_ACCOUNT_VIEW, self.driver.title)

        # Try to enter two different password
        self.el('name', 'password').send_keys(new_pwd)
        self.el('name', 'password-confirm').send_keys('This does not match')
        self.el('class_name', 'submit').click()
        WebDriverWait(self.driver, 10).until(
            lambda x: self.driver.find_element_by_css_selector(
                'div.alert-error'))
        self.find_text(FEEDBACK_FORM_ERROR)

        # Enter a new password
        f1 = self.el('name', 'password')
        f1.clear()
        f1.send_keys(new_pwd)
        f2 = self.el('name', 'password-confirm')
        f2.clear()
        f2.send_keys(new_pwd)
        self.el('class_name', 'submit').click()
        WebDriverWait(self.driver, 10).until(
            lambda x: self.driver.find_element_by_css_selector(
                'div.alert-success'))
        self.find_text(FEEDBACK_USER_SETTINGS_UPDATED)

        # Logout and try to log in with your old password
        self.driver.get(self.url('/logout'))
        self.login(self)
        WebDriverWait(self.driver, 10).until(
            lambda x: self.driver.find_element_by_css_selector(
                'div.alert-error'))
        self.find_text(FEEDBACK_LOGIN_FAILED)

        # Login with the new password and change it back again
        self.login(redirect=self.url(account_url), password=new_pwd)
        self.driver.get(self.url(account_url))
        self.el('name', 'password').send_keys(PASSWORD)
        self.el('name', 'password-confirm').send_keys(PASSWORD)
        self.el('name', 'submit').click()
        WebDriverWait(self.driver, 10).until(
            lambda x: self.driver.find_element_by_css_selector(
                'div.alert-success'))
        self.find_text(FEEDBACK_USER_SETTINGS_UPDATED)
