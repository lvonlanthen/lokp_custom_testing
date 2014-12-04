import pytest
from uuid import uuid4
from mock import patch, Mock
from pyramid import testing
from pyramid.httpexceptions import (
    HTTPForbidden,
    HTTPNotFound,
)

from lmkp.protocols.stakeholder_protocol import StakeholderProtocol
from lmkp.views.stakeholders import StakeholderView
from ...integration_tests.base import (
    LmkpTestCase,
)
from ...base import get_settings


@pytest.mark.usefixtures('app')
@pytest.mark.unittest
@pytest.mark.stakeholders
class StakeholderViewReadManyTests(LmkpTestCase):

    def setUp(self):
        self.request = testing.DummyRequest()
        self.request.matchdict = {'output': 'json'}
        settings = get_settings()
        self.config = testing.setUp(request=self.request, settings=settings)
        self.view = StakeholderView(self.request)

    def tearDown(self):
        testing.tearDown()

    @patch('lmkp.views.stakeholders.get_output_format')
    def test_read_many_calls_output_format(self, mock_get_output_format):
        mock_get_output_format.return_value = self.request.matchdict.get(
            'output')
        self.view.read_many()
        mock_get_output_format.assert_called_once_with(self.request)

    def test_read_many_returns_404_if_no_output_format_found(self):
        self.request.matchdict = {'output': 'foo'}
        with self.assertRaises(HTTPNotFound):
            self.view.read_many()


@pytest.mark.usefixtures('app')
@pytest.mark.unittest
@pytest.mark.stakeholders
class StakeholderViewReadOneTests(LmkpTestCase):

    def setUp(self):
        self.request = testing.DummyRequest()
        self.request.matchdict = {'output': 'json', 'uid': str(uuid4())}
        settings = get_settings()
        self.config = testing.setUp(request=self.request, settings=settings)
        self.view = StakeholderView(self.request)

    def tearDown(self):
        testing.tearDown()

    @patch('lmkp.views.stakeholders.get_output_format')
    def test_read_one_calls_output_format(self, mock_get_output_format):
        mock_get_output_format.return_value = self.request.matchdict.get(
            'output')
        self.view.read_one()
        mock_get_output_format.assert_called_once_with(self.request)

    def test_read_one_returns_404_if_no_output_format_found(self):
        self.request.matchdict = {'output': 'foo'}
        with self.assertRaises(HTTPNotFound):
            self.view.read_one()

    @patch('lmkp.views.stakeholders.validate_uuid')
    def test_read_one_calls_validate_uuid(self, mock_validate_uuid):
        mock_validate_uuid.return_value = True
        self.view.read_one()
        mock_validate_uuid.assert_called_once_with(
            self.request.matchdict['uid'])


@pytest.mark.usefixtures('app')
@pytest.mark.unittest
@pytest.mark.stakeholders
class StakeholderViewReadManyPublicTests(LmkpTestCase):

    def setUp(self):
        self.request = testing.DummyRequest()
        self.request.matchdict = {'output': 'json'}
        settings = get_settings()
        self.config = testing.setUp(request=self.request, settings=settings)
        self.view = StakeholderView(self.request)

    def tearDown(self):
        testing.tearDown()

    def test_read_many_public_returns_404_if_no_output_format_found(self):
        self.request.matchdict = {'output': 'foo'}
        with self.assertRaises(HTTPNotFound):
            self.view.read_many_public()


@pytest.mark.usefixtures('app')
@pytest.mark.unittest
@pytest.mark.stakeholders
class StakeholderViewReadManyByActivitiesTests(LmkpTestCase):

    def setUp(self):
        self.request = testing.DummyRequest()
        self.request.matchdict = {'output': 'json', 'uids': str(uuid4())}
        settings = get_settings()
        self.config = testing.setUp(request=self.request, settings=settings)
        self.view = StakeholderView(self.request)

    def tearDown(self):
        testing.tearDown()

    @patch('lmkp.views.stakeholders.get_output_format')
    @patch.object(StakeholderProtocol, 'read_many')
    def test_read_many_by_activities_calls_output_format(
            self, mock_protocol_read_many, mock_get_output_format):
        mock_get_output_format.return_value = self.request.matchdict.get(
            'output')
        mock_protocol_read_many.return_value = []
        self.view.by_activities()
        mock_get_output_format.assert_called_once_with(self.request)

    def test_read_many_by_activities_returns_404_if_no_output_format_found(
            self):
        self.request.matchdict['output'] = 'foo'
        with self.assertRaises(HTTPNotFound):
            self.view.by_activities()


@pytest.mark.usefixtures('app')
@pytest.mark.unittest
@pytest.mark.stakeholders
class StakeholderViewReadManyJsonTests(LmkpTestCase):

    def setUp(self):
        self.request = testing.DummyRequest()
        self.request.matchdict = {'output': 'json'}
        settings = get_settings()
        self.config = testing.setUp(request=self.request, settings=settings)
        self.view = StakeholderView(self.request)

    def tearDown(self):
        testing.tearDown()

    @patch.object(StakeholderProtocol, 'read_many')
    def test_read_many_json_calls_stakeholder_protocol(
            self, mock_protocol_read_many):
        mock_protocol_read_many.return_value = []
        self.view.read_many()
        mock_protocol_read_many.assert_called_once_with(public_query=False)

    @patch('lmkp.views.stakeholders.render_to_response')
    @patch.object(StakeholderProtocol, 'read_many')
    def test_read_many_json_calls_render_to_response(
            self, mock_protocol_read_many, mock_render_to_response):
        mock_protocol_read_many.return_value = []
        self.view.read_many()
        mock_render_to_response.assert_called_once_with(
            'json', mock_protocol_read_many.return_value, self.request)


@pytest.mark.usefixtures('app')
@pytest.mark.unittest
@pytest.mark.stakeholders
class StakeholderViewReadOneJsonTests(LmkpTestCase):

    def setUp(self):
        self.request = testing.DummyRequest()
        self.request.matchdict = {'output': 'json', 'uid': str(uuid4())}
        settings = get_settings()
        self.config = testing.setUp(request=self.request, settings=settings)
        self.view = StakeholderView(self.request)

    def tearDown(self):
        testing.tearDown()

    @patch('lmkp.views.stakeholders.stakeholder_protocol.read_one')
    def test_read_one_json_calls_stakeholder_protocol(
            self, mock_protocol_read_one):
        mock_protocol_read_one.return_value = []
        self.view.read_one()
        mock_protocol_read_one.assert_called_once_with(
            self.request, uid=self.request.matchdict['uid'], public=False,
            translate=True)

    @patch('lmkp.views.stakeholders.render_to_response')
    @patch('lmkp.views.stakeholders.stakeholder_protocol.read_one')
    def test_read_one_json_calls_render_to_response(
            self, mock_protocol_read_one, mock_render_to_response):
        mock_protocol_read_one.return_value = []
        self.view.read_one()
        mock_render_to_response.assert_called_once_with(
            'json', mock_protocol_read_one.return_value, self.request)

    @patch('lmkp.views.stakeholders.stakeholder_protocol.read_one')
    def test_read_one_json_calls_stakeholder_protocol_translated(
            self, mock_protocol_read_one):
        mock_protocol_read_one.return_value = []
        self.request.params = {'translate': 'false'}
        self.view.read_one()
        mock_protocol_read_one.assert_called_once_with(
            self.request, uid=self.request.matchdict['uid'], public=False,
            translate=False)


@pytest.mark.usefixtures('app')
@pytest.mark.unittest
@pytest.mark.stakeholders
class StakeholderViewReadManyPublicJsonTests(LmkpTestCase):

    def setUp(self):
        self.request = testing.DummyRequest()
        self.request.matchdict = {'output': 'json'}
        settings = get_settings()
        self.config = testing.setUp(request=self.request, settings=settings)
        self.view = StakeholderView(self.request)

    def tearDown(self):
        testing.tearDown()

    @patch('lmkp.views.stakeholders.StakeholderView.read_many')
    def test_read_many_json_calls_stakeholder_protocol(
            self, mock_read_many):
        self.view.read_many_public()
        mock_read_many.assert_called_once_with(public=True)


@pytest.mark.usefixtures('app')
@pytest.mark.unittest
@pytest.mark.stakeholders
class StakeholderViewReadManyByActivitiesPublicTests(LmkpTestCase):

    def setUp(self):
        self.request = testing.DummyRequest()
        self.request.matchdict = {'output': 'json', 'uids': str(uuid4())}
        settings = get_settings()
        self.config = testing.setUp(request=self.request, settings=settings)
        self.view = StakeholderView(self.request)

    def tearDown(self):
        testing.tearDown()

    @patch('lmkp.views.stakeholders.StakeholderView.by_activities')
    def test_read_many_by_activities_json_calls_by_activities(
            self, mock_by_activities):
        self.view.by_activities_public()
        mock_by_activities.assert_called_once_with(public=True)


@pytest.mark.usefixtures('app')
@pytest.mark.unittest
@pytest.mark.stakeholders
class StakeholderViewReadManyByActivitiesJsonTests(LmkpTestCase):

    def setUp(self):
        self.request = testing.DummyRequest()
        self.request.matchdict = {'output': 'json', 'uids': str(uuid4())}
        settings = get_settings()
        self.config = testing.setUp(request=self.request, settings=settings)
        self.view = StakeholderView(self.request)

    def tearDown(self):
        testing.tearDown()

    @patch.object(StakeholderProtocol, 'read_many')
    def test_read_many_by_activities_json_calls_protocol_single_uid(
            self, mock_protocol_read_many):
        mock_protocol_read_many.return_value = []
        self.view.by_activities()
        mock_protocol_read_many.assert_called_once_with(
            public_query=False,
            other_identifiers=[self.request.matchdict.get('uids')])

    @patch.object(StakeholderProtocol, 'read_many')
    def test_read_many_by_activities_json_calls_protocol_single_invalid_uid(
            self, mock_protocol_read_many):
        self.request.matchdict['uids'] = 'foo'
        mock_protocol_read_many.return_value = []
        self.view.by_activities()
        mock_protocol_read_many.assert_called_once_with(
            public_query=False,
            other_identifiers=[])

    @patch.object(StakeholderProtocol, 'read_many')
    def test_read_many_by_activities_json_calls_protocol_many_uids(
            self, mock_protocol_read_many):
        uids = [str(uuid4()), str(uuid4())]
        self.request.matchdict['uids'] = ','.join(uids)
        mock_protocol_read_many.return_value = []
        self.view.by_activities()
        mock_protocol_read_many.assert_called_once_with(
            public_query=False, other_identifiers=uids)

    @patch.object(StakeholderProtocol, 'read_many')
    def test_read_many_by_activities_json_calls_protocol_many_valid_uids(
            self, mock_protocol_read_many):
        uid_1 = uuid4()
        uid_2 = uuid4()
        uid_called = [str(uid_1), str(uid_2), 'foo']
        uid_received = [str(uid_1), str(uid_2)]
        self.request.matchdict['uids'] = ','.join(uid_called)
        mock_protocol_read_many.return_value = []
        self.view.by_activities()
        mock_protocol_read_many.assert_called_once_with(
            public_query=False, other_identifiers=uid_received)

    @patch('lmkp.views.stakeholders.validate_uuid')
    @patch.object(StakeholderProtocol, 'read_many')
    def test_read_many_by_activities_json_calls_validate_uuid(
            self, mock_protocol_read_many, mock_validate_uuid):
        uid_called = [str(uuid4()), str(uuid4()), 'foo']
        self.request.matchdict['uids'] = ','.join(uid_called)
        mock_protocol_read_many.return_value = []
        self.view.by_activities()
        mock_validate_uuid.assert_called_with('foo')


@pytest.mark.usefixtures('app')
@pytest.mark.unittest
@pytest.mark.stakeholders
class StakeholderViewReadManyFormTests(LmkpTestCase):

    def setUp(self):
        self.request = testing.DummyRequest()
        self.request.matchdict = {'output': 'form'}
        self.request.translate = Mock()
        settings = get_settings()
        self.config = testing.setUp(request=self.request, settings=settings)
        self.view = StakeholderView(self.request)

    def tearDown(self):
        testing.tearDown()

    def test_read_many_form_requires_login(self):
        with self.assertRaises(HTTPForbidden):
            self.view.read_many()


@pytest.mark.usefixtures('app')
@pytest.mark.unittest
@pytest.mark.stakeholders
class StakeholderViewReadManyHtmlTests(LmkpTestCase):

    def setUp(self):
        self.request = testing.DummyRequest()
        self.request.matchdict = {'output': 'html'}
        settings = get_settings()
        self.config = testing.setUp(request=self.request, settings=settings)
        self.view = StakeholderView(self.request)

    def tearDown(self):
        testing.tearDown()

    @patch('lmkp.views.stakeholders.get_page_parameters')
    @patch('lmkp.views.stakeholders.render_to_response')
    def test_read_many_html_calls_get_page_parameters(
            self, mock_render_to_response, mock_get_page_parameters):
        mock_render_to_response.return_value = {}
        mock_get_page_parameters.return_value = 1, 1
        self.view.read_many()
        mock_get_page_parameters.assert_called_once_with(self.request)

    @patch.object(StakeholderProtocol, 'read_many')
    @patch('lmkp.views.stakeholders.render_to_response')
    def test_read_many_json_calls_stakeholder_protocol(
            self, mock_render_to_response, mock_protocol_read_many):
        mock_render_to_response.return_value = {}
        mock_protocol_read_many.return_value = []
        self.view.read_many()
        mock_protocol_read_many.assert_called_once_with(
            public_query=False, limit=10, offset=0)

    @patch('lmkp.views.stakeholders.get_status_parameter')
    @patch('lmkp.views.stakeholders.render_to_response')
    def test_read_many_html_calls_get_status_parameter(
            self, mock_render_to_response, mock_get_status_parameter):
        mock_render_to_response.return_value = {}
        mock_get_status_parameter.return_value = 'foo'
        self.view.read_many()
        mock_get_status_parameter.assert_called_once_with(self.request)

    @patch('lmkp.views.stakeholders.BaseView.get_base_template_values')
    @patch('lmkp.views.stakeholders.render_to_response')
    def test_read_many_html_calls_get_base_template_values(
            self, mock_render_to_response, mock_get_base_template_values):
        mock_render_to_response.return_value = {}
        self.view.read_many()
        mock_get_base_template_values.assert_called_once_with()

    @patch('lmkp.views.stakeholders.handle_query_string')
    @patch('lmkp.views.stakeholders.BaseView.get_base_template_values')
    @patch('lmkp.views.stakeholders.render_to_response')
    @patch('lmkp.views.stakeholders.get_customized_template_path')
    def test_read_many_html_calls_render_to_response(
            self, get_customized_template_path, mock_render_to_response,
            mock_get_base_template_values, mock_handle_query_string):
        mock_render_to_response.return_value = {}
        mock_get_base_template_values.return_value = {
            'profile': 'profile',
            'locale': 'en'
        }
        get_customized_template_path.return_value = 'template_path'
        self.view.read_many()
        mock_render_to_response.assert_called_once_with(
            'template_path',
            {
                'profile': 'profile',
                'statusfilter': None,
                'spatialfilter': None,
                'pagesize': 10,
                'currentpage': 1,
                'locale': 'en',
                'total': 0,
                'data': [],
                'invfilter': None,
                'is_moderator': None,
                'handle_query_string': mock_handle_query_string
            },
            self.request)


@pytest.mark.usefixtures('app')
@pytest.mark.unittest
@pytest.mark.stakeholders
class StakeholderViewReadManyByActivitiesHtmlTests(LmkpTestCase):

    def setUp(self):
        self.request = testing.DummyRequest()
        self.request.matchdict = {'output': 'html', 'uids': str(uuid4())}
        settings = get_settings()
        self.config = testing.setUp(request=self.request, settings=settings)
        self.view = StakeholderView(self.request)

    def tearDown(self):
        testing.tearDown()

    @patch('lmkp.views.stakeholders.get_page_parameters')
    @patch('lmkp.views.stakeholders.render_to_response')
    @patch.object(StakeholderProtocol, 'read_many')
    def test_read_by_activities_html_calls_get_page_parameters(
            self, mock_protocol_read_many, mock_render_to_response,
            mock_get_page_parameters):
        mock_render_to_response.return_value = {}
        mock_protocol_read_many.return_value = []
        mock_get_page_parameters.return_value = 1, 1
        self.view.by_activities()
        mock_get_page_parameters.assert_called_once_with(self.request)

    @patch.object(StakeholderProtocol, 'read_many')
    @patch('lmkp.views.stakeholders.render_to_response')
    def test_read_by_activities_html_calls_stakeholder_protocol(
            self, mock_render_to_response, mock_protocol_read_many):
        mock_render_to_response.return_value = {}
        mock_protocol_read_many.return_value = []
        self.view.by_activities()
        mock_protocol_read_many.assert_called_once_with(
            other_identifiers=[self.request.matchdict.get('uids')],
            public_query=False, limit=10, offset=0)

    @patch('lmkp.views.stakeholders.BaseView.get_base_template_values')
    @patch('lmkp.views.stakeholders.render_to_response')
    @patch.object(StakeholderProtocol, 'read_many')
    def test_read_by_activities_html_calls_get_base_template_values(
            self, mock_protocol_read_many, mock_render_to_response,
            mock_get_base_template_values):
        mock_render_to_response.return_value = {}
        mock_protocol_read_many.return_value = []
        self.view.by_activities()
        mock_get_base_template_values.assert_called_once_with()

    @patch('lmkp.views.stakeholders.handle_query_string')
    @patch('lmkp.views.stakeholders.BaseView.get_base_template_values')
    @patch('lmkp.views.stakeholders.render_to_response')
    @patch('lmkp.views.stakeholders.get_customized_template_path')
    @patch.object(StakeholderProtocol, 'read_many')
    def test_read_by_activities_html_calls_render_to_response(
            self, mock_protocol_read_many, get_customized_template_path,
            mock_render_to_response, mock_get_base_template_values,
            mock_handle_query_string):
        mock_render_to_response.return_value = {}
        mock_protocol_read_many.return_value = []
        mock_get_base_template_values.return_value = {
            'profile': 'profile',
            'locale': 'en'
        }
        get_customized_template_path.return_value = 'template_path'
        self.view.by_activities()
        mock_render_to_response.assert_called_once_with(
            'template_path',
            {
                'profile': 'profile',
                'spatialfilter': None,
                'statusfilter': None,
                'handle_query_string': mock_handle_query_string,
                'pagesize': 10,
                'currentpage': 1,
                'locale': 'en',
                'total': 0,
                'data': [],
                'invfilter': [self.request.matchdict.get('uids')]
            },
            self.request)
