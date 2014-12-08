import pytest
from mock import patch
from pyramid import testing

from ...integration_tests.base import (
    LmkpTestCase,
)
from ...base import get_settings
from lmkp.protocols.activity_protocol import ActivityProtocol
from lmkp.protocols.stakeholder_protocol import StakeholderProtocol
from lmkp.views.download import to_flat_table


@pytest.mark.unittest
@pytest.mark.download
class ActivityDownloadTest(LmkpTestCase):

    def setUp(self):
        self.request = testing.DummyRequest()
        settings = get_settings()
        self.config = testing.setUp(request=self.request, settings=settings)

    def tearDown(self):
        testing.tearDown()

    @patch.object(ActivityProtocol, 'read_many')
    @patch('lmkp.views.download.getCategoryList')
    def test_to_table_calls_activity_protocol_read_many(
            self, mock_getCategoryList, mock_read_many):
        mock_read_many.return_value = {}
        to_flat_table(self.request, 'activities')
        mock_read_many.assert_called_once_with(
            public_query=True, translate=False)


@pytest.mark.unittest
@pytest.mark.download
class StakeholderDownloadTest(LmkpTestCase):

    def setUp(self):
        self.request = testing.DummyRequest()
        settings = get_settings()
        self.config = testing.setUp(request=self.request, settings=settings)

    def tearDown(self):
        testing.tearDown()

    @patch.object(StakeholderProtocol, 'read_many')
    @patch('lmkp.views.download.getCategoryList')
    def test_to_table_calls_stakeholder_protocol_read_many(
            self, mock_getCategoryList, mock_read_many):
        to_flat_table(self.request, 'stakeholders')
        mock_read_many.assert_called_once_with(
            public_query=True, translate=False, other_identifiers=[])
