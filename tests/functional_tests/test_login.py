import pytest

from .base import (
    createUrl,
    getEl,
)
from ..base import(
    BUTTON_LOGIN,
    BUTTON_USERNAME,
    PASSWORD,
    TITLE_MAP_VIEW,
    USERNAME,
)


@pytest.mark.functional
@pytest.mark.login
def test_login(testcase):
    """
    Tests the login
    """

    # Make sure the user is not logged in. On Map View, the login link
    # should appear but no username.
    testcase.driver.get(createUrl('/logout'))
    testcase.assertIn(TITLE_MAP_VIEW, testcase.driver.title)
    getEl(testcase, 'link_text', BUTTON_USERNAME, inverse=True)
    getEl(testcase, 'link_text', BUTTON_LOGIN)

    # Login
    testcase.driver.get(createUrl('/login'))
    loginfield = testcase.driver.find_element_by_name('login') #
    loginfield.send_keys(USERNAME)
    passwordfield = testcase.driver.find_element_by_name('password')
    passwordfield.send_keys(PASSWORD)
    btn = testcase.driver.find_element_by_name('form.submitted')
    btn.click()

    # Check that the user is now logged in. We should be back on the Map
    # View, with the username showing instead of the login link.
    testcase.assertIn(TITLE_MAP_VIEW, testcase.driver.title)
    getEl(testcase, 'link_text', BUTTON_USERNAME)
    getEl(testcase, 'link_text', BUTTON_LOGIN, inverse=True)
    