import pytest

from ..integration_tests.base import LmkpTestCase
from lmkp.utils import (
    validate_bbox,
    validate_item_type,
)


@pytest.mark.usefixtures('app')
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


@pytest.mark.usefixtures('app')
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
