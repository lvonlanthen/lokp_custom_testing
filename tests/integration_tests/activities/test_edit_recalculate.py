import pytest

from ..base import (
    find_key_value_in_taggroups_json,
    get_involvements_from_item_json,
    get_role_id_from_involvement_json,
    get_status_from_item_json,
    get_version_from_involvement_json,
    LmkpTestCase,
)
from ..diffs import (
    get_new_diff,
    get_edit_diff,
)
from ...base import (
    STATUS_ACTIVE,
    STATUS_EDITED,
    STATUS_INACTIVE,
    STATUS_PENDING,
)


@pytest.mark.usefixtures('app')
@pytest.mark.integration
@pytest.mark.activities
class ActivityEditRecalculateTests(LmkpTestCase):

    def setUp(self):
        self.login()

    @pytest.mark.test
    def test_recalculate_xxxxxxxxxxxxxxxxxxx(self):
        uid = self.create('a', get_new_diff(101), return_uid=True)
        self.review('a', uid)
        self.create('a', get_edit_diff(101, uid, version=1))
        self.create('a', get_edit_diff(104, uid, version=1))

        res = self.read_one('a', uid, 'json')
        self.assertEqual(res['total'], 3)
        self.assertEqual(STATUS_PENDING, get_status_from_item_json(res, 0))
        self.assertEqual(STATUS_PENDING, get_status_from_item_json(res, 1))
        self.assertEqual(STATUS_ACTIVE, get_status_from_item_json(res, 2))
        taggroups_v3 = res['data'][0]['taggroups']
        taggroups_v2 = res['data'][1]['taggroups']
        taggroups_v1 = res['data'][2]['taggroups']
        self.assertEqual(len(taggroups_v1), 2)
        self.assertEqual(len(taggroups_v2), 3)
        self.assertEqual(len(taggroups_v3), 2)
        self.assertFalse(find_key_value_in_taggroups_json(
            taggroups_v1, '[A] Checkbox 1', value='[A] Value D1',
            main_tag=True))
        self.assertTrue(find_key_value_in_taggroups_json(
            taggroups_v2, '[A] Checkbox 1', value='[A] Value D1',
            main_tag=True))
        self.assertFalse(find_key_value_in_taggroups_json(
            taggroups_v3, '[A] Checkbox 1', value='[A] Value D1',
            main_tag=True))
        self.assertTrue(find_key_value_in_taggroups_json(
            taggroups_v1, '[A] Dropdown 1', value='[A] Value A1',
            main_tag=True))
        self.assertFalse(find_key_value_in_taggroups_json(
            taggroups_v1, '[A] Dropdown 1', value='[A] Value A2',
            main_tag=True))
        self.assertTrue(find_key_value_in_taggroups_json(
            taggroups_v2, '[A] Dropdown 1', value='[A] Value A1',
            main_tag=True))
        self.assertFalse(find_key_value_in_taggroups_json(
            taggroups_v2, '[A] Dropdown 1', value='[A] Value A2',
            main_tag=True))
        self.assertFalse(find_key_value_in_taggroups_json(
            taggroups_v3, '[A] Dropdown 1', value='[A] Value A1',
            main_tag=True))
        self.assertTrue(find_key_value_in_taggroups_json(
            taggroups_v3, '[A] Dropdown 1', value='[A] Value A2',
            main_tag=True))

    @pytest.mark.test
    def test_recalculate_yyyyyyyyyyyyyyyyyyyy(self):
        uid = self.create('a', get_new_diff(101), return_uid=True)
        self.review('a', uid)
        self.create('a', get_edit_diff(101, uid, version=1))
        self.create('a', get_edit_diff(104, uid, version=1))
        self.review('a', uid, version=2)
        self.review('a', uid, version=3)

        res = self.read_one('a', uid, 'json')
        self.assertEqual(res['total'], 4)
        self.assertEqual(STATUS_ACTIVE, get_status_from_item_json(res, 0))
        self.assertEqual(STATUS_EDITED, get_status_from_item_json(res, 1))
        self.assertEqual(STATUS_INACTIVE, get_status_from_item_json(res, 2))
        self.assertEqual(STATUS_INACTIVE, get_status_from_item_json(res, 3))
        taggroups_v4 = res['data'][0]['taggroups']
        self.assertEqual(len(taggroups_v4), 3)
        self.assertTrue(find_key_value_in_taggroups_json(
            taggroups_v4, '[A] Checkbox 1', value='[A] Value D1',
            main_tag=True))
        self.assertFalse(find_key_value_in_taggroups_json(
            taggroups_v4, '[A] Dropdown 1', value='[A] Value A1',
            main_tag=True))
        self.assertTrue(find_key_value_in_taggroups_json(
            taggroups_v4, '[A] Dropdown 1', value='[A] Value A2',
            main_tag=True))
