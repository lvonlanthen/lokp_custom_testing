import pytest

from .base import LmkpFunctionalTestCase
from ..base import(
    BUTTON_LOGIN,
    BUTTON_USERNAME,
    PASSWORD,
    TITLE_MAP_VIEW,
    USERNAME,
)


@pytest.mark.usefixtures('app_functional')
@pytest.mark.functional
@pytest.mark.login
class LoginTests(LmkpFunctionalTestCase):

    def test_login(self):
        """
        Tests the login
        """

        # Make sure the user is not logged in. On Map View, the login link
        # should appear but no username.
        self.driver.get(self.url('/logout'))
        self.assertIn(TITLE_MAP_VIEW, self.driver.title)
        self.el('link_text', BUTTON_USERNAME, inverse=True)
        self.el('link_text', BUTTON_LOGIN)

        # Login
        self.driver.get(self.url('/login'))
        loginfield = self.el('name', 'login')
        loginfield.send_keys(USERNAME)
        passwordfield = self.el('name', 'password')
        passwordfield.send_keys(PASSWORD)
        btn = self.el('name', 'form.submitted')
        btn.click()

        # Check that the user is now logged in. We should be back on the Map
        # View, with the username showing instead of the login link.
        self.assertIn(TITLE_MAP_VIEW, self.driver.title)
        self.el('link_text', BUTTON_USERNAME)
        self.el('link_text', BUTTON_LOGIN, inverse=True)
