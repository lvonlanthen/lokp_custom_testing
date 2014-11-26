import pytest
from geoalchemy.functions import functions as geofunctions
from mock import patch, Mock
from pyramid import testing
from sqlalchemy.orm.query import Query
import sqlalchemy

from lmkp.protocols.stakeholder_protocol import StakeholderProtocol
from lmkp.protocols.features import ItemFeature
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


@pytest.mark.usefixtures('app')
@pytest.mark.unittest
@pytest.mark.protocol
class ProtocolsStakeholderProtocolQueryToFeatures(LmkpTestCase):

    def setUp(self):
        self.request = testing.DummyRequest()
        settings = get_settings()
        self.config = testing.setUp(request=self.request, settings=settings)
        self.stakeholder_protocol = StakeholderProtocol(self.request)
        q1 = Mock()  # Stakeholder 1, Taggroup 1, Tag 1
        q1.identifier = 'identifier1'
        q1.version = 1
        q1.order_value = 1
        q1.taggroup = 1
        q1.key = 'key1'
        q1.value = 'value1'
        self.q1 = q1
        q2 = Mock()  # Stakeholder 1, Taggroup 1, Tag 2
        q2.identifier = 'identifier1'
        q2.version = 1
        q2.order_value = 1
        q2.taggroup = 1
        q2.key = 'key2'
        q2.value = 'value2'
        self.q2 = q2
        q3 = Mock()  # Stakeholder 1, Taggroup 2, Tag 1
        q3.identifier = 'identifier1'
        q3.version = 1
        q3.order_value = 1
        q3.taggroup = 2
        q3.key = 'key3'
        q3.value = 'value3'
        self.q3 = q3
        q4 = Mock()  # Stakeholder 2, Taggroup 1, Tag 1
        q4.identifier = 'identifier2'
        q4.version = 1
        q4.order_value = 1
        q4.taggroup = 1
        q4.key = 'key4'
        q4.value = 'value4'
        self.q4 = q4
        rel_act = Mock()
        rel_act.all.return_value = [self.q1, self.q2, self.q3, self.q4]
        self.rel_act = rel_act

    def tearDown(self):
        testing.tearDown()

    @patch('lmkp.protocols.stakeholder_protocol.get_user_privileges')
    def test_query_to_features_calls_get_user_privileges(
            self, mock_get_user_privileges):
        mock_get_user_privileges.return_value = None, None
        self.stakeholder_protocol.query_to_features(self.rel_act)
        mock_get_user_privileges.assert_called_once_with(self.request)

    def test_query_to_features_separates_features(self):
        self.rel_act.all.return_value = [self.q1, self.q4]
        features = self.stakeholder_protocol.query_to_features(self.rel_act)
        self.assertEqual(len(features), 2)

    def test_query_to_features_separates_taggroups(self):
        self.rel_act.all.return_value = [self.q1, self.q3]
        features = self.stakeholder_protocol.query_to_features(self.rel_act)
        self.assertEqual(len(features), 1)
        self.assertEqual(len(features[0].taggroups), 2)

    def test_query_to_features_separates_tags(self):
        self.rel_act.all.return_value = [self.q1, self.q2]
        features = self.stakeholder_protocol.query_to_features(self.rel_act)
        self.assertEqual(len(features), 1)
        self.assertEqual(len(features[0].taggroups), 1)
        self.assertEqual(len(features[0].taggroups[0].tags), 2)

    def test_query_to_features_returns_list_with_features(self):
        features = self.stakeholder_protocol.query_to_features(self.rel_act)
        self.assertIsInstance(features, list)
        self.assertEqual(len(features), 2)
        for f in features:
            self.assertIsInstance(f, ItemFeature)


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
        'get_relevant_query_many')
    @patch(
        'lmkp.protocols.stakeholder_protocol.StakeholderProtocol.query_many')
    @patch(
        'lmkp.protocols.stakeholder_protocol.StakeholderProtocol.'
        'query_to_features')
    def test_read_many_calls_get_relevant_query_many(
            self, mock_query_to_features, mock_query_many,
            mock_get_relevant_query_many):
        mock_query_many.return_value = (None, 0)
        mock_query_to_features.return_value = []
        self.stakeholder_protocol.read_many()
        mock_get_relevant_query_many.assert_called_once_with(
            public_query=True)

    @patch(
        'lmkp.protocols.stakeholder_protocol.get_current_involvement_details')
    @patch(
        'lmkp.protocols.stakeholder_protocol.StakeholderProtocol.'
        'get_relevant_query_many')
    @patch(
        'lmkp.protocols.stakeholder_protocol.StakeholderProtocol.query_many')
    @patch(
        'lmkp.protocols.stakeholder_protocol.StakeholderProtocol.'
        'query_to_features')
    def test_read_many_calls_get_current_involvement_details(
            self, mock_query_to_features, mock_query_many,
            mock_get_relevant_query_many,
            mock_get_current_involvement_details):
        mock_query_many.return_value = (None, 0)
        mock_query_to_features.return_value = []
        mock_get_relevant_query_many.return_value = None
        self.stakeholder_protocol.read_many()
        mock_get_current_involvement_details.assert_called_once_with(
            self.request)

    @patch(
        'lmkp.protocols.stakeholder_protocol.get_current_limit')
    @patch(
        'lmkp.protocols.stakeholder_protocol.StakeholderProtocol.'
        'get_relevant_query_many')
    @patch(
        'lmkp.protocols.stakeholder_protocol.StakeholderProtocol.query_many')
    @patch(
        'lmkp.protocols.stakeholder_protocol.StakeholderProtocol.'
        'query_to_features')
    def test_read_many_calls_get_current_limit(
            self, mock_query_to_features, mock_query_many,
            mock_get_relevant_query_many,
            mock_get_current_limit):
        mock_query_many.return_value = (None, 0)
        mock_query_to_features.return_value = []
        mock_get_relevant_query_many.return_value = None
        self.stakeholder_protocol.read_many()
        mock_get_current_limit.assert_called_once_with(self.request)

    @patch(
        'lmkp.protocols.stakeholder_protocol.get_current_offset')
    @patch(
        'lmkp.protocols.stakeholder_protocol.StakeholderProtocol.'
        'get_relevant_query_many')
    @patch(
        'lmkp.protocols.stakeholder_protocol.StakeholderProtocol.query_many')
    @patch(
        'lmkp.protocols.stakeholder_protocol.StakeholderProtocol.'
        'query_to_features')
    def test_read_many_calls_get_current_offset(
            self, mock_query_to_features, mock_query_many,
            mock_get_relevant_query_many,
            mock_get_current_offset):
        mock_query_many.return_value = (None, 0)
        mock_query_to_features.return_value = []
        mock_get_relevant_query_many.return_value = None
        self.stakeholder_protocol.read_many()
        mock_get_current_offset.assert_called_once_with(self.request)

    @patch(
        'lmkp.protocols.stakeholder_protocol.StakeholderProtocol.'
        'get_relevant_query_many')
    @patch(
        'lmkp.protocols.stakeholder_protocol.StakeholderProtocol.query_many')
    @patch(
        'lmkp.protocols.stakeholder_protocol.StakeholderProtocol.'
        'query_to_features')
    def test_read_many_calls_query_many(
            self, mock_query_to_features, mock_query_many,
            mock_get_relevant_query_many):
        mock_query_many.return_value = (None, 0)
        mock_query_to_features.return_value = []
        mock_get_relevant_query_many.return_value = None
        self.stakeholder_protocol.read_many()
        mock_query_many.assert_called_once_with(
            None, limit=None, with_involvements=True, offset=0)

    @patch(
        'lmkp.protocols.stakeholder_protocol.StakeholderProtocol.'
        'get_relevant_query_many')
    @patch(
        'lmkp.protocols.stakeholder_protocol.StakeholderProtocol.query_many')
    @patch(
        'lmkp.protocols.stakeholder_protocol.StakeholderProtocol.'
        'query_to_features')
    def test_read_many_calls_query_to_features(
            self, mock_query_to_features, mock_query_many,
            mock_get_relevant_query_many):
        mock_query_many.return_value = (None, 0)
        mock_query_to_features.return_value = []
        mock_get_relevant_query_many.return_value = None
        self.stakeholder_protocol.read_many()
        mock_query_to_features.assert_called_once_with(
            None, involvements='full', translate=True, public_query=True)


@pytest.mark.unittest
@pytest.mark.protocol
class ProtocolsStakeholderProtocolGetRelevantQueryMany(LmkpTestCase):

    def setUp(self):
        self.request = testing.DummyRequest()
        settings = get_settings()
        self.config = testing.setUp(request=self.request, settings=settings)
        self.stakeholder_protocol = StakeholderProtocol(self.request)

    def tearDown(self):
        testing.tearDown()

    @patch('lmkp.protocols.stakeholder_protocol.get_user_privileges')
    def test_get_relevant_query_many_calls_get_user_privileges(
            self, mock_get_user_privileges):
        mock_get_user_privileges.return_value = (None, None)
        self.stakeholder_protocol.get_relevant_query_many()
        mock_get_user_privileges.assert_called_once_with(self.request)

    @patch(
        'lmkp.protocols.stakeholder_protocol.StakeholderProtocol.'
        'get_attribute_filters')
    def test_get_relevant_query_many_calls_get_attribute_filters(
            self, mock_get_attribute_filters):
        mock_get_attribute_filters.return_value = ([], [])
        self.stakeholder_protocol.get_relevant_query_many()
        mock_get_attribute_filters.assert_called_once_with()

    @patch(
        'lmkp.protocols.stakeholder_protocol.'
        'get_current_logical_filter_operator')
    def test_get_relevant_query_many_calls_get_logical_filter_operator(
            self, mock_get_logical_filter_operator):
        self.request.params = {'sh__foo__like': 'bar'}
        self.stakeholder_protocol.get_relevant_query_many()
        mock_get_logical_filter_operator.assert_called_once_with(self.request)

    @patch('lmkp.protocols.stakeholder_protocol.StakeholderProtocol.get_order')
    def test_get_relevant_query_many_calls_get_order(
            self, mock_get_order):
        with self.assertRaises(UnboundLocalError):
            self.stakeholder_protocol.get_relevant_query_many()
        mock_get_order.assert_called_once_with('sh')

    @patch(
        'lmkp.protocols.stakeholder_protocol.StakeholderProtocol.'
        'apply_visible_version_filter')
    def test_get_relevant_query_many_calls_apply_visible_version_filter(
            self, mock_apply_visible_version_filter):
        self.stakeholder_protocol.get_relevant_query_many()
        mock_apply_visible_version_filter.assert_called_once()

    @patch('lmkp.protocols.stakeholder_protocol.get_current_order_direction')
    def test_get_relevant_query_many_calls_get_current_order_direction(
            self, mock_get_order_direction):
        self.stakeholder_protocol.get_relevant_query_many()
        mock_get_order_direction.assert_called_once_with(self.request)

    def test_get_relevant_query_many_returns_query(self):
        rel_query = self.stakeholder_protocol.get_relevant_query_many()
        self.assertIsInstance(rel_query, Query)


@pytest.mark.unittest
@pytest.mark.protocol
class ProtocolsStakeholderProtocolQueryMany(LmkpTestCase):

    def setUp(self):
        self.request = testing.DummyRequest()
        settings = get_settings()
        self.config = testing.setUp(request=self.request, settings=settings)
        self.stakeholder_protocol = StakeholderProtocol(self.request)

    def tearDown(self):
        testing.tearDown()

    @patch(
        'lmkp.protocols.stakeholder_protocol.StakeholderProtocol.'
        'get_translation_queries')
    def test_query_many_calls_get_translation_queries(
            self, mock_get_translation_queries):
        mock_get_translation_queries.return_value = Session.query(
            SH_Key.fk_key.label("key_original_id"),
            SH_Key.key.label("key_translated")
        ).subquery(), Session.query(
            SH_Value.fk_value.label("value_original_id"),
            SH_Value.value.label("value_translated")
        ).subquery()
        rel_query = self.stakeholder_protocol.get_relevant_query_many()
        self.stakeholder_protocol.query_many(rel_query, return_count=False)
        mock_get_translation_queries.assert_called_once_with('sh')

    @patch('lmkp.protocols.stakeholder_protocol.get_current_order_direction')
    def test_query_many_with_involvements_calls_get_current_order_direction(
            self, mock_get_current_order_direction):
        rel_query = self.stakeholder_protocol.get_relevant_query_many()
        self.stakeholder_protocol.query_many(
            rel_query, with_involvements=True, return_count=False)
        mock_get_current_order_direction.assert_called()

    @patch('lmkp.protocols.stakeholder_protocol.get_user_privileges')
    def test_query_many_with_involvements_calls_get_user_privileges(
            self, mock_get_user_privileges):
        mock_get_user_privileges.return_value = None, None
        rel_query = self.stakeholder_protocol.get_relevant_query_many()
        self.stakeholder_protocol.query_many(
            rel_query, with_involvements=True, return_count=False)
        mock_get_user_privileges.assert_called()

    @patch(
        'lmkp.protocols.stakeholder_protocol.StakeholderProtocol.'
        'get_valid_status_ids')
    def test_query_many_with_involvements_calls_get_valid_status_ids(
            self, mock_get_valid_status_ids):
        rel_query = self.stakeholder_protocol.get_relevant_query_many()
        self.stakeholder_protocol.query_many(
            rel_query, with_involvements=True, return_count=False)
        mock_get_valid_status_ids.assert_called_once_with(
            'involvements', None, None)

    def test_query_many_returns_query(self):
        rel_query = self.stakeholder_protocol.get_relevant_query_many()
        query = self.stakeholder_protocol.query_many(
            rel_query, with_involvements=True, return_count=False)
        self.assertIsInstance(query, Query)

    @pytest.mark.usefixtures('app')
    def test_query_many_returns_query_and_count(self):
        rel_query = self.stakeholder_protocol.get_relevant_query_many()
        query, count = self.stakeholder_protocol.query_many(
            rel_query, with_involvements=True, return_count=True)
        self.assertIsInstance(query, Query)
        self.assertIsInstance(count, long)
