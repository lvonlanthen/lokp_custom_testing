import pytest
from mock import Mock

from ..integration_tests.base import (
    LmkpTestCase,
)
from lmkp.views.views import (
    get_output_format,
)


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
