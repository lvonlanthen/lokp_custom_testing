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
    STATUS_INACTIVE,
    STATUS_PENDING,
)


@pytest.mark.usefixtures('app')
@pytest.mark.integration
@pytest.mark.activities
class ActivityEditActiveTests(LmkpTestCase):

    def test_active_activity_add_new_taggroup(self):
        self.login()
        uid = self.create('a', get_new_diff(101), return_uid=True)
        self.review('a', uid)
        self.create('a', get_edit_diff(101, uid, version=1))
        res = self.read_one('a', uid, 'json')
        self.assertEqual(res['total'], 2)
        self.assertEqual(STATUS_PENDING, get_status_from_item_json(res, 0))
        self.assertEqual(STATUS_ACTIVE, get_status_from_item_json(res, 1))
        taggroups_v2 = res['data'][0]['taggroups']
        taggroups_v1 = res['data'][1]['taggroups']
        self.assertEqual(len(taggroups_v1), 2)
        self.assertEqual(len(taggroups_v2), 3)
        self.assertFalse(find_key_value_in_taggroups_json(
            taggroups_v1, '[A] Checkbox 1', value='[A] Value D1',
            main_tag=True))
        self.assertTrue(find_key_value_in_taggroups_json(
            taggroups_v2, '[A] Checkbox 1', value='[A] Value D1',
            main_tag=True))

    def test_active_activity_remove_taggroup(self):
        self.login()
        uid = self.create('a', get_new_diff(101), return_uid=True)
        self.review('a', uid)
        self.create('a', get_edit_diff(103, uid, version=1))
        res = self.read_one('a', uid, 'json')
        self.assertEqual(res['total'], 2)
        self.assertEqual(STATUS_PENDING, get_status_from_item_json(res, 0))
        self.assertEqual(STATUS_ACTIVE, get_status_from_item_json(res, 1))
        taggroups_v2 = res['data'][0]['taggroups']
        taggroups_v1 = res['data'][1]['taggroups']
        self.assertEqual(len(taggroups_v1), 2)
        self.assertEqual(len(taggroups_v2), 1)
        self.assertTrue(find_key_value_in_taggroups_json(
            taggroups_v1, '[A] Dropdown 1', value='[A] Value A1',
            main_tag=True))
        self.assertFalse(find_key_value_in_taggroups_json(
            taggroups_v2, '[A] Dropdown 1', value='[A] Value A1',
            main_tag=True))

    def test_active_activity_edit_maintag_of_taggroup(self):
        self.login()
        uid = self.create('a', get_new_diff(101), return_uid=True)
        self.review('a', uid)
        self.create('a', get_edit_diff(104, uid, version=1))
        res = self.read_one('a', uid, 'json')
        self.assertEqual(res['total'], 2)
        self.assertEqual(STATUS_PENDING, get_status_from_item_json(res, 0))
        self.assertEqual(STATUS_ACTIVE, get_status_from_item_json(res, 1))
        taggroups_v2 = res['data'][0]['taggroups']
        taggroups_v1 = res['data'][1]['taggroups']
        self.assertEqual(len(taggroups_v1), 2)
        self.assertEqual(len(taggroups_v2), 2)
        self.assertTrue(find_key_value_in_taggroups_json(
            taggroups_v1, '[A] Dropdown 1', value='[A] Value A1',
            main_tag=True))
        self.assertFalse(find_key_value_in_taggroups_json(
            taggroups_v1, '[A] Dropdown 1', value='[A] Value A2',
            main_tag=True))
        self.assertTrue(find_key_value_in_taggroups_json(
            taggroups_v2, '[A] Dropdown 1', value='[A] Value A2',
            main_tag=True))
        self.assertFalse(find_key_value_in_taggroups_json(
            taggroups_v2, '[A] Dropdown 1', value='[A] Value A1',
            main_tag=True))

    def test_active_activity_edit_tag_of_taggroup(self):
        self.login()
        uid = self.create('a', get_new_diff(105), return_uid=True)
        self.review('a', uid)
        self.create('a', get_edit_diff(107, uid, version=1))
        res = self.read_one('a', uid, 'json')
        self.assertEqual(res['total'], 2)
        self.assertEqual(STATUS_PENDING, get_status_from_item_json(res, 0))
        self.assertEqual(STATUS_ACTIVE, get_status_from_item_json(res, 1))
        taggroups_v2 = res['data'][0]['taggroups']
        taggroups_v1 = res['data'][1]['taggroups']
        self.assertEqual(len(taggroups_v1), 2)
        self.assertEqual(len(taggroups_v2), 2)
        textarea_value_v1 = find_key_value_in_taggroups_json(
            taggroups_v1, '[A] Textarea 1', return_value=True)
        self.assertIn('Foo', textarea_value_v1)
        self.assertNotIn('Bar', textarea_value_v1)
        textarea_value_v2 = find_key_value_in_taggroups_json(
            taggroups_v2, '[A] Textarea 1', return_value=True)
        self.assertIn('Bar', textarea_value_v2)
        self.assertNotIn('Foo', textarea_value_v2)

    def test_active_activity_add_tag_to_taggroup(self):
        self.login()
        uid = self.create('a', get_new_diff(101), return_uid=True)
        self.review('a', uid)
        self.create('a', get_edit_diff(105, uid, version=1))
        res = self.read_one('a', uid, 'json')
        self.assertEqual(res['total'], 2)
        self.assertEqual(STATUS_PENDING, get_status_from_item_json(res, 0))
        self.assertEqual(STATUS_ACTIVE, get_status_from_item_json(res, 1))
        taggroups_v2 = res['data'][0]['taggroups']
        taggroups_v1 = res['data'][1]['taggroups']
        self.assertEqual(len(taggroups_v1), 2)
        self.assertEqual(len(taggroups_v2), 2)
        self.assertTrue(find_key_value_in_taggroups_json(
            taggroups_v1, '[A] Dropdown 1', value='[A] Value A1',
            main_tag=True))
        self.assertFalse(find_key_value_in_taggroups_json(
            taggroups_v1, '[A] Textarea 1'))
        self.assertEqual(len(taggroups_v1[0]['tags']), 1)
        self.assertTrue(find_key_value_in_taggroups_json(
            taggroups_v2, '[A] Dropdown 1', value='[A] Value A1',
            main_tag=True))
        self.assertTrue(find_key_value_in_taggroups_json(
            taggroups_v2, '[A] Textarea 1'))
        self.assertEqual(len(taggroups_v2[0]['tags']), 2)

    def test_active_activity_remove_tag_of_taggroup(self):
        self.login()
        uid = self.create('a', get_new_diff(105), return_uid=True)
        self.review('a', uid)
        self.create('a', get_edit_diff(108, uid, version=1))
        res = self.read_one('a', uid, 'json')
        self.assertEqual(res['total'], 2)
        self.assertEqual(STATUS_PENDING, get_status_from_item_json(res, 0))
        self.assertEqual(STATUS_ACTIVE, get_status_from_item_json(res, 1))
        taggroups_v2 = res['data'][0]['taggroups']
        taggroups_v1 = res['data'][1]['taggroups']
        self.assertEqual(len(taggroups_v1), 2)
        self.assertEqual(len(taggroups_v2), 2)
        self.assertTrue(find_key_value_in_taggroups_json(
            taggroups_v1, '[A] Textarea 1'))
        self.assertFalse(find_key_value_in_taggroups_json(
            taggroups_v2, '[A] Textarea 1'))

    def test_active_edit_attributes_copies_geometry(self):
        self.login()
        uid = self.create('a', get_new_diff(101), return_uid=True)
        self.review('a', uid)
        self.create('a', get_edit_diff(101, uid, version=1))
        res = self.read_one('a', uid, 'json')
        self.assertEqual(res['total'], 2)
        self.assertEqual(STATUS_PENDING, get_status_from_item_json(res, 0))
        self.assertEqual(STATUS_ACTIVE, get_status_from_item_json(res, 1))
        geom_v2 = res['data'][0]['geometry']
        geom_v1 = res['data'][1]['geometry']
        self.assertEqual(geom_v1, geom_v2)

    def test_active_activity_edit_geometry(self):
        self.login()
        uid = self.create('a', get_new_diff(101), return_uid=True)
        self.review('a', uid)
        self.create('a', get_edit_diff(106, uid, version=1))
        res = self.read_one('a', uid, 'json')
        self.assertEqual(res['total'], 2)
        self.assertEqual(STATUS_PENDING, get_status_from_item_json(res, 0))
        self.assertEqual(STATUS_ACTIVE, get_status_from_item_json(res, 1))
        geom_v2 = res['data'][0]['geometry']
        geom_v1 = res['data'][1]['geometry']
        self.assertNotEqual(geom_v1, geom_v2)

    def test_active_activity_add_pending_stakeholder(self):
        """

        """
        self.login()
        # Create a first Stakeholder
        sh_uid = self.create('sh', get_new_diff(201), return_uid=True)
        # Create a first Activity
        a_uid = self.create('a', get_new_diff(101), return_uid=True)
        self.review('a', a_uid)
        # Edit the Activity and add the Stakeholder as involvement
        inv_data1 = [{
            'id': sh_uid,
            'version': 1,
            'role': 6
        }]
        self.create('a', get_edit_diff(102, a_uid, version=1, data=inv_data1))

        # Check that everything was added correctly
        res = self.read_one('a', a_uid, 'json')
        self.assertEqual(res['total'], 2)
        self.assertEqual(STATUS_PENDING, get_status_from_item_json(res, 0))
        self.assertEqual(STATUS_ACTIVE, get_status_from_item_json(res, 1))
        self.assertEqual(len(get_involvements_from_item_json(res, 0)), 1)
        self.assertEqual(len(get_involvements_from_item_json(res, 1)), 0)
        res = self.read_one('sh', sh_uid, 'json')
        self.assertEqual(res['total'], 2)
        self.assertEqual(STATUS_PENDING, get_status_from_item_json(res, 0))
        self.assertEqual(STATUS_PENDING, get_status_from_item_json(res, 1))
        self.assertEqual(len(get_involvements_from_item_json(res, 0)), 1)
        self.assertEqual(len(get_involvements_from_item_json(res, 1)), 0)

    def test_active_activity_add_active_stakeholder(self):
        self.login()
        # Create and review first Stakeholder
        sh_uid = self.create('sh', get_new_diff(201), return_uid=True)
        self.review('sh', sh_uid)
        # Create a first Activity
        a_uid = self.create('a', get_new_diff(101), return_uid=True)
        self.review('a', a_uid)
        # Edit the Activity and add the Stakeholder as involvement
        inv_data1 = [{
            'id': sh_uid,
            'version': 1,
            'role': 6
        }]
        self.create('a', get_edit_diff(102, a_uid, version=1, data=inv_data1))

        # Check that everything was added correctly
        res = self.read_one('a', a_uid, 'json')
        self.assertEqual(res['total'], 2)
        self.assertEqual(STATUS_PENDING, get_status_from_item_json(res, 0))
        self.assertEqual(STATUS_ACTIVE, get_status_from_item_json(res, 1))
        self.assertEqual(len(get_involvements_from_item_json(res, 0)), 1)
        self.assertEqual(len(get_involvements_from_item_json(res, 1)), 0)
        res = self.read_one('sh', sh_uid, 'json')
        self.assertEqual(res['total'], 2)
        self.assertEqual(STATUS_PENDING, get_status_from_item_json(res, 0))
        self.assertEqual(STATUS_ACTIVE, get_status_from_item_json(res, 1))
        self.assertEqual(len(get_involvements_from_item_json(res, 0)), 1)
        self.assertEqual(len(get_involvements_from_item_json(res, 1)), 0)

    def test_active_activity_remove_active_stakeholder(self):
        self.login()
        # Create a first Stakeholder and review it
        sh_uid = self.create('sh', get_new_diff(201), return_uid=True)
        self.review('sh', sh_uid, decision='approve', version=1)
        # Create a first Activity and review it
        a_uid = self.create('a', get_new_diff(101), return_uid=True)
        self.review('a', a_uid)
        # Create the involvement and review it
        inv_data_add = [{
            'id': sh_uid,
            'version': 1,
            'role': 6,
            'op': 'add'
        }]
        self.create(
            'a', get_edit_diff(102, a_uid, version=1, data=inv_data_add))
        self.review('a', a_uid, version=2)
        # Edit the Activity and remove the involvement
        inv_data_delete = [{
            'id': sh_uid,
            'version': 2,
            'role': 6,
            'op': 'delete'
        }]
        self.create(
            'a', get_edit_diff(102, a_uid, version=2, data=inv_data_delete))

        # On Activity side, there are 3 versions:
        # [0] v3: without involvement, pending.
        # [1] v2: with involvement, active.
        # [2] v1: without involvement, inactive.
        res = self.read_one('a', a_uid, 'json')
        self.assertEqual(res['total'], 3)
        self.assertEqual(STATUS_PENDING, get_status_from_item_json(res, 0))
        self.assertEqual(STATUS_ACTIVE, get_status_from_item_json(res, 1))
        self.assertEqual(STATUS_INACTIVE, get_status_from_item_json(res, 2))
        self.assertEqual(len(get_involvements_from_item_json(res, 0)), 0)
        self.assertEqual(len(get_involvements_from_item_json(res, 1)), 1)
        self.assertEqual(len(get_involvements_from_item_json(res, 2)), 0)

        # On Stakeholder side, there are 3 versions:
        # [0] v3: without involvement, pending.
        # [1] v2: with involvement to v1 of Activity, active.
        # [2] v1: blank Stakeholder, no involvements, inactive.
        res = self.read_one('sh', sh_uid, 'json')
        self.assertEqual(res['total'], 3)
        self.assertEqual(STATUS_PENDING, get_status_from_item_json(res, 0))
        self.assertEqual(STATUS_ACTIVE, get_status_from_item_json(res, 1))
        self.assertEqual(STATUS_INACTIVE, get_status_from_item_json(res, 2))
        self.assertEqual(len(get_involvements_from_item_json(res, 0)), 0)
        self.assertEqual(len(get_involvements_from_item_json(res, 1)), 1)
        self.assertEqual(len(get_involvements_from_item_json(res, 2)), 0)

    def test_involvement_attribute_change_does_not_touch_attributes(self):
        self.login()
        # Create a Stakeholder
        sh_uid = self.create('sh', get_new_diff(201), return_uid=True)
        self.review('sh', sh_uid, decision='approve', version=1)
        inv_data = [{
            'id': sh_uid,
            'version': 1,
            'role': 1,
            'op': 'add'
        }]
        a_uid = self.create(
            'a', get_new_diff(103, data=inv_data), return_uid=True)
        self.review('a', a_uid)
        # Edit the Stakeholder
        self.create('sh', get_edit_diff(201, sh_uid, version=2))

        # On Activity side, there is 1 version:
        # [0] v1: with involvement to v3 of Stakeholder, pending.
        res = self.read_one('a', a_uid, 'json')
        self.assertEqual(res['total'], 1)
        self.assertEqual(STATUS_ACTIVE, get_status_from_item_json(res, 0))
        inv = get_involvements_from_item_json(res, 0)
        self.assertEqual(len(inv), 1)
        self.assertEqual(get_version_from_involvement_json(inv, 0), 3)

        # On Stakeholder side, there are 3 versions:
        # [0] v3: with involvement, pending.
        # [1] v2: with involvement, active.
        # [2] v1: no involvement, inactive.
        res = self.read_one('sh', sh_uid, 'json')
        self.assertEqual(res['total'], 3)
        self.assertEqual(STATUS_PENDING, get_status_from_item_json(res, 0))
        self.assertEqual(STATUS_ACTIVE, get_status_from_item_json(res, 1))
        self.assertEqual(STATUS_INACTIVE, get_status_from_item_json(res, 2))
        self.assertEqual(len(get_involvements_from_item_json(res, 0)), 1)
        self.assertEqual(len(get_involvements_from_item_json(res, 1)), 1)
        self.assertEqual(len(get_involvements_from_item_json(res, 2)), 0)
