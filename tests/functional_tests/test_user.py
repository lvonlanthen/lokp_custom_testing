import pytest
from selenium.webdriver.support.ui import WebDriverWait

from .base import (
    createUrl, 
    doLogin, 
    findTextOnPage, 
    getEl,
)
from ..base import (
    FEEDBACK_FORM_ERROR,
    FEEDBACK_LOGIN_FAILED,
    FEEDBACK_USER_SETTINGS_UPDATED, 
    PASSWORD, 
    TITLE_USER_ACCOUNT_VIEW, 
)


@pytest.mark.functional
@pytest.mark.user
def test_change_password(testcase):
    """
    Test that the user can change his password.
    """
    newPwd = 'asdfasdf2'
    accountUrl = '/users/account'

    # Login first using the default password and go the user details page
    doLogin(testcase, redirect=createUrl(accountUrl))
    testcase.assertIn(TITLE_USER_ACCOUNT_VIEW, testcase.driver.title)

    # Try to enter two different password
    getEl(testcase, 'name', 'password').send_keys(newPwd)
    getEl(testcase, 'name', 'password-confirm').send_keys('This does not match')
    getEl(testcase, 'class_name', 'submit').click()
    WebDriverWait(testcase.driver, 10).until(
        lambda x: testcase.driver.find_element_by_css_selector('div.alert-error'))
    findTextOnPage(testcase, FEEDBACK_FORM_ERROR)

    # Enter a new password
    f1 = getEl(testcase, 'name', 'password')
    f1.clear()
    f1.send_keys(newPwd)
    f2 = getEl(testcase, 'name', 'password-confirm')
    f2.clear()
    f2.send_keys(newPwd)
    getEl(testcase, 'class_name', 'submit').click()
    WebDriverWait(testcase.driver, 10).until(
        lambda x: testcase.driver.find_element_by_css_selector('div.alert-success'))
    findTextOnPage(testcase, FEEDBACK_USER_SETTINGS_UPDATED)

    # Logout and try to log in with your old password
    testcase.driver.get(createUrl('/logout'))
    doLogin(testcase)
    WebDriverWait(testcase.driver, 10).until(
        lambda x: testcase.driver.find_element_by_css_selector('div.alert-error'))
    findTextOnPage(testcase, FEEDBACK_LOGIN_FAILED)

    # Login with the new password and change it back again
    doLogin(testcase, redirect=createUrl(accountUrl), password=newPwd)
    testcase.driver.get(createUrl(accountUrl))
    getEl(testcase, 'name', 'password').send_keys(PASSWORD)
    getEl(testcase, 'name', 'password-confirm').send_keys(PASSWORD)
    getEl(testcase, 'name', 'submit').click()
    WebDriverWait(testcase.driver, 10).until(
        lambda x: testcase.driver.find_element_by_css_selector('div.alert-success'))
    findTextOnPage(testcase, FEEDBACK_USER_SETTINGS_UPDATED)
