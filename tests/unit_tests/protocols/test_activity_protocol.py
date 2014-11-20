import pytest
from geoalchemy.functions import functions as geofunctions
from mock import patch
from pyramid import testing
from sqlalchemy.orm.query import Query

from lmkp.protocols.activity_protocol import ActivityProtocol
from ...integration_tests.base import (
    LmkpTestCase,
)
from ...base import get_settings

from lmkp.models.meta import DBSession as Session
from lmkp.models.database_objects import A_Key, A_Value


@pytest.mark.unittest
@pytest.mark.protocol
class ProtocolsActivityProtocolQueryMany(LmkpTestCase):

    def setUp(self):
        self.request = testing.DummyRequest()
        settings = get_settings()
        self.config = testing.setUp(request=self.request, settings=settings)
        self.activity_protocol = ActivityProtocol(self.request)

    def tearDown(self):
        testing.tearDown()

    @patch(
        'lmkp.protocols.activity_protocol.ActivityProtocol.get_translations')
    @patch(
        'lmkp.protocols.activity_protocol.ActivityProtocol.get_profile_filter')
    def test_query_many_calls_get_translations(
            self, mock_get_profile_filter, mock_get_translations):
        mock_get_profile_filter.return_value = None
        mock_get_translations.return_value = Session.query(
            A_Key.fk_key.label("key_original_id"),
            A_Key.key.label("key_translated")
        ).subquery(), Session.query(
            A_Value.fk_value.label("value_original_id"),
            A_Value.value.label("value_translated")
        ).subquery()
        rel_act = self.activity_protocol.get_relevant_activities_many()
        self.activity_protocol.query_many(rel_act, return_count=False)
        mock_get_translations.assert_called_once_with('a')


@pytest.mark.unittest
@pytest.mark.protocol
class ProtocolsActivityProtocolReadMany(LmkpTestCase):

    def setUp(self):
        self.request = testing.DummyRequest()
        settings = get_settings()
        self.config = testing.setUp(request=self.request, settings=settings)
        self.activity_protocol = ActivityProtocol(self.request)

    def tearDown(self):
        testing.tearDown()

    @patch(
        'lmkp.protocols.activity_protocol.ActivityProtocol.'
        'get_relevant_activities_many')
    @patch('lmkp.protocols.activity_protocol.ActivityProtocol.query_many')
    @patch(
        'lmkp.protocols.activity_protocol.ActivityProtocol.'
        '_query_to_activities')
    def test_read_many_calls_get_relevant_activities_many(
            self, mock_query_to_activities, mock_query_many,
            mock_get_relevant_activities_many):
        mock_query_many.return_value = (None, 0)
        mock_query_to_activities.return_value = []
        self.activity_protocol.read_many(self.request)
        mock_get_relevant_activities_many.assert_called_once_with(
            public_query=True)

    @patch(
        'lmkp.protocols.activity_protocol.get_current_involvement_details')
    @patch(
        'lmkp.protocols.activity_protocol.ActivityProtocol.'
        'get_relevant_activities_many')
    @patch('lmkp.protocols.activity_protocol.ActivityProtocol.query_many')
    @patch(
        'lmkp.protocols.activity_protocol.ActivityProtocol.'
        '_query_to_activities')
    def test_read_many_calls_get_current_involvement_details(
            self, mock_query_to_activities, mock_query_many,
            mock_get_relevant_activities_many,
            mock_get_current_involvement_details):
        mock_query_many.return_value = (None, 0)
        mock_query_to_activities.return_value = []
        mock_get_relevant_activities_many.return_value = None
        self.activity_protocol.read_many(self.request)
        mock_get_current_involvement_details.assert_called_once_with(
            self.request)


@pytest.mark.unittest
@pytest.mark.protocol
class ProtocolsActivityProtocolGetRelevantActivitiesMany(LmkpTestCase):

    def setUp(self):
        self.request = testing.DummyRequest()
        settings = get_settings()
        self.config = testing.setUp(request=self.request, settings=settings)
        self.activity_protocol = ActivityProtocol(self.request)

    def tearDown(self):
        testing.tearDown()

    @patch('lmkp.protocols.activity_protocol.get_user_privileges')
    @patch(
        'lmkp.protocols.activity_protocol.ActivityProtocol.get_profile_filter')
    def test_get_relevant_activities_many_calls_get_user_privileges(
            self, mock_get_profile_filter, mock_get_user_privileges):
        mock_get_user_privileges.return_value = (None, None)
        mock_get_profile_filter.return_value = None
        self.activity_protocol.get_relevant_activities_many()
        mock_get_user_privileges.assert_called_once_with(self.request)

    @patch(
        'lmkp.protocols.activity_protocol.ActivityProtocol.'
        'get_attribute_filters')
    @patch(
        'lmkp.protocols.activity_protocol.ActivityProtocol.get_profile_filter')
    def test_get_relevant_activities_many_calls_get_attribute_filters(
            self, mock_get_profile_filter, mock_get_attribute_filters):
        mock_get_attribute_filters.return_value = ([], [])
        mock_get_profile_filter.return_value = None
        self.activity_protocol.get_relevant_activities_many()
        mock_get_attribute_filters.assert_called_once_with()

    @patch(
        'lmkp.protocols.activity_protocol.get_current_logical_filter_operator')
    @patch(
        'lmkp.protocols.activity_protocol.ActivityProtocol.get_profile_filter')
    def test_get_relevant_activities_many_calls_get_logical_filter_operator(
            self, mock_get_profile_filter, mock_get_logical_filter_operator):
        self.request.params = {'a__foo__like': 'bar'}
        mock_get_profile_filter.return_value = None
        self.activity_protocol.get_relevant_activities_many()
        mock_get_logical_filter_operator.assert_called_once_with(self.request)

    @patch('lmkp.protocols.activity_protocol.ActivityProtocol.get_order')
    @patch(
        'lmkp.protocols.activity_protocol.ActivityProtocol.get_profile_filter')
    def test_get_relevant_activities_many_calls_get_order(
            self, mock_get_profile_filter, mock_get_order):
        mock_get_profile_filter.return_value = None
        with self.assertRaises(UnboundLocalError):
            self.activity_protocol.get_relevant_activities_many()
        mock_get_order.assert_called_once_with('a')

    @patch('lmkp.protocols.activity_protocol.get_status_parameter')
    @patch(
        'lmkp.protocols.activity_protocol.ActivityProtocol.get_profile_filter')
    def test_get_relevant_activities_many_calls_get_status_parameter(
            self, mock_get_profile_filter, mock_get_status_parameter):
        mock_get_profile_filter.return_value = None
        self.activity_protocol.get_relevant_activities_many()
        mock_get_status_parameter.assert_called_once_with(self.request)

    @patch(
        'lmkp.protocols.activity_protocol.ActivityProtocol.get_profile_filter')
    def test_get_relevant_activities_many_calls_get_profile_filter(
            self, mock_get_profile_filter):
        mock_get_profile_filter.return_value = None
        self.activity_protocol.get_relevant_activities_many()
        mock_get_profile_filter.assert_called_once_with()

    @patch('lmkp.protocols.activity_protocol.ActivityProtocol.get_bbox_filter')
    @patch(
        'lmkp.protocols.activity_protocol.ActivityProtocol.get_profile_filter')
    def test_get_relevant_activities_many_calls_get_bbox_filter(
            self, mock_get_profile_filter, mock_get_box_filter):
        mock_get_box_filter.return_value = None
        mock_get_profile_filter.return_value = None
        self.activity_protocol.get_relevant_activities_many()
        mock_get_box_filter.assert_called_once_with(cookies=True)

    @patch('lmkp.protocols.activity_protocol.get_current_order_direction')
    @patch(
        'lmkp.protocols.activity_protocol.ActivityProtocol.get_profile_filter')
    def test_get_relevant_activities_many_calls_get_current_order_direction(
            self, mock_get_profile_filter, mock_get_order_direction):
        mock_get_profile_filter.return_value = None
        self.activity_protocol.get_relevant_activities_many()
        mock_get_order_direction.assert_called_once_with(self.request)

    @patch('lmkp.protocols.activity_protocol.get_current_order_direction')
    @patch(
        'lmkp.protocols.activity_protocol.ActivityProtocol.get_profile_filter')
    def test_get_relevant_activities_many_returns_fooo(
            self, mock_get_profile_filter, mock_get_order_direction):
        mock_get_profile_filter.return_value = None
        rel_act = self.activity_protocol.get_relevant_activities_many()
        self.assertIsInstance(rel_act, Query)


@pytest.mark.unittest
@pytest.mark.protocol
class ProtocolsActivityProtocolGetBboxFilter(LmkpTestCase):

    def setUp(self):
        self.request = testing.DummyRequest()
        settings = get_settings()
        self.config = testing.setUp(request=self.request, settings=settings)
        self.activity_protocol = ActivityProtocol(self.request)

    def tearDown(self):
        testing.tearDown()

    @patch('lmkp.protocols.activity_protocol.get_bbox_parameters')
    def test_get_bbox_filter_calls_get_bbox_parameters(
            self, mock_get_bbox_parameters):
        mock_get_bbox_parameters.return_value = None, None
        self.activity_protocol.get_bbox_filter(cookies=False)
        mock_get_bbox_parameters.assert_called_once_with(
            self.request, cookies=False)

    @patch('lmkp.protocols.activity_protocol.validate_bbox')
    @patch('lmkp.protocols.activity_protocol.get_bbox_parameters')
    def test_get_bbox_filter_calls_validate_bbox(
            self, mock_get_bbox_parameters, mock_validate_bbox):
        mock_get_bbox_parameters.return_value = 'bbox', 'epsg'
        self.activity_protocol.get_bbox_filter(cookies=False)
        mock_validate_bbox.assert_called_once_with('bbox')

    def test_get_bbox_filter_returns_none_if_no_bbox(self):
        filter = self.activity_protocol.get_bbox_filter(cookies=False)
        self.assertIsNone(filter)

    def test_get_bbox_filter_returns_geoalchemy_function_for_bbox(self):
        self.request.params = {
            'bbox': '-8008785.1837498,11534051.373142,-7999612.7403568,'
            '11540472.083518'}
        filter = self.activity_protocol.get_bbox_filter(cookies=False)
        self.assertIsInstance(filter, geofunctions.intersects)
