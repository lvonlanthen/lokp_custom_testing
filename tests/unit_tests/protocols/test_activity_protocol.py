import pytest
from mock import patch
from pyramid import testing

from lmkp.protocols.activity_protocol import ActivityProtocol
from ...integration_tests.base import (
    LmkpTestCase,
)
from ...base import get_settings


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
    @patch('lmkp.protocols.activity_protocol.ActivityProtocol._query_many')
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
        'lmkp.protocols.activity_protocol.ActivityProtocol.'
        '_get_profile_filter')
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
        'lmkp.protocols.activity_protocol.ActivityProtocol.'
        '_get_profile_filter')
    def test_get_relevant_activities_many_calls_get_attribute_filters(
            self, mock_get_profile_filter, mock_get_attribute_filters):
        mock_get_attribute_filters.return_value = ([], [])
        mock_get_profile_filter.return_value = None
        self.activity_protocol.get_relevant_activities_many()
        mock_get_attribute_filters.assert_called_once_with()
