import pytest

from .base import (
    LmkpTestCase
)
from ..base import USERNAME, PASSWORD


@pytest.mark.customization
@pytest.mark.usefixtures('app')
@pytest.mark.integration
class ViewTests(LmkpTestCase):

    customization_title = 'LOKP'

    def is_url_available(self, url, login=False, find=''):
        if login:
            self.app.post('/login', {
                'login': USERNAME,
                'password': PASSWORD,
                'form.submitted': 'true'
            })
        res = self.app.get(url)
        # If the route is being redirected, follow it.
        if res.status_int == 302:
            res = res.follow()
        self.assertEqual(res.status_int, 200)
        if find != '':
            self.assertIn(find, res.body)
        else:
            self.assertIn(self.customization_title, res.body)
        return res

    def test_root_view(self):
        self.is_url_available('/')

    def test_map_view(self):
        self.is_url_available('/map')

    def test_charts_view(self):
        self.is_url_available('/charts')

    def test_about_view(self):
        self.is_url_available('/about')

    def test_faq_view(self):
        self.is_url_available('/faq')

    def test_showcases_view(self):
        self.is_url_available('/showcases')

    def test_partners_view(self):
        self.is_url_available('/partners')

    def test_moderation_view(self):
        self.is_url_available('/moderation')

    def test_administration_view(self):
        self.is_url_available(
            '/administration', login=True, find='Administration')
