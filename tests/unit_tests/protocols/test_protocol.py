import pytest
from mock import patch
from pyramid import testing
from sqlalchemy.sql import expression

from lmkp.protocols.protocol import Protocol
from ...integration_tests.base import (
    LmkpTestCase,
)
from ...base import get_settings
from lmkp.models.database_objects import Activity


@pytest.mark.usefixtures('app')
@pytest.mark.unittest
@pytest.mark.protocol
class ProtocolsProtocolGetTranslationsTest(LmkpTestCase):

    def setUp(self):
        self.request = testing.DummyRequest()
        settings = get_settings()
        self.config = testing.setUp(request=self.request, settings=settings)
        self.protocol = Protocol(self.request)

    def tearDown(self):
        testing.tearDown()

    @patch('lmkp.protocols.protocol.validate_item_type')
    def test_get_translations_calls_validate_item_type(
            self, mock_validate_item_type):
        self.protocol.get_translations('a')
        mock_validate_item_type.assert_called_once_with('a')

    @patch('lmkp.protocols.protocol.get_current_locale')
    def test_get_translations_calls_get_current_locale(
            self, mock_get_current_locale):
        self.protocol.get_translations('a')
        mock_get_current_locale.assert_called_once_with(self.request)

    def test_get_translations_returns_subqueries(self):
        key_query, value_query = self.protocol.get_translations('a')
        self.assertIsInstance(key_query, expression.Alias)
        self.assertIsInstance(value_query, expression.Alias)


@pytest.mark.usefixtures('app')
@pytest.mark.unittest
@pytest.mark.protocol
class ProtocolsProtocolGetOrderTest(LmkpTestCase):

    def setUp(self):
        self.request = testing.DummyRequest()
        settings = get_settings()
        self.config = testing.setUp(request=self.request, settings=settings)
        self.protocol = Protocol(self.request)

    def tearDown(self):
        testing.tearDown()

    @patch('lmkp.protocols.protocol.validate_item_type')
    def test_get_order_calls_validate_item_type(
            self, mock_validate_item_type):
        self.protocol.get_order('a')
        mock_validate_item_type.assert_called_once_with('a')

    @patch('lmkp.protocols.protocol.get_current_order_key')
    def test_get_order_calls_get_current_order_key(
            self, mock_get_current_order_key):
        mock_get_current_order_key.return_value = 'foo'
        self.protocol.get_order('a')
        mock_get_current_order_key.assert_called_once_with(self.request)

    @patch('lmkp.protocols.protocol.get_current_order_key')
    def test_get_order_returns_subquery(self, mock_get_current_order_key):
        mock_get_current_order_key.return_value = 'foo'
        order = self.protocol.get_order('a')
        params = order.compile().params
        self.assertEqual(len(params), 1)
        self.assertEqual(params.get('key_1'), 'foo')


@pytest.mark.unittest
@pytest.mark.protocol
class ProtocolsProtocolGetAttributeFiltersTest(LmkpTestCase):

    def setUp(self):
        self.request = testing.DummyRequest()
        settings = get_settings()
        self.config = testing.setUp(request=self.request, settings=settings)
        self.protocol = Protocol(self.request)

    def tearDown(self):
        testing.tearDown()

    def test_get_attribute_filters_returns_empty(self):
        a_filters, sh_filters = self.protocol.get_attribute_filters()
        self.assertEqual(a_filters, [])
        self.assertEqual(sh_filters, [])

    def test_get_attribute_filters_returns_a_filter(self):
        self.request.params = {'a__foo__like': 'bar'}
        a_filters, sh_filters = self.protocol.get_attribute_filters()
        self.assertEqual(len(a_filters), 1)
        filter = a_filters[0]
        params = filter.whereclause.compile().params
        self.assertEqual(len(params), 2)
        self.assertEqual(params.get('key_1'), 'foo')
        self.assertEqual(params.get('value_1'), 'bar')
        self.assertEqual(sh_filters, [])

    def test_get_attribute_filters_returns_a_filters(self):
        self.request.params = {
            'a__foo__like': 'bar',
            'a__abc__ilike': 'xyz'
        }
        a_filters, sh_filters = self.protocol.get_attribute_filters()
        self.assertEqual(len(a_filters), 2)
        filter_1 = a_filters[0]
        params_1 = filter_1.whereclause.compile().params
        self.assertEqual(len(params_1), 2)
        self.assertEqual(params_1.get('key_1'), 'abc')
        self.assertEqual(params_1.get('value_1'), 'xyz')
        filter_2 = a_filters[1]
        params_2 = filter_2.whereclause.compile().params
        self.assertEqual(len(params_2), 2)
        self.assertEqual(params_2.get('key_1'), 'foo')
        self.assertEqual(params_2.get('value_1'), 'bar')
        self.assertEqual(sh_filters, [])

    def test_get_attribute_filters_returns_sh_filter(self):
        self.request.params = {'sh__foo__like': 'bar'}
        a_filters, sh_filters = self.protocol.get_attribute_filters()
        self.assertEqual(len(sh_filters), 1)
        filter = sh_filters[0]
        params = filter.whereclause.compile().params
        self.assertEqual(len(params), 2)
        self.assertEqual(params.get('key_1'), 'foo')
        self.assertEqual(params.get('value_1'), 'bar')
        self.assertEqual(a_filters, [])

    def test_get_attribute_filters_returns_sh_filters(self):
        self.request.params = {
            'sh__foo__like': 'bar',
            'sh__abc__ilike': 'xyz'
        }
        a_filters, sh_filters = self.protocol.get_attribute_filters()
        self.assertEqual(len(sh_filters), 2)
        filter_1 = sh_filters[0]
        params_1 = filter_1.whereclause.compile().params
        self.assertEqual(len(params_1), 2)
        self.assertEqual(params_1.get('key_1'), 'foo')
        self.assertEqual(params_1.get('value_1'), 'bar')
        filter_2 = sh_filters[1]
        params_2 = filter_2.whereclause.compile().params
        self.assertEqual(len(params_2), 2)
        self.assertEqual(params_2.get('key_1'), 'abc')
        self.assertEqual(params_2.get('value_1'), 'xyz')
        self.assertEqual(a_filters, [])

    def test_get_attribute_filters_ignores_other_params(self):
        self.request.params = {
            'c__foo__like': 'bar_1',
            'a__foo__like': 'bar_2',
            'foo': 'bar_3'
        }
        a_filters, sh_filters = self.protocol.get_attribute_filters()
        self.assertEqual(len(a_filters), 1)
        filter = a_filters[0]
        params = filter.whereclause.compile().params
        self.assertEqual(len(params), 2)
        self.assertEqual(params.get('key_1'), 'foo')
        self.assertEqual(params.get('value_1'), 'bar_2')
        self.assertEqual(sh_filters, [])

    def test_get_attribute_filters_equals(self):
        self.request.params = {
            'a__foo__eq': '20'
        }
        a_filters, sh_filters = self.protocol.get_attribute_filters()
        self.assertEqual(len(a_filters), 1)
        filter = a_filters[0]
        params = filter.whereclause.compile().params
        self.assertEqual(len(params), 3)
        self.assertEqual(params.get('key_1'), 'foo')
        self.assertEqual(params.get('param_1'), '20')
        self.assertEqual(params.get('param_2'), '20')
        self.assertEqual(sh_filters, [])

    def test_get_attribute_filters_nonequals(self):
        self.request.params = {
            'a__foo__ne': '20'
        }
        a_filters, sh_filters = self.protocol.get_attribute_filters()
        self.assertEqual(len(a_filters), 1)
        filter = a_filters[0]
        params = filter.whereclause.compile().params
        self.assertEqual(len(params), 2)
        self.assertEqual(params.get('key_1'), 'foo')
        self.assertEqual(params.get('param_1'), '20')
        self.assertEqual(sh_filters, [])

    def test_get_attribute_filters_multiple_params(self):
        self.request.params = {
            'a__foo__like': 'foo,bar'
        }
        a_filters, sh_filters = self.protocol.get_attribute_filters()
        self.assertEqual(len(a_filters), 2)
        filter1 = a_filters[0]
        params1 = filter1.whereclause.compile().params
        self.assertEqual(len(params1), 2)
        self.assertEqual(params1.get('key_1'), 'foo')
        self.assertEqual(params1.get('value_1'), 'foo')
        filter2 = a_filters[1]
        params2 = filter2.whereclause.compile().params
        self.assertEqual(len(params2), 2)
        self.assertEqual(params2.get('key_1'), 'foo')
        self.assertEqual(params2.get('value_1'), 'bar')
        self.assertEqual(sh_filters, [])

    def test_get_attribute_filters_handles_invalid_number_values(self):
        self.request.params = {
            'a__foo__eq': 'bar'
        }
        a_filters, sh_filters = self.protocol.get_attribute_filters()
        self.assertEqual(len(a_filters), 1)
        filter = a_filters[0]
        params = filter.whereclause.compile().params
        self.assertEqual(len(params), 1)
        self.assertEqual(params.get('key_1'), 'foo')
        self.assertIsNone(params.get('param_1'))
        self.assertIsNone(params.get('param_2'))
        self.assertEqual(sh_filters, [])

    def test_get_attribute_filters_handles_invalid_operator(self):
        self.request.params = {
            'a__foo__foo': 'bar'
        }
        a_filters, sh_filters = self.protocol.get_attribute_filters()
        self.assertEqual(len(a_filters), 1)
        filter = a_filters[0]
        params = filter.whereclause.compile().params
        self.assertEqual(len(params), 1)
        self.assertEqual(params.get('key_1'), 'foo')
        self.assertIsNone(params.get('param_1'))
        self.assertIsNone(params.get('param_2'))
        self.assertEqual(sh_filters, [])

    def test_get_attribute_filters_handles_invalid_prefix(self):
        self.request.params = {
            'foo__foo__foo': 'bar'
        }
        a_filters, sh_filters = self.protocol.get_attribute_filters()
        self.assertEqual(a_filters, [])
        self.assertEqual(sh_filters, [])

    @patch('lmkp.protocols.protocol.get_current_attribute_filters')
    def test_get_attribute_filters_calls_get_current_filters(
            self, mock_get_current_filters):
        a_filters, sh_filters = self.protocol.get_attribute_filters()
        mock_get_current_filters.assert_called_once_with(self.request)


@pytest.mark.usefixtures('app')
@pytest.mark.unittest
@pytest.mark.protocol
class ProtocolsProtocolGetStatusFilterTest(LmkpTestCase):

    def setUp(self):
        self.request = testing.DummyRequest()
        settings = get_settings()
        self.config = testing.setUp(request=self.request, settings=settings)
        self.protocol = Protocol(self.request)

    def tearDown(self):
        testing.tearDown()

    @patch('lmkp.protocols.protocol.get_status_parameter')
    def test_get_status_filter_calls_get_status_parameter(
            self, mock_get_status_parameter):
        self.protocol.get_status_filter(Activity)
        mock_get_status_parameter.assert_called_once_with(self.request)

    @patch('lmkp.protocols.protocol.get_user_privileges')
    def test_get_status_filter_calls_get_user_privileges(
            self, mock_get_user_privileges):
        mock_get_user_privileges.return_value = (None, None)
        self.protocol.get_status_filter(Activity)
        mock_get_user_privileges.assert_called_once_with(self.request)

    def test_default_status(self):
        status_filter = self.protocol.get_status_filter(Activity)
        params = status_filter.compile().params
        self.assertEqual(len(params), 1)
        self.assertEqual(params.get('fk_status_1'), 2)

    def test_handle_single_status(self):
        self.request.params = {'status': 'inactive'}
        status_filter = self.protocol.get_status_filter(Activity)
        params = status_filter.compile().params
        self.assertEqual(len(params), 1)
        self.assertEqual(params.get('fk_status_1'), 3)

    def test_handle_multiple_statii(self):
        self.request.params = {'status': 'active,inactive'}
        status_filter = self.protocol.get_status_filter(Activity)
        params = status_filter.compile().params
        self.assertEqual(len(params), 2)
        self.assertEqual(params.get('fk_status_1'), 2)
        self.assertEqual(params.get('fk_status_2'), 3)

    def test_remove_one_invalid_status(self):
        self.request.params = {'status': 'foo,inactive'}
        status_filter = self.protocol.get_status_filter(Activity)
        params = status_filter.compile().params
        self.assertEqual(len(params), 1)
        self.assertEqual(params.get('fk_status_1'), 3)

    def test_remove_all_invalid_statii(self):
        self.request.params = {'status': 'foo,bar'}
        status_filter = self.protocol.get_status_filter(Activity)
        params = status_filter.compile().params
        self.assertEqual(len(params), 1)
        self.assertEqual(params.get('fk_status_1'), 2)

    def test_public_cannot_see_pending_and_edited(self):
        self.request.params = {'status': 'pending,active,edited'}
        status_filter = self.protocol.get_status_filter(Activity)
        params = status_filter.compile().params
        self.assertEqual(len(params), 1)
        self.assertEqual(params.get('fk_status_1'), 2)

    @patch('lmkp.protocols.protocol.get_user_privileges')
    def test_moderators_can_see_pending_and_edited(
            self, mock_get_user_privileges):
        self.request.params = {'status': 'pending,active,edited'}
        mock_get_user_privileges.return_value = (True, True)
        status_filter = self.protocol.get_status_filter(Activity)
        params = status_filter.compile().params
        self.assertEqual(len(params), 3)
        self.assertEqual(params.get('fk_status_1'), 1)
        self.assertEqual(params.get('fk_status_2'), 2)
        self.assertEqual(params.get('fk_status_3'), 6)
