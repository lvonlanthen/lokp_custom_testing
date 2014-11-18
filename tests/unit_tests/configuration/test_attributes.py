import pytest
from mock import patch
from pyramid import testing

from lmkp.configuration.attributes import (
    get_attributes_configuration,
)
from ...integration_tests.base import (
    LmkpTestCase,
)
from ...base import get_settings


@pytest.mark.usefixtures('app')
@pytest.mark.unittest
@pytest.mark.configuration
class GetAttributesConfigurationTest(LmkpTestCase):

    def setUp(self):
        self.request = testing.DummyRequest()
        settings = get_settings()
        self.config = testing.setUp(request=self.request, settings=settings)

    def tearDown(self):
        testing.tearDown()

    @patch('lmkp.configuration.attributes.validate_item_type')
    def test_get_attr_configuration_calls_validate_item_type(
            self, mock_validate_item_type):
        get_attributes_configuration(self.request, 'activities')
        mock_validate_item_type.assert_called_once_with('activities')

    @patch('lmkp.configuration.attributes.get_current_locale')
    def test_get_attr_configuration_calls_get_current_locale(
            self, mock_get_current_locale):
        get_attributes_configuration(self.request, 'activities')
        mock_get_current_locale.assert_called_once_with(self.request)

    @patch('lmkp.configuration.attributes.get_db_keys')
    @patch('lmkp.configuration.attributes.get_current_locale')
    def test_get_attr_configuration_calls_get_db_keys(
            self, mock_get_current_locale, mock_get_db_keys):
        mock_get_current_locale.return_value = 'foo'
        get_attributes_configuration(self.request, 'activities')
        mock_get_db_keys.assert_called_once_with('a', 'foo')


@pytest.mark.usefixtures('app')
@pytest.mark.unittest
@pytest.mark.configuration
class GetDbKeysTest(LmkpTestCase):

    def setUp(self):
        self.request = testing.DummyRequest()
        settings = get_settings()
        self.config = testing.setUp(request=self.request, settings=settings)

    def tearDown(self):
        testing.tearDown()

    # @patch('lmkp.configuration.attributes.validate_item_type')
    # def test_get_attr_configuration_calls_validate_item_type(
    #         self, mock_validate_item_type):
    #     get_attributes_configuration(self.request, 'activities')
    #     mock_validate_item_type.assert_called_once_with('activities')
