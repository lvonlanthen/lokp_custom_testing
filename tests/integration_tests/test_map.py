import pytest

from .base import (
    LmkpTestCase,
)


@pytest.mark.usefixtures('app')
@pytest.mark.integration
class MapTests(LmkpTestCase):

    def test_map_page_is_available(self):
        """
        The Map page is available.
        """
        res = self.app.get('/map')
        self.assertEqual(res.status_int, 200)
        self.assertIn(b'LOKP', res.body)

    def test_map_page_login_link_is_available(self):
        """
        The Map page shows a login link.
        """
        res = self.app.get('/map')
        self.assertIn(b'Login', res.body)
