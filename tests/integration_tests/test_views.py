import pytest

from .base import (
    LmkpTestCase
)


@pytest.mark.usefixtures('app')
@pytest.mark.integration
class ViewTests(LmkpTestCase):

    def test_root(self):
        """
        The root page (/) is available.
        """
        res = self.app.get('/')
        self.assertEqual(res.status_int, 200)
        self.assertIn(b'Land Observatory', res.body)
