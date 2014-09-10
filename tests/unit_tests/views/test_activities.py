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
@pytest.mark.download
class ActivityViewReadManyJsonTests(LmkpTestCase):

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
        mock_get_output_format.return_value = 'json'
        self.view.read_many()
        mock_get_output_format.assert_called_once_with(self.request)

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
@pytest.mark.download
class ActivityViewReadManyJson(LmkpTestCase):

    def setUp(self):
        self.request = testing.DummyRequest()
        self.request.matchdict = {'output': 'json'}
        settings = get_settings()
        self.config = testing.setUp(request=self.request, settings=settings)
        self.view = ActivityView(self.request)

    def tearDown(self):
        testing.tearDown()
