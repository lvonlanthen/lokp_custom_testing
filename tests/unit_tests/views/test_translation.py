import pytest
from mock import patch

from ...integration_tests.base import (
    LmkpTestCase,
)
from lmkp.views.translation import get_translated_keys


@pytest.mark.unittest
@pytest.mark.views
class TranslationGetTranslatedKeysTests(LmkpTestCase):

    @patch('lmkp.views.translation.validate_item_type')
    def test_get_translated_keys_calls_validate_item_type(
            self, mock_validate_item_type):
        get_translated_keys('a', [], 'en')
        mock_validate_item_type.assert_called_once_with('a')

    def test_get_translated_keys_returns_empty_array_if_no_keys(self):
        keys = get_translated_keys('a', [], 'en')
        self.assertEqual(keys, [])
