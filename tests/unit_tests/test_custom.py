import pytest
from mock import patch
from pyramid import testing

from lmkp.custom import (
    get_customization_name,
    get_customized_template_path,
)
from ..integration_tests.base import (
    LmkpTestCase,
)
from ..base import get_settings


@pytest.mark.usefixtures('app')
@pytest.mark.unittest
@pytest.mark.customization
class CustomGetCustomizedTemplatePath(LmkpTestCase):

    def setUp(self):
        self.request = testing.DummyRequest()
        settings = get_settings()
        self.config = testing.setUp(request=self.request, settings=settings)

    def tearDown(self):
        testing.tearDown()

    @patch('lmkp.custom.get_customization_name')
    def test_get_customized_template_path_calls_get_customized_name(
            self, mock_get_customization_name):
        get_customized_template_path(self.request, 'foo.mak')
        mock_get_customization_name.assert_called_once_with(
            request=self.request)

    @patch('lmkp.custom.get_customization_name')
    def test_get_customized_template_path_returns_path(
            self, mock_get_customization_name):
        mock_get_customization_name.return_value = 'foo'
        path = get_customized_template_path(self.request, 'foo.mak')
        self.assertEqual(path, 'lmkp:customization/foo/templates/foo.mak')


@pytest.mark.usefixtures('app')
@pytest.mark.unittest
@pytest.mark.customization
class CustomGetCustomizationName(LmkpTestCase):

    def setUp(self):
        self.request = testing.DummyRequest()
        self.settings = get_settings()
        self.config = testing.setUp(
            request=self.request, settings=self.settings)

    def tearDown(self):
        testing.tearDown()

    def test_get_customization_name_returns_name_from_request(self):
        name = get_customization_name(request=self.request)
        self.assertEqual(name, 'testing')

    def test_get_customization_name_returns_name_from_settings(self):
        name = get_customization_name(settings=self.settings)
        self.assertEqual(name, 'testing')

    def test_get_customization_name_raises_error_if_invalid_input(self):
        with self.assertRaises(Exception):
            get_customization_name(settings=object)

    def test_get_customization_name_raises_error_if_no_customization(self):
        settings = {'foo': 'bar'}
        with self.assertRaises(Exception):
            get_customization_name(settings=settings)

    def test_get_customization_name_raises_error_if_folder_not_found(self):
        settings = {'lmkp.customization': 'foo'}
        with self.assertRaises(Exception):
            get_customization_name(settings=settings)
