import pytest
from mock import Mock, patch
from pyramid import testing

from lmkp.views.views import (
    get_output_format,
    get_page_parameters,
    get_bbox_parameters,
)
from ..integration_tests.base import (
    LmkpTestCase,
)
from ..base import get_settings


@pytest.mark.usefixtures('app')
@pytest.mark.unittest
@pytest.mark.views
class ViewsGetOutputFormatTests(LmkpTestCase):

    def setUp(self):
        self.request = testing.DummyRequest()
        settings = get_settings()
        self.config = testing.setUp(request=self.request, settings=settings)

    def tearDown(self):
        testing.tearDown()

    def test_get_output_format_returns_json_by_default(self):
        self.request.matchdict = {}
        output = get_output_format(self.request)
        self.assertEqual(output, 'json')

    def test_get_output_format_returns_output_format(self):
        self.request.matchdict = {'output': 'foo'}
        output = get_output_format(self.request)
        self.assertEqual(output, 'foo')


@pytest.mark.usefixtures('app')
@pytest.mark.unittest
@pytest.mark.views
class ViewsGetPageParametersTests(LmkpTestCase):

    def setUp(self):
        self.request = testing.DummyRequest()
        settings = get_settings()
        self.config = testing.setUp(request=self.request, settings=settings)

    def tearDown(self):
        testing.tearDown()

    def test_get_page_parameters_returns_default_values(self):
        page, page_size = get_page_parameters(self.request)
        self.assertEqual(page, 1)
        self.assertEqual(page_size, 10)

    def test_get_page_parameters_returns_parameters(self):
        self.request.params = {'page': 2, 'pagesize': 5}
        page, page_size = get_page_parameters(self.request)
        self.assertEqual(page, 2)
        self.assertEqual(page_size, 5)

    def test_get_page_parameters_returns_valid_values(self):
        self.request.params = {'page': -1, 'pagesize': 0}
        page, page_size = get_page_parameters(self.request)
        self.assertEqual(page, 1)
        self.assertEqual(page_size, 1)
        self.request.params = {'page': 0, 'pagesize': 1000}
        page, page_size = get_page_parameters(self.request)
        self.assertEqual(page, 1)
        self.assertEqual(page_size, 50)


@pytest.mark.usefixtures('app')
@pytest.mark.unittest
@pytest.mark.views
class ViewsGetBboxParametersTests(LmkpTestCase):

    def setUp(self):
        self.request = testing.DummyRequest()
        settings = get_settings()
        self.config = testing.setUp(request=self.request, settings=settings)

    def tearDown(self):
        testing.tearDown()

    def test_get_bbox_parameters_returns_none_or_default(self):
        bbox, epsg = get_bbox_parameters(self.request)
        self.assertIsNone(bbox)
        self.assertEqual(epsg, '900913')

    def test_get_bbox_parameters_returns_bbox_from_params(self):
        self.request.params = {'bbox': 'foo', 'epsg': 'bar'}
        bbox, epsg = get_bbox_parameters(self.request)
        self.assertEqual(bbox, 'foo')
        self.assertEqual(epsg, 'bar')

    def test_get_bbox_parameters_returns_bbox_from_cookies(self):
        self.request.cookies = {'_LOCATION_': 'foo'}
        bbox, epsg = get_bbox_parameters(self.request)
        self.assertEqual(bbox, 'foo')
        self.assertEqual(epsg, '900913')

    def test_get_bbox_parameters_does_not_return_bbox_from_cookies(self):
        self.request.cookies = {'_LOCATION_': 'foo'}
        bbox, epsg = get_bbox_parameters(self.request, cookies=False)
        self.assertIsNone(bbox)
        self.assertEqual(epsg, '900913')

    def test_get_bbox_parameters_returns_params_before_cookies(self):
        self.request.cookies = {'_LOCATION_': 'cookie'}
        self.request.params = {'bbox': 'param'}
        bbox, __ = get_bbox_parameters(self.request)
        self.assertEqual(bbox, 'param')


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
