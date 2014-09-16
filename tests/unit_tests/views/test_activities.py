import pytest
from mock import patch
from pyramid import testing

from lmkp.views.activities import ActivityView
from ...integration_tests.base import (
    LmkpTestCase,
)
from ...base import get_settings


@pytest.mark.usefixtures('app')
@pytest.mark.unittest
@pytest.mark.activities
class ActivityViewReadManyTests(LmkpTestCase):

    def setUp(self):
        self.request = testing.DummyRequest()
        self.request.matchdict = {'output': 'json'}
        settings = get_settings()
        self.config = testing.setUp(request=self.request, settings=settings)
        self.view = ActivityView(self.request)

    def tearDown(self):
        testing.tearDown()

    @patch('lmkp.views.activities.get_output_format')
    def test_read_many_calls_output_format(self, mock_get_output_format):
        mock_get_output_format.return_value = self.request.matchdict.get(
            'output')
        self.view.read_many()
        mock_get_output_format.assert_called_once_with(self.request)


@pytest.mark.usefixtures('app')
@pytest.mark.unittest
@pytest.mark.activities
class ActivityViewReadManyJsonTests(LmkpTestCase):

    def setUp(self):
        self.request = testing.DummyRequest()
        self.request.matchdict = {'output': 'json'}
        settings = get_settings()
        self.config = testing.setUp(request=self.request, settings=settings)
        self.view = ActivityView(self.request)

    def tearDown(self):
        testing.tearDown()

    @patch('lmkp.views.activities.activity_protocol.read_many')
    def test_read_many_json_calls_activity_protocol(
            self, mock_protocol_read_many):
        mock_protocol_read_many.return_value = []
        self.view.read_many()
        mock_protocol_read_many.assert_called_once_with(
            self.request, public=False)

    @patch('lmkp.views.activities.render_to_response')
    @patch('lmkp.views.activities.activity_protocol.read_many')
    def test_read_many_json_calls_render_to_response(
            self, mock_protocol_read_many, mock_render_to_response):
        mock_protocol_read_many.return_value = []
        self.view.read_many()
        mock_render_to_response.assert_called_once_with(
            'json', mock_protocol_read_many.return_value, self.request)


@pytest.mark.usefixtures('app')
@pytest.mark.unittest
@pytest.mark.activities
class ActivityViewReadManyGeojsonTests(LmkpTestCase):

    def setUp(self):
        self.request = testing.DummyRequest()
        self.request.matchdict = {'output': 'geojson'}
        settings = get_settings()
        self.config = testing.setUp(request=self.request, settings=settings)
        self.view = ActivityView(self.request)

    def tearDown(self):
        testing.tearDown()

    @patch('lmkp.views.activities.activity_protocol.read_many_geojson')
    def test_read_many_geojson_calls_activity_protocol(
            self, mock_protocol_read_many_geojson):
        mock_protocol_read_many_geojson.return_value = []
        self.view.read_many()
        mock_protocol_read_many_geojson.assert_called_once_with(
            self.request, public=False)

    @patch('lmkp.views.activities.render_to_response')
    @patch('lmkp.views.activities.activity_protocol.read_many_geojson')
    def test_read_many_json_calls_render_to_response(
            self, mock_protocol_read_many_geojson, mock_render_to_response):
        mock_protocol_read_many_geojson.return_value = []
        self.view.read_many()
        mock_render_to_response.assert_called_once_with(
            'json', mock_protocol_read_many_geojson.return_value, self.request)


@pytest.mark.usefixtures('app')
@pytest.mark.unittest
@pytest.mark.activities
class ActivityViewReadManyHtmlTests(LmkpTestCase):

    def setUp(self):
        self.request = testing.DummyRequest()
        self.request.matchdict = {'output': 'html'}
        settings = get_settings()
        self.config = testing.setUp(request=self.request, settings=settings)
        self.view = ActivityView(self.request)

    def tearDown(self):
        testing.tearDown()

    @patch('lmkp.views.activities.get_page_parameters')
    @patch('lmkp.views.activities.render_to_response')
    def test_read_many_html_calls_get_page_parameters(
            self, mock_render_to_response, mock_get_page_parameters):
        mock_render_to_response.return_value = {}
        mock_get_page_parameters.return_value = 1, 1
        self.view.read_many()
        mock_get_page_parameters.assert_called_once_with(self.request)

    @patch('lmkp.views.activities.get_bbox_parameters')
    @patch('lmkp.views.activities.render_to_response')
    def test_read_many_html_calls_get_bbox_parameters(
            self, mock_render_to_response, mock_get_bbox_parameters):
        mock_render_to_response.return_value = {}
        mock_get_bbox_parameters.return_value = 'foo', 'bar'
        self.view.read_many()
        mock_get_bbox_parameters.assert_called_once_with(self.request)

    @patch('lmkp.views.activities.activity_protocol.read_many')
    @patch('lmkp.views.activities.render_to_response')
    def test_read_many_json_calls_activity_protocol(
            self, mock_render_to_response, mock_protocol_read_many):
        mock_render_to_response.return_value = {}
        mock_protocol_read_many.return_value = []
        self.view.read_many()
        mock_protocol_read_many.assert_called_once_with(
            self.request, public=False, limit=10, offset=0)

    @patch('lmkp.views.activities.get_status_parameter')
    @patch('lmkp.views.activities.render_to_response')
    def test_read_many_html_calls_get_status_parameter(
            self, mock_render_to_response, mock_get_status_parameter):
        mock_render_to_response.return_value = {}
        mock_get_status_parameter.return_value = 'foo'
        self.view.read_many()
        mock_get_status_parameter.assert_called_once_with(self.request)

    @patch('lmkp.views.activities.BaseView.get_base_template_values')
    @patch('lmkp.views.activities.render_to_response')
    def test_read_many_html_calls_get_base_template_values(
            self, mock_render_to_response, mock_get_base_template_values):
        mock_render_to_response.return_value = {}
        self.view.read_many()
        mock_get_base_template_values.assert_called_once_with()

    @patch('lmkp.views.activities.BaseView.get_base_template_values')
    @patch('lmkp.views.activities.get_bbox_parameters')
    @patch('lmkp.views.activities.render_to_response')
    @patch('lmkp.views.activities.get_customized_template_path')
    def test_read_many_html_calls_render_to_response(
            self, get_customized_template_path, mock_render_to_response,
            mock_get_bbox_parameters, mock_get_base_template_values):
        mock_render_to_response.return_value = {}
        mock_get_base_template_values.return_value = {
            'profile': 'profile',
            'locale': 'en'
        }
        get_customized_template_path.return_value = 'template_path'
        mock_get_bbox_parameters.return_value = 'map', None
        self.view.read_many()
        mock_render_to_response.assert_called_once_with(
            'template_path',
            {
                'profile': 'profile',
                'statusfilter': None,
                'spatialfilter': 'map',
                'pagesize': 10,
                'currentpage': 1,
                'locale': 'en',
                'total': 0,
                'data': [],
                'invfilter': None
            },
            self.request)
