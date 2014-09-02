import pytest
from mock import Mock, patch
from pyramid import testing

from lmkp.views import download
from lmkp.views.views import (
    get_output_format,
)
from ..integration_tests.base import (
    LmkpTestCase,
)
from ..base import get_settings


@pytest.mark.usefixtures('app')
@pytest.mark.unittest
class TestViews(LmkpTestCase):

    def test_get_output_format_returns_json_by_default(self):
        mock_request = Mock()
        mock_request.matchdict = {}
        output = get_output_format(mock_request)
        self.assertEqual(output, 'json')

    def test_get_output_format_returns_output_format(self):
        mock_request = Mock()
        mock_request.matchdict = {'output': 'foo'}
        output = get_output_format(mock_request)
        self.assertEqual(output, 'foo')


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
        res = self.app.get('/download')
        self.assertEqual(res.status_int, 200)
        self.assertEqual(res.content_type, 'text/csv')

    @patch('lmkp.views.download.to_table')
    def test_download_calls_to_table(self, mock_to_table):
        mock_to_table.return_value = ([], [])
        view = download.DownloadView(self.request)
        view.downloadAll()
        mock_to_table.assert_called_once_with(self.request)
