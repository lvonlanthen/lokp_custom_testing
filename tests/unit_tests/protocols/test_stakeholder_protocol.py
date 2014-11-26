import pytest
from geoalchemy.functions import functions as geofunctions
from mock import patch, Mock
from pyramid import testing
from sqlalchemy.orm.query import Query
import sqlalchemy

from lmkp.protocols.stakeholder_protocol import StakeholderProtocol
from lmkp.protocols.activity_features import ActivityFeature
from ...integration_tests.base import (
    LmkpTestCase,
)
from ...base import get_settings

from lmkp.models.database_objects import (
    Activity,
    SH_Key,
    SH_Value,
    User,
)
from lmkp.models.meta import DBSession as Session


@pytest.mark.unittest
@pytest.mark.protocol
class ProtocolsStakeholderProtocolReadMany(LmkpTestCase):

    def setUp(self):
        self.request = testing.DummyRequest()
        settings = get_settings()
        self.config = testing.setUp(request=self.request, settings=settings)
        self.stakeholder_protocol = StakeholderProtocol(self.request)

    def tearDown(self):
        testing.tearDown()

    @patch(
        'lmkp.protocols.stakeholder_protocol.StakeholderProtocol.'
        'get_relevant_stakeholders_many')
    @patch(
        'lmkp.protocols.stakeholder_protocol.StakeholderProtocol.query_many')
    @patch(
        'lmkp.protocols.stakeholder_protocol.StakeholderProtocol.'
        'query_to_features')
    def test_read_many_calls_get_relevant_stakeholders_many(
            self, mock_query_to_features, mock_query_many,
            mock_get_relevant_stakeholders_many):
        mock_query_many.return_value = (None, 0)
        mock_query_to_features.return_value = []
        self.stakeholder_protocol.read_many()
        mock_get_relevant_stakeholders_many.assert_called_once_with(
            public_query=True)

    @patch(
        'lmkp.protocols.stakeholder_protocol.get_current_involvement_details')
    @patch(
        'lmkp.protocols.stakeholder_protocol.StakeholderProtocol.'
        'get_relevant_stakeholders_many')
    @patch(
        'lmkp.protocols.stakeholder_protocol.StakeholderProtocol.query_many')
    @patch(
        'lmkp.protocols.stakeholder_protocol.StakeholderProtocol.'
        'query_to_features')
    def test_read_many_calls_get_current_involvement_details(
            self, mock_query_to_features, mock_query_many,
            mock_get_relevant_stakeholders_many,
            mock_get_current_involvement_details):
        mock_query_many.return_value = (None, 0)
        mock_query_to_features.return_value = []
        mock_get_relevant_stakeholders_many.return_value = None
        self.stakeholder_protocol.read_many()
        mock_get_current_involvement_details.assert_called_once_with(
            self.request)

    @patch(
        'lmkp.protocols.stakeholder_protocol.get_current_limit')
    @patch(
        'lmkp.protocols.stakeholder_protocol.StakeholderProtocol.'
        'get_relevant_stakeholders_many')
    @patch(
        'lmkp.protocols.stakeholder_protocol.StakeholderProtocol.query_many')
    @patch(
        'lmkp.protocols.stakeholder_protocol.StakeholderProtocol.'
        'query_to_features')
    def test_read_many_calls_get_current_limit(
            self, mock_query_to_features, mock_query_many,
            mock_get_relevant_stakeholders_many,
            mock_get_current_limit):
        mock_query_many.return_value = (None, 0)
        mock_query_to_features.return_value = []
        mock_get_relevant_stakeholders_many.return_value = None
        self.stakeholder_protocol.read_many()
        mock_get_current_limit.assert_called_once_with(self.request)

    @patch(
        'lmkp.protocols.stakeholder_protocol.get_current_offset')
    @patch(
        'lmkp.protocols.stakeholder_protocol.StakeholderProtocol.'
        'get_relevant_stakeholders_many')
    @patch(
        'lmkp.protocols.stakeholder_protocol.StakeholderProtocol.query_many')
    @patch(
        'lmkp.protocols.stakeholder_protocol.StakeholderProtocol.'
        'query_to_features')
    def test_read_many_calls_get_current_offset(
            self, mock_query_to_features, mock_query_many,
            mock_get_relevant_stakeholders_many,
            mock_get_current_offset):
        mock_query_many.return_value = (None, 0)
        mock_query_to_features.return_value = []
        mock_get_relevant_stakeholders_many.return_value = None
        self.stakeholder_protocol.read_many()
        mock_get_current_offset.assert_called_once_with(self.request)


# @pytest.mark.foo
# @pytest.mark.unittest
# @pytest.mark.protocol
# class ProtocolsStakeholderProtocolQueryMany(LmkpTestCase):

#     def setUp(self):
#         self.request = testing.DummyRequest()
#         settings = get_settings()
#         self.config = testing.setUp(request=self.request, settings=settings)
#         self.stakeholder_protocol = StakeholderProtocol(self.request)

#     def tearDown(self):
#         testing.tearDown()

#     @patch(
#         'lmkp.protocols.stakeholder_protocol.StakeholderProtocol.'
#         'get_translation_queries')
#     @patch(
#         'lmkp.protocols.stakeholder_protocol.StakeholderProtocol.get_profile_filter')
#     def test_query_many_calls_get_translation_queries(
#             self, mock_get_profile_filter, mock_get_translation_queries):
#         mock_get_profile_filter.return_value = None
#         mock_get_translation_queries.return_value = Session.query(
#             SH_Key.fk_key.label("key_original_id"),
#             SH_Key.key.label("key_translated")
#         ).subquery(), Session.query(
#             SH_Value.fk_value.label("value_original_id"),
#             SH_Value.value.label("value_translated")
#         ).subquery()
#         rel_act = self.stakeholder_protocol.get_relevant_stakeholders_many()
#         self.stakeholder_protocol.query_many(rel_act, return_count=False)
#         mock_get_translation_queries.assert_called_once_with('a')

#     # @patch('lmkp.protocols.stakeholder_protocol.get_current_order_direction')
#     # @patch(
#     #     'lmkp.protocols.stakeholder_protocol.StakeholderProtocol.get_profile_filter')
#     # def test_query_many_with_involvements_calls_get_current_order_direction(
#     #         self, mock_get_profile_filter, mock_get_current_order_direction):
#     #     mock_get_profile_filter.return_value = None
#     #     rel_act = self.stakeholder_protocol.get_relevant_stakeholders_many()
#     #     self.stakeholder_protocol.query_many(
#     #         rel_act, with_involvements=True, return_count=False)
#     #     mock_get_current_order_direction.assert_called()

#     # @patch('lmkp.protocols.stakeholder_protocol.get_user_privileges')
#     # @patch(
#     #     'lmkp.protocols.stakeholder_protocol.StakeholderProtocol.get_profile_filter')
#     # def test_query_many_with_involvements_calls_get_user_privileges(
#     #         self, mock_get_profile_filter, mock_get_user_privileges):
#     #     mock_get_user_privileges.return_value = None, None
#     #     mock_get_profile_filter.return_value = None
#     #     rel_act = self.stakeholder_protocol.get_relevant_stakeholders_many()
#     #     self.stakeholder_protocol.query_many(
#     #         rel_act, with_involvements=True, return_count=False)
#     #     mock_get_user_privileges.assert_called()

#     # @patch(
#     #     'lmkp.protocols.stakeholder_protocol.StakeholderProtocol.'
#     #     'get_valid_status_ids')
#     # @patch(
#     #     'lmkp.protocols.stakeholder_protocol.StakeholderProtocol.get_profile_filter')
#     # def test_query_many_with_involvements_calls_get_valid_status_ids(
#     #         self, mock_get_profile_filter, mock_get_valid_status_ids):
#     #     mock_get_profile_filter.return_value = None
#     #     rel_act = self.stakeholder_protocol.get_relevant_stakeholders_many()
#     #     self.stakeholder_protocol.query_many(
#     #         rel_act, with_involvements=True, return_count=False)
#     #     mock_get_valid_status_ids.assert_called_once_with(
#     #         'involvements', None, None)

#     # @patch(
#     #     'lmkp.protocols.stakeholder_protocol.StakeholderProtocol.get_profile_filter')
#     # def test_query_many_returns_query(
#     #         self, mock_get_profile_filter):
#     #     mock_get_profile_filter.return_value = None
#     #     rel_act = self.stakeholder_protocol.get_relevant_stakeholders_many()
#     #     query = self.stakeholder_protocol.query_many(
#     #         rel_act, with_involvements=True, return_count=False)
#     #     self.assertIsInstance(query, Query)

#     # @pytest.mark.usefixtures('app')
#     # @patch(
#     #     'lmkp.protocols.stakeholder_protocol.StakeholderProtocol.get_profile_filter')
#     # def test_query_many_returns_query_and_count(
#     #         self, mock_get_profile_filter):
#     #     mock_get_profile_filter.return_value = None
#     #     rel_act = self.stakeholder_protocol.get_relevant_stakeholders_many()
#     #     query, count = self.stakeholder_protocol.query_many(
#     #         rel_act, with_involvements=True, return_count=True)
#     #     self.assertIsInstance(query, Query)
#     #     self.assertIsInstance(count, long)
