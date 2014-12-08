import pytest
import uuid

from ..integration_tests.base import LmkpTestCase
from lmkp.utils import (
    handle_query_string,
    validate_bbox,
    validate_item_type,
    validate_uuid,
)


@pytest.mark.unittest
@pytest.mark.utils
class ValidateBboxTests(LmkpTestCase):

    def test_validate_bbox_handles_invalid_input(self):
        self.assertIsNone(validate_bbox(None))
        self.assertIsNone(validate_bbox({}))
        self.assertIsNone(validate_bbox('foo'))
        self.assertIsNone(validate_bbox('foo,bar,abc'))
        self.assertIsNone(validate_bbox('foo,bar,abc,def'))
        self.assertIsNone(validate_bbox('1,2,foo,3'))
        self.assertIsNone(validate_bbox('1,2,3,4,5'))

    def test_validate_bbox_returns_list(self):
        bbox = validate_bbox('1, 2.34, 3, 4')
        self.assertIsInstance(bbox, list)
        self.assertEqual(len(bbox), 4)

    def test_validate_bbox_returns_list_of_floats(self):
        bbox = validate_bbox('1,2.34,3,4')
        for b in bbox:
            self.assertIsInstance(b, float)


@pytest.mark.unittest
@pytest.mark.utils
class ValidateItemTypeTests(LmkpTestCase):

    def test_validate_item_type_handles_invalid_input(self):
        invalid_types = [None, {}, 'foo', 3.14159, False]
        for invalid_type in invalid_types:
            with self.assertRaises(Exception):
                validate_item_type(invalid_type)

    def test_validate_item_type_returns_short_representation(self):
        self.assertEqual(validate_item_type('activities'), 'a')
        self.assertEqual(validate_item_type('a'), 'a')
        self.assertEqual(validate_item_type('stakeholders'), 'sh')


@pytest.mark.unittest
@pytest.mark.utils
class ValidateUuidTests(LmkpTestCase):

    def test_validate_uuid_handles_invalid_input(self):
        self.assertFalse(validate_uuid('foo'))
        self.assertFalse(validate_uuid(None))
        self.assertFalse(validate_uuid({}))
        self.assertFalse(validate_uuid('xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx'))
        self.assertFalse(validate_uuid('87b9ce04-ad4a-4a8c-84af-8e9643f8701x'))
        self.assertFalse(validate_uuid('87b9ce04-ad4a-4a8c-84af-8e9643f8701'))

    def test_validate_uuid_handles_valid_input(self):
        self.assertTrue(validate_uuid(str(uuid.uuid4())))
        self.assertTrue(validate_uuid('EC856438-08BE-4842-963A-47A7E723543F'))
        self.assertTrue(validate_uuid(
            unicode('87b9ce04-ad4a-4a8c-84af-8e9643f8701a')))


@pytest.mark.unittest
@pytest.mark.utils
class ViewsHandleQueryStringTests(LmkpTestCase):

    def setUp(self):
        self.url = 'http://www.foo.com/foo'
        self.url2 = '%s?foo=bar' % self.url

    def test_handle_query_string_returns_url_as_is(self):
        self.assertEqual(handle_query_string(self.url), self.url)
        self.assertEqual(handle_query_string(self.url2), self.url2)

    def test_handle_query_string_adds_param(self):
        add = [('foo', 'bar')]
        query_string = handle_query_string(self.url, add=add)
        self.assertEqual(query_string, self.url2)

    def test_handle_query_string_adds_multiple_params(self):
        add = [('foo', 'bar'), ('blu', 'bla')]
        query_string = handle_query_string(self.url, add=add)
        self.assertEqual(query_string, '%s?blu=bla&foo=bar' % self.url)

    def test_handle_query_string_removes_param(self):
        remove = ['foo']
        query_string = handle_query_string(self.url2, remove=remove)
        self.assertEqual(query_string, self.url)

    def test_handle_query_string_removes_multiple_params(self):
        remove = ['foo', 'blu']
        url = '%s?blu=bla&foo=bar' % self.url
        query_string = handle_query_string(url, remove=remove)
        self.assertEqual(query_string, self.url)

    def test_handle_query_string_adds_and_removes_params(self):
        add = [('blu', 'bla')]
        remove = ['foo']
        query_string = handle_query_string(self.url2, add=add, remove=remove)
        self.assertEqual(query_string, '%s?blu=bla' % self.url)

    def test_handle_query_string_always_removes_epsg(self):
        query_string = handle_query_string('%s?epsg=foo' % self.url)
        self.assertEqual(query_string, self.url)

    def test_handle_query_string_always_removes_page(self):
        query_string = handle_query_string('%s?page=foo' % self.url)
        self.assertEqual(query_string, self.url)

    def test_handle_query_string_removes_bbox_if_not_set_to_profile(self):
        query_string = handle_query_string('%s?bbox=foo' % self.url)
        self.assertEqual(query_string, self.url)
        url = '%s?bbox=profile' % self.url
        self.assertEqual(handle_query_string(url), url)

    def test_handle_query_string_returns_only_query_string(self):
        query_string = handle_query_string(
            self.url2, return_value='query_string')
        self.assertEqual(query_string, '?foo=bar')
