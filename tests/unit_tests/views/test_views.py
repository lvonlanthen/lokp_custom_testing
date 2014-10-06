import pytest
from mock import patch
from pyramid import testing

from lmkp.views.views import (
    BaseView,
    get_bbox_parameters,
    get_output_format,
    get_page_parameters,
    get_status_parameter,
    get_current_locale,
    get_current_profile,
)
from ...integration_tests.base import (
    LmkpTestCase,
)
from ...base import get_settings


@pytest.mark.usefixtrues('app')
@pytest.mark.unittest
@pytest.mark.views
class ViewsBaseViewGetBaseTemplateValuesTests(LmkpTestCase):

    def setUp(self):
        self.request = testing.DummyRequest()
        settings = get_settings()
        self.config = testing.setUp(request=self.request, settings=settings)
        self.view = BaseView(self.request)

    def tearDown(self):
        testing.tearDown()

    def test_get_base_template_values_returns_dict(self):
        res = self.view.get_base_template_values()
        self.assertIsInstance(res, dict)

    def test_get_base_template_values_returns_values(self):
        res = self.view.get_base_template_values()
        self.assertIn('profile', res)
        self.assertIn('locale', res)

    @patch('lmkp.views.views.get_current_profile')
    def test_get_base_template_values_calls_get_current_profile(
            self, mock_get_current_profile):
        self.view.get_base_template_values()
        mock_get_current_profile.assert_called_once_with(self.request)

    @patch('lmkp.views.views.get_current_locale')
    def test_get_base_template_values_calls_get_current_locale(
            self, mock_get_current_locale):
        self.view.get_base_template_values()
        mock_get_current_locale.assert_called_once_with(self.request)


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
@pytest.mark.views
class ViewsGetStatusParameterTests(LmkpTestCase):

    def setUp(self):
        self.request = testing.DummyRequest()
        settings = get_settings()
        self.config = testing.setUp(request=self.request, settings=settings)

    def tearDown(self):
        testing.tearDown()

    def test_get_status_parameter_returns_status(self):
        self.request.params = {'status': 'foo'}
        status = get_status_parameter(self.request)
        self.assertEqual(status, 'foo')

    def test_get_status_parameter_returns_none_if_not_set(self):
        status = get_status_parameter(self.request)
        self.assertIsNone(status)


@pytest.mark.usefixtures('app')
@pytest.mark.unittest
@pytest.mark.profile
class ViewsGetCurrentProfileTests(LmkpTestCase):

    def setUp(self):
        self.request = testing.DummyRequest()
        settings = get_settings()
        self.config = testing.setUp(request=self.request, settings=settings)

    def tearDown(self):
        testing.tearDown()

    def test_get_current_profile_returns_global_by_default(self):
        profile = get_current_profile(self.request)
        self.assertEqual(profile, 'global')

    def test_get_current_profile_returns_profile_from_params(self):
        self.request.params = {'_PROFILE_': 'foo'}
        profile = get_current_profile(self.request)
        self.assertEqual(profile, 'foo')

    def test_get_current_profile_returns_profile_from_cookies(self):
        self.request.cookies = {'_PROFILE_': 'foo'}
        profile = get_current_profile(self.request)
        self.assertEqual(profile, 'foo')

    def test_get_current_profile_returns_params_before_cookies(self):
        self.request.cookies = {'_PROFILE_': 'cookie'}
        self.request.params = {'_PROFILE_': 'param'}
        profile = get_current_profile(self.request)
        self.assertEqual(profile, 'param')


@pytest.mark.usefixtures('app')
@pytest.mark.unittest
@pytest.mark.locale
class ViewsGetCurrentLocaleTests(LmkpTestCase):

    def setUp(self):
        self.request = testing.DummyRequest()
        settings = get_settings()
        self.config = testing.setUp(request=self.request, settings=settings)

    def tearDown(self):
        testing.tearDown()

    def test_get_current_locale_returns_en_by_default(self):
        locale = get_current_locale(self.request)
        self.assertEqual(locale, 'en')

    def test_get_current_locale_returns_locale_from_params(self):
        self.request.params = {'_LOCALE_': 'foo'}
        locale = get_current_locale(self.request)
        self.assertEqual(locale, 'foo')

    def test_get_current_locale_returns_locale_from_cookies(self):
        self.request.cookies = {'_LOCALE_': 'foo'}
        locale = get_current_locale(self.request)
        self.assertEqual(locale, 'foo')

    def test_get_current_locale_returns_params_before_cookies(self):
        self.request.cookies = {'_LOCALE_': 'cookie'}
        self.request.params = {'_LOCALE_': 'param'}
        locale = get_current_locale(self.request)
        self.assertEqual(locale, 'param')
