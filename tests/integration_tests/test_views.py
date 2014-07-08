import pytest
from unittest import TestCase

from .base import *


@pytest.mark.usefixtures('app')
@pytest.mark.integration
class ViewTests(TestCase):
        
    def test_root(self):
        """
        The root page (/) is available.
        """
        res = self.app.get('/')
        self.assertEqual(res.status_int, 200)
        self.assertIn(b'Land Observatory', res.body)