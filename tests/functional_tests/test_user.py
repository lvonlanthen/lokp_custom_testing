import pytest
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from unittest import TestCase

from .base import createUrl, doLogin, findTextOnPage, getEl
from ..base import TITLE_USER_ACCOUNT_VIEW, PASSWORD, FEEDBACK_FORM_ERROR, FEEDBACK_USER_SETTINGS_UPDATED, FEEDBACK_LOGIN_FAILED

@pytest.mark.functional
@pytest.mark.user
class UserTests(TestCase):
    
    def setUp(self):
        self.driver = webdriver.Firefox()
        
    def tearDown(self):
        self.driver.quit()
    
    @pytest.mark.test
    def test_change_password(self):
        """
        Test that the user can change his password.
        """
        newPwd = 'asdfasdf2'
        accountUrl = '/users/account'
        
        # Login first using the default password and go the user details page
        doLogin(self, redirect=createUrl(accountUrl))
        self.assertIn(TITLE_USER_ACCOUNT_VIEW, self.driver.title)
        
        # Try to enter two different password
        getEl(self, 'name', 'password').send_keys(newPwd)
        getEl(self, 'name', 'password-confirm').send_keys('This does not match')
        getEl(self, 'class_name', 'submit').click()
        WebDriverWait(self.driver, 10).until(
            lambda x: self.driver.find_element_by_css_selector('div.alert-error'))
        findTextOnPage(self, FEEDBACK_FORM_ERROR)
        
        # Enter a new password
        f1 = getEl(self, 'name', 'password')
        f1.clear()
        f1.send_keys(newPwd)
        f2 = getEl(self, 'name', 'password-confirm')
        f2.clear()
        f2.send_keys(newPwd)
        getEl(self, 'class_name', 'submit').click()
        WebDriverWait(self.driver, 10).until(
            lambda x: self.driver.find_element_by_css_selector('div.alert-success'))
        findTextOnPage(self, FEEDBACK_USER_SETTINGS_UPDATED)
        
        # Logout and try to log in with your old password
        self.driver.get(createUrl('/logout'))
        doLogin(self)
        WebDriverWait(self.driver, 10).until(
            lambda x: self.driver.find_element_by_css_selector('div.alert-error'))
        findTextOnPage(self, FEEDBACK_LOGIN_FAILED)
        
        # Login with the new password and change it back again
        doLogin(self, redirect=createUrl(accountUrl), password=newPwd)
        self.driver.get(createUrl(accountUrl))
        getEl(self, 'name', 'password').send_keys(PASSWORD)
        getEl(self, 'name', 'password-confirm').send_keys(PASSWORD)
        getEl(self, 'name', 'submit').click()
        WebDriverWait(self.driver, 10).until(
            lambda x: self.driver.find_element_by_css_selector('div.alert-success'))
        findTextOnPage(self, FEEDBACK_USER_SETTINGS_UPDATED)