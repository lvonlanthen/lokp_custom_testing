import pytest

from ..base import (
    LmkpTestCase,
    find_key_value_in_taggroups_json,
    get_status_from_item_json,
    get_involvements_from_item_json,
)
from ..diffs import (
    get_new_diff,
    get_edit_diff,
)
from ...base import (
    STATUS_EDITED,
    STATUS_PENDING,
)


@pytest.mark.usefixtures('app')
@pytest.mark.integration
@pytest.mark.activities
@pytest.mark.moderation
class ActivityEditTests(LmkpTestCase):

    def test_first_pending_activity_add_new_taggroup(self):
        self.login()
        uid = self.create('a', get_new_diff('a'), return_uid=True)
        self.create('a', get_edit_diff('a', uid, version=1, diff_type=1))
        res = self.read_one('a', uid, 'json')
        self.assertEqual(res['total'], 2)
        self.assertEqual(STATUS_PENDING, get_status_from_item_json(res, 0))
        self.assertEqual(STATUS_EDITED, get_status_from_item_json(res, 1))
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

    def test_first_pending_activity_remove_taggroup(self):
        self.login()
        uid = self.create('a', get_new_diff('a'), return_uid=True)
        self.create('a', get_edit_diff('a', uid, version=1, diff_type=3))
        res = self.read_one('a', uid, 'json')
        self.assertEqual(res['total'], 2)
        self.assertEqual(STATUS_PENDING, get_status_from_item_json(res, 0))
        self.assertEqual(STATUS_EDITED, get_status_from_item_json(res, 1))
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

    def test_first_pending_activity_edit_tag_of_taggroup(self):
        self.login()
        uid = self.create('a', get_new_diff('a'), return_uid=True)
        self.create('a', get_edit_diff('a', uid, version=1, diff_type=4))
        res = self.read_one('a', uid, 'json')
        self.assertEqual(res['total'], 2)
        self.assertEqual(STATUS_PENDING, get_status_from_item_json(res, 0))
        self.assertEqual(STATUS_EDITED, get_status_from_item_json(res, 1))
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

    @pytest.mark.test
    def test_first_pending_activity_edit_inside_taggroup(self):
        self.login()
        uid = self.create('a', get_new_diff('a'), return_uid=True)
        self.create('a', get_edit_diff('a', uid, version=1, diff_type=5))
        res = self.read_one('a', uid, 'json')
        self.assertEqual(res['total'], 2)
        self.assertEqual(STATUS_PENDING, get_status_from_item_json(res, 0))
        self.assertEqual(STATUS_EDITED, get_status_from_item_json(res, 1))
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

    def test_add_pending_stakeholder_to_pending_activity(self):
        """

        """
        self.login()
        # Create a first Stakeholder
        sh_uid = self.create('sh', get_new_diff('sh'), return_uid=True)
        # Create a first Activity
        a_uid = self.create('a', get_new_diff('a', 1), return_uid=True)
        # Edit the Activity and add the Stakeholder as involvement
        inv_data1 = [{
            'id': sh_uid,
            'version': 1,
            'role': 6
        }]
        self.create(
            'a', get_edit_diff('a', a_uid, version=1, diff_type=2,
            data=inv_data1))

        # Check that everything was added correctly
        res = self.read_one('a', a_uid, 'json')
        self.assertEqual(res['total'], 2)
        self.assertEqual(STATUS_PENDING, get_status_from_item_json(res, 0))
        self.assertEqual(STATUS_EDITED, get_status_from_item_json(res, 1))
        self.assertEqual(len(get_involvements_from_item_json(res, 0)), 1)
        self.assertEqual(len(get_involvements_from_item_json(res, 1)), 0)
        res = self.read_one('sh', sh_uid, 'json')
        self.assertEqual(res['total'], 2)
        self.assertEqual(STATUS_PENDING, get_status_from_item_json(res, 0))
        self.assertEqual(STATUS_PENDING, get_status_from_item_json(res, 1))
        self.assertEqual(len(get_involvements_from_item_json(res, 0)), 1)
        self.assertEqual(len(get_involvements_from_item_json(res, 1)), 0)

    def test_add_pending_stakeholder_to_multiple_pending_activities(self):
        """

        """
        self.login()
        # Create a first Stakeholder
        sh_uid = self.create('sh', get_new_diff('sh'), return_uid=True)
        # Create a first Activity
        a_uid1 = self.create('a', get_new_diff('a', 1), return_uid=True)
        # Edit the Activity and add the Stakeholder as involvement
        inv_data1 = [{
            'id': sh_uid,
            'version': 1,
            'role': 6
        }]
        self.create(
            'a',
            get_edit_diff('a', a_uid1, version=1, diff_type=2, data=inv_data1))
        # Create a second Activity
        a_uid2 = self.create('a', get_new_diff('a', 1), return_uid=True)
        # Edit the Activity and add the Stakeholder as involvement
        inv_data2 = [{
            'id': sh_uid,
            'version': 2,
            'role': 6
        }]
        self.create(
            'a',
            get_edit_diff('a', a_uid2, version=1, diff_type=2, data=inv_data2))

        # Check that everything was added correctly
        res = self.read_one('a', a_uid1, 'json')
        self.assertEqual(res['total'], 2)
        self.assertEqual(STATUS_PENDING, get_status_from_item_json(res, 0))
        self.assertEqual(STATUS_EDITED, get_status_from_item_json(res, 1))
        self.assertEqual(len(get_involvements_from_item_json(res, 0)), 1)
        self.assertEqual(len(get_involvements_from_item_json(res, 1)), 0)
        res = self.read_one('a', a_uid2, 'json')
        self.assertEqual(res['total'], 2)
        self.assertEqual(STATUS_PENDING, get_status_from_item_json(res, 0))
        self.assertEqual(STATUS_EDITED, get_status_from_item_json(res, 1))
        self.assertEqual(len(get_involvements_from_item_json(res, 0)), 1)
        self.assertEqual(len(get_involvements_from_item_json(res, 1)), 0)
        res = self.read_one('sh', sh_uid, 'json')
        self.assertEqual(res['total'], 3)
        self.assertEqual(STATUS_PENDING, get_status_from_item_json(res, 0))
        self.assertEqual(STATUS_EDITED, get_status_from_item_json(res, 1))
        self.assertEqual(STATUS_PENDING, get_status_from_item_json(res, 2))
        self.assertEqual(len(get_involvements_from_item_json(res, 0)), 2)
        self.assertEqual(len(get_involvements_from_item_json(res, 1)), 1)
        self.assertEqual(len(get_involvements_from_item_json(res, 2)), 0)

    def test_add_pending_stakeholder_to_multiple_activities(self):
        """

        """
        self.login()
        # Create a first Stakeholder
        sh_uid = self.create('sh', get_new_diff('sh'), return_uid=True)
        # Create a first Activity
        a_uid1 = self.create('a', get_new_diff('a', 1), return_uid=True)
        # Edit the Activity and add the Stakeholder as involvement
        inv_data1 = [{
            'id': sh_uid,
            'version': 1,
            'role': 6
        }]
        self.create(
            'a',
            get_edit_diff('a', a_uid1, version=1, diff_type=2, data=inv_data1))
        # Create a second Activity, directly with SH 1
        inv_data2 = [{
            'id': sh_uid,
            'version': 2,
            'role': 6
        }]
        a_uid2 = self.create(
            'a', get_new_diff('a', 3, data=inv_data2), return_uid=True)

        # Check that everything was added correctly
        res = self.read_one('a', a_uid1, 'json')
        self.assertEqual(res['total'], 2)
        self.assertEqual(STATUS_PENDING, get_status_from_item_json(res, 0))
        self.assertEqual(STATUS_EDITED, get_status_from_item_json(res, 1))
        self.assertEqual(len(get_involvements_from_item_json(res, 0)), 1)
        self.assertEqual(len(get_involvements_from_item_json(res, 1)), 0)
        res = self.read_one('a', a_uid2, 'json')
        self.assertEqual(res['total'], 1)
        self.assertEqual(STATUS_PENDING, get_status_from_item_json(res, 0))
        self.assertEqual(len(get_involvements_from_item_json(res, 0)), 1)
        res = self.read_one('sh', sh_uid, 'json')
        self.assertEqual(res['total'], 3)
        self.assertEqual(STATUS_PENDING, get_status_from_item_json(res, 0))
        self.assertEqual(STATUS_EDITED, get_status_from_item_json(res, 1))
        self.assertEqual(STATUS_PENDING, get_status_from_item_json(res, 2))
        self.assertEqual(len(get_involvements_from_item_json(res, 0)), 2)
        self.assertEqual(len(get_involvements_from_item_json(res, 1)), 1)
        self.assertEqual(len(get_involvements_from_item_json(res, 2)), 0)

    def test_json_service_shows_new_versions_on_top(self):
        self.login()
        uid = self.create('a', get_new_diff('a'), return_uid=True)
        # self.review('a', uid)
        self.create('a', get_edit_diff('a', uid, version=1, diff_type=1))

        res = self.read_one('a', uid, 'json')
        self.assertEqual(res['total'], 2)
        self.assertEqual(STATUS_PENDING, get_status_from_item_json(res, 0))
        self.assertEqual(STATUS_EDITED, get_status_from_item_json(res, 1))
        self.assertEqual(res['data'][0]['version'], 2)
        self.assertEqual(res['data'][1]['version'], 1)
