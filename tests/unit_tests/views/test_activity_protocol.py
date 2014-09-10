import pytest
from geoalchemy.functions import functions as geofunctions
from mock import patch
from pyramid import testing

from lmkp.views.activity_protocol3 import ActivityProtocol3 as ActivityProtocol
from ...integration_tests.base import (
    LmkpTestCase,
)
from ...base import get_settings


@pytest.mark.usefixtures('app')
@pytest.mark.unittest
@pytest.mark.download
class ActivityProtocolTests(LmkpTestCase):

    def setUp(self):
        self.request = testing.DummyRequest()
        self.request.matchdict = {'output': 'json'}
        settings = get_settings()
        self.config = testing.setUp(request=self.request, settings=settings)
        self.protocol = ActivityProtocol(self.db_session)

    def tearDown(self):
        testing.tearDown()

    @patch('lmkp.views.activity_protocol3.get_bbox_parameters')
    def test_get_bbox_filter_calls_get_bbox_parameters(
            self, mock_get_bbox_parameters):
        mock_get_bbox_parameters.return_value = None, None
        self.protocol._get_bbox_filter(self.request, cookies=False)
        mock_get_bbox_parameters.assert_called_once_with(
            self.request, cookies=False)

    @patch('lmkp.views.activity_protocol3.validate_bbox')
    @patch('lmkp.views.activity_protocol3.get_bbox_parameters')
    def test_get_bbox_filter_calls_validate_bbox(
            self, mock_get_bbox_parameters, mock_validate_bbox):
        mock_get_bbox_parameters.return_value = 'bbox', 'epsg'
        self.protocol._get_bbox_filter(self.request, cookies=False)
        mock_validate_bbox.assert_called_once_with('bbox')

    def test_get_bbox_filter_returns_none_if_no_bbox(self):
        filter = self.protocol._get_bbox_filter(self.request, cookies=False)
        self.assertIsNone(filter)

    def test_get_bbox_filter_returns_geoalchemy_functoin_for_bbox(self):
        self.request.params = {
            'bbox': '-8008785.1837498,11534051.373142,-7999612.7403568,'
            '11540472.083518'}
        filter = self.protocol._get_bbox_filter(self.request, cookies=False)
        self.assertIsInstance(filter, geofunctions.intersects)
