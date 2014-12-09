import pytest

from ..base import (
    find_key_value_in_taggroups_json,
    get_involvements_from_item_json,
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
        super(ActivityEditRecalculateTests, self).setUp()

    def test_blublu(self):
        sh_uid = self.create('sh', get_new_diff(201), return_uid=True)
        self.review('sh', sh_uid)
        inv_data = [{
            'id': sh_uid,
            'version': 1,
            'role': 1
        }]
        a_uid = self.create(
            'a', get_new_diff(103, data=inv_data), return_uid=True)
        self.review('a', a_uid)

        self.create('a', get_edit_diff(101, a_uid, version=1))
        self.create('a', get_edit_diff(106, a_uid, version=1))

        self.review('a', a_uid, version=2)
        self.review('a', a_uid, version=3)

        res = self.read_one_history('a', a_uid, 'json')
        self.assertEqual(res['total'], 4)
        self.assertEqual(STATUS_ACTIVE, get_status_from_item_json(res, 0))
        self.assertEqual(STATUS_EDITED, get_status_from_item_json(res, 1))
        self.assertEqual(STATUS_INACTIVE, get_status_from_item_json(res, 2))
        self.assertEqual(STATUS_INACTIVE, get_status_from_item_json(res, 3))

        taggroups_v4 = res['data'][0]['taggroups']
        self.assertEqual(len(taggroups_v4), 3)
        # self.assertTrue(find_key_value_in_taggroups_json(
        #     taggroups_v4, '[A] Checkbox 1', value='[A] Value D1',
        #     main_tag=True))
        inv_v4 = get_involvements_from_item_json(res, 0)
        self.assertEqual(len(inv_v4), 1)

    def test_recalculate_1(self):
        sh_uid = self.create('sh', get_new_diff(201), return_uid=True)
        self.review('sh', sh_uid)
        a_uid = self.create('a', get_new_diff(101), return_uid=True)
        self.review('a', a_uid)
        self.create('a', get_edit_diff(101, a_uid, version=1))
        inv_data = [{
            'id': sh_uid,
            'version': 1,
            'role': 1
        }]
        self.create('a', get_edit_diff(102, a_uid, version=1, data=inv_data))

        res = self.read_one_history('a', a_uid, 'json')
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
        inv_v3 = get_involvements_from_item_json(res, 0)
        inv_v2 = get_involvements_from_item_json(res, 1)
        inv_v1 = get_involvements_from_item_json(res, 2)
        self.assertEqual(len(inv_v1), 0)
        self.assertEqual(len(inv_v2), 0)
        self.assertEqual(len(inv_v3), 1)
        self.assertEqual(get_version_from_involvement_json(inv_v3), 2)

        res = self.read_one_history('sh', sh_uid, 'json')
        self.assertEqual(res['total'], 2)
        self.assertEqual(STATUS_PENDING, get_status_from_item_json(res, 0))
        self.assertEqual(STATUS_ACTIVE, get_status_from_item_json(res, 1))
        inv_v2 = get_involvements_from_item_json(res, 0)
        self.assertEqual(len(inv_v2), 1)
        self.assertEqual(get_version_from_involvement_json(inv_v2), 3)

    # @pytest.mark.test
    def test_recalculate_1_review(self):
        sh_uid = self.create('sh', get_new_diff(201), return_uid=True)
        self.review('sh', sh_uid)
        a_uid = self.create('a', get_new_diff(101), return_uid=True)
        self.review('a', a_uid)
        self.create('a', get_edit_diff(101, a_uid, version=1))
        inv_data = [{
            'id': sh_uid,
            'version': 1,
            'role': 1
        }]
        self.create('a', get_edit_diff(102, a_uid, version=1, data=inv_data))
        self.review('a', a_uid, version=2)
        self.review('a', a_uid, version=3)

        res = self.read_one_history('a', a_uid, 'json')
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
        inv_v4 = get_involvements_from_item_json(res, 0)
        self.assertEqual(len(inv_v4), 1)
        self.assertEqual(get_version_from_involvement_json(inv_v4), 2)

        res = self.read_one_history('sh', sh_uid, 'json')
        self.assertEqual(res['total'], 2)
        self.assertEqual(STATUS_ACTIVE, get_status_from_item_json(res, 0))
        self.assertEqual(STATUS_INACTIVE, get_status_from_item_json(res, 1))
        inv_v2 = get_involvements_from_item_json(res, 0)
        self.assertEqual(len(inv_v2), 1)
        self.assertEqual(get_version_from_involvement_json(inv_v2), 4)

    def test_recalculate_1_review_2(self):
        sh_uid = self.create('sh', get_new_diff(201), return_uid=True)
        self.review('sh', sh_uid)
        a_uid = self.create('a', get_new_diff(101), return_uid=True)
        self.review('a', a_uid)
        self.create('a', get_edit_diff(101, a_uid, version=1))
        inv_data = [{
            'id': sh_uid,
            'version': 1,
            'role': 1
        }]
        self.create('a', get_edit_diff(102, a_uid, version=1, data=inv_data))
        self.review('a', a_uid, version=3)
        self.review('a', a_uid, version=2)

        res = self.read_one_history('a', a_uid, 'json')
        self.assertEqual(res['total'], 4)
        self.assertEqual(STATUS_ACTIVE, get_status_from_item_json(res, 0))
        self.assertEqual(STATUS_INACTIVE, get_status_from_item_json(res, 1))
        self.assertEqual(STATUS_EDITED, get_status_from_item_json(res, 2))
        self.assertEqual(STATUS_INACTIVE, get_status_from_item_json(res, 3))

        taggroups_v4 = res['data'][0]['taggroups']
        self.assertEqual(len(taggroups_v4), 3)
        self.assertTrue(find_key_value_in_taggroups_json(
            taggroups_v4, '[A] Checkbox 1', value='[A] Value D1',
            main_tag=True))
        inv_v4 = get_involvements_from_item_json(res, 0)
        self.assertEqual(len(inv_v4), 1)
        self.assertEqual(get_version_from_involvement_json(inv_v4), 2)

        res = self.read_one_history('sh', sh_uid, 'json')
        self.assertEqual(res['total'], 2)
        self.assertEqual(STATUS_ACTIVE, get_status_from_item_json(res, 0))
        self.assertEqual(STATUS_INACTIVE, get_status_from_item_json(res, 1))
        inv_v2 = get_involvements_from_item_json(res, 0)
        self.assertEqual(len(inv_v2), 1)
        self.assertEqual(get_version_from_involvement_json(inv_v2), 4)

    def test_recalculate_xxxxxxxxxxxxxxxxxxx(self):
        uid = self.create('a', get_new_diff(101), return_uid=True)
        self.review('a', uid)
        self.create('a', get_edit_diff(101, uid, version=1))
        self.create('a', get_edit_diff(104, uid, version=1))

        res = self.read_one_history('a', uid, 'json')
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

    def test_recalculate_yyyyyyyyyyyyyyyyyyyy(self):
        uid = self.create('a', get_new_diff(101), return_uid=True)
        self.review('a', uid)
        self.create('a', get_edit_diff(101, uid, version=1))
        self.create('a', get_edit_diff(104, uid, version=1))
        self.review('a', uid, version=2)
        self.review('a', uid, version=3)

        res = self.read_one_history('a', uid, 'json')
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

    def test_recalculated_activities_can_be_deleted_with_form(self):
        uid = self.create('a', get_new_diff(101), return_uid=True)
        self.review('a', uid)
        self.create('a', get_edit_diff(101, uid, version=1))
        self.app.post(str('/activities/form/%s' % uid), {
            '__formid__': 'activityform',
            'id': uid,
            'version': 2,
            'delete': 'true'
        })

        res = self.read_one_history('a', uid, 'json')
        self.assertEqual(res['total'], 3)
        self.assertEqual(STATUS_PENDING, get_status_from_item_json(res, 0))
        self.assertEqual(STATUS_EDITED, get_status_from_item_json(res, 1))
        self.assertEqual(STATUS_ACTIVE, get_status_from_item_json(res, 2))
        v2_taggroups = res['data'][1]['taggroups']
        v3_taggroups = res['data'][0]['taggroups']
        self.assertEqual(len(v2_taggroups), 3)
        self.assertTrue(find_key_value_in_taggroups_json(
            v2_taggroups, '[A] Dropdown 1'))
        self.assertTrue(find_key_value_in_taggroups_json(
            v2_taggroups, '[A] Numberfield 1'))
        self.assertEqual(len(v3_taggroups), 0)
        self.assertFalse(find_key_value_in_taggroups_json(
            v3_taggroups, '[A] Dropdown 1'))
        self.assertFalse(find_key_value_in_taggroups_json(
            v3_taggroups, '[A] Numberfield 1'))

    def test_activities_with_involvements_can_be_deleted_with_form(self):
        sh_uid = self.create('sh', get_new_diff(201), return_uid=True)
        self.review('sh', sh_uid)
        inv_data = [{
            'id': sh_uid,
            'version': 1,
            'role': 6
        }]
        a_uid = self.create(
            'a', get_new_diff(103, data=inv_data), return_uid=True)
        self.review('a', a_uid)
        self.create('a', get_edit_diff(101, a_uid, version=1))
        self.app.post(str('/activities/form/%s' % a_uid), {
            '__formid__': 'activityform',
            'id': a_uid,
            'version': 2,
            'delete': 'true'
        })

        res = self.read_one_history('a', a_uid, 'json')
        self.assertEqual(res['total'], 3)
        self.assertEqual(STATUS_PENDING, get_status_from_item_json(res, 0))
        self.assertEqual(STATUS_EDITED, get_status_from_item_json(res, 1))
        self.assertEqual(STATUS_ACTIVE, get_status_from_item_json(res, 2))
        v2_taggroups = res['data'][1]['taggroups']
        v3_taggroups = res['data'][0]['taggroups']
        self.assertEqual(len(v2_taggroups), 3)
        self.assertTrue(find_key_value_in_taggroups_json(
            v2_taggroups, '[A] Dropdown 1'))
        self.assertTrue(find_key_value_in_taggroups_json(
            v2_taggroups, '[A] Numberfield 1'))
        self.assertEqual(len(v3_taggroups), 0)
        self.assertFalse(find_key_value_in_taggroups_json(
            v3_taggroups, '[A] Dropdown 1'))
        self.assertFalse(find_key_value_in_taggroups_json(
            v3_taggroups, '[A] Numberfield 1'))
        v2_inv = get_involvements_from_item_json(res, 1)
        v3_inv = get_involvements_from_item_json(res, 0)
        self.assertEqual(len(v2_inv), 1)
        self.assertEqual(len(v3_inv), 0)

        res = self.read_one_history('sh', sh_uid, 'json')
        self.assertEqual(res['total'], 3)
        self.assertEqual(STATUS_PENDING, get_status_from_item_json(res, 0))
        self.assertEqual(STATUS_ACTIVE, get_status_from_item_json(res, 1))
        self.assertEqual(STATUS_INACTIVE, get_status_from_item_json(res, 2))
        v1_inv = get_involvements_from_item_json(res, 2)
        v2_inv = get_involvements_from_item_json(res, 1)
        v3_inv = get_involvements_from_item_json(res, 0)
        self.assertEqual(len(v1_inv), 0)
        self.assertEqual(len(v2_inv), 1)
        self.assertEqual(len(v3_inv), 0)
