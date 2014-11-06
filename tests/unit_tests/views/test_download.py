import pytest
from mock import patch
from pyramid import testing

from ...integration_tests.base import (
    LmkpTestCase,
)
from ...base import get_settings


@pytest.mark.usefixtures('app')
@pytest.mark.unittest
@pytest.mark.download
class ActivityDownloadTest(LmkpTestCase):

    def setUp(self):
        self.request = testing.DummyRequest()
        settings = get_settings()
        self.config = testing.setUp(request=self.request, settings=settings)

    def tearDown(self):
        testing.tearDown()

    def test_download_returns_csv(self):
        res = self.app.post('/activities/download', params={
            'format': 'csv'
        })
        self.assertEqual(res.status_int, 200)
        self.assertEqual(res.content_type, 'text/csv')

    @patch('lmkp.views.download.to_flat_table')
    def test_download_calls_to_table(self, mock_to_flat_table):
        mock_to_flat_table.return_value = ([], [])
        self.app.post('/activities/download', params={
            'format': 'csv'
        })
        mock_to_flat_table.assert_called_once()


@pytest.mark.usefixtures('app')
@pytest.mark.unittest
@pytest.mark.download
class StakeholderDownloadTest(LmkpTestCase):

    def setUp(self):
        self.request = testing.DummyRequest()
        settings = get_settings()
        self.config = testing.setUp(request=self.request, settings=settings)

    def tearDown(self):
        testing.tearDown()

    def test_download_returns_csv(self):
        res = self.app.post('/stakeholders/download', params={
            'format': 'csv'
        })
        self.assertEqual(res.status_int, 200)
        self.assertEqual(res.content_type, 'text/csv')

    @patch('lmkp.views.download.to_flat_table')
    def test_download_calls_to_table(self, mock_to_flat_table):
        mock_to_flat_table.return_value = ([], [])
        self.app.post('/stakeholders/download', params={
            'format': 'csv'
        })
        mock_to_flat_table.assert_called_once()
