import pytest
from mock import patch
from pyramid import testing

from lmkp.views.views import (
    BaseView,
    get_bbox_parameters,
    get_output_format,
    get_page_parameters,
    get_status_parameter,
    get_current_profile,
    get_current_attribute_filters,
    get_current_logical_filter_operator,
    get_current_order_key,
    get_current_order_direction,
    get_current_involvement_details,
    get_current_limit,
    get_current_offset,
    get_current_translation_parameter,
    get_current_taggroup_geometry_parameter,
    get_current_attributes,
)
from ...integration_tests.base import (
    LmkpTestCase,
)
from ...base import get_settings


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


@pytest.mark.unittest
@pytest.mark.profile
@pytest.mark.views
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


@pytest.mark.unittest
@pytest.mark.filter
@pytest.mark.views
class ViewsGetCurrentAttributeFiltersTests(LmkpTestCase):

    def setUp(self):
        self.request = testing.DummyRequest()
        settings = get_settings()
        self.config = testing.setUp(request=self.request, settings=settings)

    def tearDown(self):
        testing.tearDown()

    def test_get_current_attribute_filters_returns_empty_array(self):
        filters = get_current_attribute_filters(self.request)
        self.assertEqual(filters, [])

    def test_get_current_attribute_filters_returns_filters(self):
        self.request.params = {
            'a__foo1__eq': 'bar1',
            'sh__foo2__ne': 'bar2'
        }
        filters = get_current_attribute_filters(self.request)
        self.assertEqual(len(filters), 2)
        filter1 = filters[0]
        self.assertEqual(len(filter1), 4)
        self.assertEqual(filter1[0], 'a')
        self.assertEqual(filter1[1], 'foo1')
        self.assertEqual(filter1[2], 'eq')
        self.assertEqual(filter1[3], 'bar1')
        filter2 = filters[1]
        self.assertEqual(len(filter2), 4)
        self.assertEqual(filter2[0], 'sh')
        self.assertEqual(filter2[1], 'foo2')
        self.assertEqual(filter2[2], 'ne')
        self.assertEqual(filter2[3], 'bar2')

    def test_get_current_attribute_filters_ignores_incorrect_prefix(self):
        self.request.params = {
            'foo__foo__eq': 'bar'
        }
        filters = get_current_attribute_filters(self.request)
        self.assertEqual(filters, [])

    def test_get_current_attribute_filters_handles_invalid_input(self):
        self.request.params = {
            'foo__foo': 'bar',
            'foo__foo__foo__foo': 'bar'
        }
        filters = get_current_attribute_filters(self.request)
        self.assertEqual(filters, [])


@pytest.mark.unittest
@pytest.mark.filter
@pytest.mark.views
class ViewsGetLogicalFilterOperatorTests(LmkpTestCase):

    def setUp(self):
        self.request = testing.DummyRequest()
        settings = get_settings()
        self.config = testing.setUp(request=self.request, settings=settings)

    def tearDown(self):
        testing.tearDown()

    def test_get_logical_filter_operator_returns_default(self):
        op = get_current_logical_filter_operator(self.request)
        self.assertEqual(op, 'and')

    def test_get_logical_filter_operator_returns_operator(self):
        self.request.params = {'logical_op': 'or'}
        op = get_current_logical_filter_operator(self.request)
        self.assertEqual(op, 'or')

    def test_get_logical_filter_operator_handles_invalid_operator(self):
        self.request.params = {'logical_op': 'foo'}
        op = get_current_logical_filter_operator(self.request)
        self.assertEqual(op, 'and')


@pytest.mark.unittest
@pytest.mark.views
class ViewsGetCurrentOrderKeyTests(LmkpTestCase):

    def setUp(self):
        self.request = testing.DummyRequest()
        settings = get_settings()
        self.config = testing.setUp(request=self.request, settings=settings)

    def tearDown(self):
        testing.tearDown()

    def test_get_current_order_key_returns_default(self):
        key = get_current_order_key(self.request)
        self.assertEqual(key, 'timestamp')

    def test_get_current_order_key_returns_order_key(self):
        self.request.params = {'order_by': 'foo'}
        key = get_current_order_key(self.request)
        self.assertEqual(key, 'foo')


@pytest.mark.unittest
@pytest.mark.views
class ViewsGetCurrentOrderDirectionTetss(LmkpTestCase):

    def setUp(self):
        self.request = testing.DummyRequest()
        settings = get_settings()
        self.config = testing.setUp(request=self.request, settings=settings)

    def tearDown(self):
        testing.tearDown()

    def test_get_current_order_direction_returns_default(self):
        direction = get_current_order_direction(self.request)
        self.assertEqual(direction, 'desc')

    def test_get_current_order_direction_returns_order_direction(self):
        self.request.params = {'dir': 'asc'}
        direction = get_current_order_direction(self.request)
        self.assertEqual(direction, 'asc')

    def test_get_current_order_direction_handles_invalid_direction(self):
        self.request.params = {'dir': 'foo'}
        direction = get_current_order_direction(self.request)
        self.assertEqual(direction, 'desc')


@pytest.mark.unittest
@pytest.mark.views
class ViewsGetCurrentInvolvementDetailsTests(LmkpTestCase):

    def setUp(self):
        self.request = testing.DummyRequest()
        settings = get_settings()
        self.config = testing.setUp(request=self.request, settings=settings)

    def tearDown(self):
        testing.tearDown()

    def test_get_current_involvement_details_returns_default(self):
        details = get_current_involvement_details(self.request)
        self.assertEqual(details, 'full')

    def test_get_current_involvement_details_returns_details(self):
        self.request.params = {'involvements': 'none'}
        details = get_current_involvement_details(self.request)
        self.assertEqual(details, 'none')

    def test_get_current_involvement_details_handles_invalid_keyword(self):
        self.request.params = {'involvements': 'foo'}
        details = get_current_involvement_details(self.request)
        self.assertEqual(details, 'full')


@pytest.mark.unittest
@pytest.mark.views
class ViewsGetCurrentLimitTests(LmkpTestCase):

    def setUp(self):
        self.request = testing.DummyRequest()
        settings = get_settings()
        self.config = testing.setUp(request=self.request, settings=settings)

    def tearDown(self):
        testing.tearDown()

    def test_get_current_limit_returns_default(self):
        limit = get_current_limit(self.request)
        self.assertIsNone(limit)

    def test_get_current_limit_returns_limit(self):
        self.request.params = {'limit': 15}
        limit = get_current_limit(self.request)
        self.assertEqual(limit, 15)

    def test_get_current_limit_returns_absolute_limit(self):
        self.request.params = {'limit': -15}
        limit = get_current_limit(self.request)
        self.assertEqual(limit, 15)

    def test_get_current_limit_handles_invalid_limit(self):
        self.request.params = {'limit': 'foo'}
        limit = get_current_limit(self.request)
        self.assertIsNone(limit)


@pytest.mark.unittest
@pytest.mark.views
class ViewsGetCurrentOffsetTests(LmkpTestCase):

    def setUp(self):
        self.request = testing.DummyRequest()
        settings = get_settings()
        self.config = testing.setUp(request=self.request, settings=settings)

    def tearDown(self):
        testing.tearDown()

    def test_get_current_offset_returns_default(self):
        offset = get_current_offset(self.request)
        self.assertEqual(offset, 0)

    def test_get_current_offset_returns_limit(self):
        self.request.params = {'offset': 15}
        offset = get_current_offset(self.request)
        self.assertEqual(offset, 15)

    def test_get_current_offset_returns_absolute_offset(self):
        self.request.params = {'offset': -15}
        offset = get_current_offset(self.request)
        self.assertEqual(offset, 15)

    def test_get_current_offset_handles_invalid_limit(self):
        self.request.params = {'offset': 'foo'}
        offset = get_current_offset(self.request)
        self.assertEqual(offset, 0)


@pytest.mark.unittest
@pytest.mark.views
class ViewsGetCurrentTranslationParameterTests(LmkpTestCase):

    def test_get_current_translation_parameter_returns_default(self):
        translate = get_current_translation_parameter(self.request)
        self.assertTrue(translate)

    def test_get_current_translation_parameter_returns_parameter_false(self):
        self.request.params = {'translate': 'false'}
        translate = get_current_translation_parameter(self.request)
        self.assertFalse(translate)

    def test_get_current_translation_parameter_returns_parameter_foo(self):
        self.request.params = {'translate': 'foo'}
        translate = get_current_translation_parameter(self.request)
        self.assertTrue(translate)

    def test_get_current_translation_parameter_returns_parameter_true(self):
        self.request.params = {'translate': 'true'}
        translate = get_current_translation_parameter(self.request)
        self.assertTrue(translate)


@pytest.mark.unittest
@pytest.mark.views
class ViewsGetCurrentTaggroupGeometryParameterTests(LmkpTestCase):

    def test_get_current_taggroup_geometry_parameter_returns_default(self):
        translate = get_current_taggroup_geometry_parameter(self.request)
        self.assertFalse(translate)

    def test_get_current_taggroup_geometry_parameter_returns_parameter_false(
            self):
        self.request.params = {'taggroup_geometry': 'false'}
        translate = get_current_taggroup_geometry_parameter(self.request)
        self.assertFalse(translate)

    def test_get_current_taggroup_geometry_parameter_returns_parameter_foo(
            self):
        self.request.params = {'taggroup_geometry': 'foo'}
        translate = get_current_taggroup_geometry_parameter(self.request)
        self.assertFalse(translate)

    def test_get_current_taggroup_geometry_parameter_returns_parameter_true(
            self):
        self.request.params = {'taggroup_geometry': 'true'}
        translate = get_current_taggroup_geometry_parameter(self.request)
        self.assertTrue(translate)

    def test_get_current_taggroup_geometry_parameter_tggeom(self):
        self.request.params = {'tggeom': 'false'}
        translate = get_current_taggroup_geometry_parameter(self.request)
        self.assertFalse(translate)

    def test_get_current_taggroup_geometry_parameter_tggeom_lower_priority(
            self):
        self.request.params = {'taggroup_geometry': 'false', 'tggeom': 'true'}
        translate = get_current_taggroup_geometry_parameter(self.request)
        self.assertFalse(translate)


@pytest.mark.unittest
@pytest.mark.views
class ViewsGetCurrentAttributesTests(LmkpTestCase):

    def test_get_current_attributes_returns_empty_list(self):
        attributes = get_current_attributes(self.request)
        self.assertEqual(attributes, [])

    def test_get_current_attributes_returns_single_attribute(self):
        self.request.params = {'attributes': 'foo'}
        attributes = get_current_attributes(self.request)
        self.assertEqual(len(attributes), 1)
        self.assertEqual(attributes[0], 'foo')

    def test_get_current_attributes_returns_multiple_attributes(self):
        self.request.params = {'attributes': 'foo,bar'}
        attributes = get_current_attributes(self.request)
        self.assertEqual(len(attributes), 2)
        self.assertEqual(attributes[0], 'foo')
        self.assertEqual(attributes[1], 'bar')

    def test_get_current_attributes_attrs_param(self):
        self.request.params = {'attrs': 'foo'}
        attributes = get_current_attributes(self.request)
        self.assertEqual(len(attributes), 1)
        self.assertEqual(attributes[0], 'foo')

    def test_get_current_attributes_attrs_lower_priority(self):
        self.request.params = {'attributes': 'foo,bar', 'attrs': 'asdf'}
        attributes = get_current_attributes(self.request)
        self.assertEqual(len(attributes), 2)
        self.assertEqual(attributes[0], 'foo')
        self.assertEqual(attributes[1], 'bar')
