#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pytest

from ..base import (
    find_key_value_in_taggroups_json,
    get_involvements_from_item_json,
    get_status_from_item_json,
    get_taggroup_by_main_tag,
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
    STATUS_PENDING,
)


@pytest.mark.usefixtures('app')
@pytest.mark.integration
@pytest.mark.stakeholders
class StakeholderEditActiveTests(LmkpTestCase):

    def setUp(self):
        self.login()

    def test_active_stakeholder_add_new_taggroup(self):
        uid = self.create('sh', get_new_diff(201), return_uid=True)
        self.review('sh', uid)
        self.create('sh', get_edit_diff(201, uid, version=1))
        res = self.read_one('sh', uid, 'json')
        self.assertEqual(res['total'], 2)
        self.assertEqual(STATUS_PENDING, get_status_from_item_json(res, 0))
        self.assertEqual(STATUS_ACTIVE, get_status_from_item_json(res, 1))
        taggroups_v2 = res['data'][0]['taggroups']
        taggroups_v1 = res['data'][1]['taggroups']
        self.assertEqual(len(taggroups_v1), 2)
        self.assertEqual(len(taggroups_v2), 3)
        self.assertFalse(find_key_value_in_taggroups_json(
            taggroups_v1, '[SH] Checkbox 1', value='[SH] Value D1',
            main_tag=True))
        self.assertTrue(find_key_value_in_taggroups_json(
            taggroups_v2, '[SH] Checkbox 1', value='[SH] Value D1',
            main_tag=True))

    def test_active_stakeholder_remove_taggroup(self):
        uid = self.create('sh', get_new_diff(201), return_uid=True)
        self.review('sh', uid)
        self.create('sh', get_edit_diff(202, uid, version=1))
        res = self.read_one('sh', uid, 'json')
        self.assertEqual(res['total'], 2)
        self.assertEqual(STATUS_PENDING, get_status_from_item_json(res, 0))
        self.assertEqual(STATUS_ACTIVE, get_status_from_item_json(res, 1))
        taggroups_v2 = res['data'][0]['taggroups']
        taggroups_v1 = res['data'][1]['taggroups']
        self.assertEqual(len(taggroups_v1), 2)
        self.assertEqual(len(taggroups_v2), 1)
        self.assertTrue(find_key_value_in_taggroups_json(
            taggroups_v1, '[SH] Textfield 1', value='asdf',
            main_tag=True))
        self.assertFalse(find_key_value_in_taggroups_json(
            taggroups_v2, '[SH] Textfield 1'))

    def test_active_stakeholder_edit_maintag_of_taggroup(self):
        uid = self.create('sh', get_new_diff(204), return_uid=True)
        self.review('sh', uid)
        self.create('sh', get_edit_diff(203, uid, version=1))
        res = self.read_one('sh', uid, 'json')
        self.assertEqual(res['total'], 2)
        self.assertEqual(STATUS_PENDING, get_status_from_item_json(res, 0))
        self.assertEqual(STATUS_ACTIVE, get_status_from_item_json(res, 1))
        taggroups_v2 = res['data'][0]['taggroups']
        taggroups_v1 = res['data'][1]['taggroups']
        self.assertEqual(len(taggroups_v1), 2)
        self.assertEqual(len(taggroups_v2), 2)
        textfield_v1 = find_key_value_in_taggroups_json(
            taggroups_v1, '[SH] Textfield 1', return_value=True)
        self.assertIn('Foo', textfield_v1)
        self.assertNotIn('Bar', textfield_v1)
        self.assertTrue(find_key_value_in_taggroups_json(
            taggroups_v1, '[SH] Textfield 1',
            value=u'Foo ‰öäüñ Æò" dróżką ສອບ', main_tag=True))
        textfield_v2 = find_key_value_in_taggroups_json(
            taggroups_v2, '[SH] Textfield 1', return_value=True)
        self.assertIn('Bar', textfield_v2)
        self.assertNotIn('Foo', textfield_v2)
        self.assertTrue(find_key_value_in_taggroups_json(
            taggroups_v2, '[SH] Textfield 1', value=u'Bar %&ä£',
            main_tag=True))

    def test_active_stakeholder_edit_tag_of_taggroup(self):
        uid = self.create('sh', get_new_diff(204), return_uid=True)
        self.review('sh', uid)
        self.create('sh', get_edit_diff(204, uid, version=1))
        res = self.read_one('sh', uid, 'json')
        self.assertEqual(res['total'], 2)
        self.assertEqual(STATUS_PENDING, get_status_from_item_json(res, 0))
        self.assertEqual(STATUS_ACTIVE, get_status_from_item_json(res, 1))
        taggroups_v2 = res['data'][0]['taggroups']
        taggroups_v1 = res['data'][1]['taggroups']
        self.assertEqual(len(taggroups_v1), 2)
        self.assertEqual(len(taggroups_v2), 2)
        self.assertTrue(find_key_value_in_taggroups_json(
            taggroups_v1, '[SH] Textarea 1', value='Foo text'))
        self.assertFalse(find_key_value_in_taggroups_json(
            taggroups_v1, '[SH] Textarea 1', value='Bar text'))
        self.assertFalse(find_key_value_in_taggroups_json(
            taggroups_v2, '[SH] Textarea 1', value='Foo text'))
        self.assertTrue(find_key_value_in_taggroups_json(
            taggroups_v2, '[SH] Textarea 1', value='Bar text'))

    def test_active_stakeholder_add_tag_to_taggroup(self):
        uid = self.create('sh', get_new_diff(201), return_uid=True)
        self.review('sh', uid)
        self.create('sh', get_edit_diff(205, uid, version=1))
        res = self.read_one('sh', uid, 'json')
        self.assertEqual(res['total'], 2)
        self.assertEqual(STATUS_PENDING, get_status_from_item_json(res, 0))
        self.assertEqual(STATUS_ACTIVE, get_status_from_item_json(res, 1))
        taggroups_v2 = res['data'][0]['taggroups']
        taggroups_v1 = res['data'][1]['taggroups']
        self.assertEqual(len(taggroups_v1), 2)
        self.assertEqual(len(taggroups_v2), 2)
        self.assertTrue(find_key_value_in_taggroups_json(
            taggroups_v1, '[SH] Textfield 1', value='asdf',
            main_tag=True))
        self.assertFalse(find_key_value_in_taggroups_json(
            taggroups_v1, '[SH] Textarea 1', value='Foo'))
        self.assertEqual(len(get_taggroup_by_main_tag(
            taggroups_v1, '[SH] Textfield 1', value='asdf')['tags']), 1)
        self.assertTrue(find_key_value_in_taggroups_json(
            taggroups_v2, '[SH] Textfield 1', value='asdf',
            main_tag=True))
        self.assertTrue(find_key_value_in_taggroups_json(
            taggroups_v2, '[SH] Textarea 1', value='Foo'))
        self.assertEqual(len(get_taggroup_by_main_tag(
            taggroups_v2, '[SH] Textfield 1', value='asdf')['tags']), 2)

    def test_active_stakeholder_remove_tag_of_taggroup(self):
        uid = self.create('sh', get_new_diff(204), return_uid=True)
        self.review('sh', uid)
        self.create('sh', get_edit_diff(206, uid, version=1))
        res = self.read_one('sh', uid, 'json')
        self.assertEqual(res['total'], 2)
        self.assertEqual(STATUS_PENDING, get_status_from_item_json(res, 0))
        self.assertEqual(STATUS_ACTIVE, get_status_from_item_json(res, 1))
        taggroups_v2 = res['data'][0]['taggroups']
        taggroups_v1 = res['data'][1]['taggroups']
        self.assertEqual(len(taggroups_v1), 2)
        self.assertEqual(len(taggroups_v2), 2)
        self.assertTrue(find_key_value_in_taggroups_json(
            taggroups_v1, '[SH] Textarea 1'))
        self.assertEqual(len(get_taggroup_by_main_tag(
            taggroups_v1, '[SH] Textfield 1')['tags']), 2)
        self.assertFalse(find_key_value_in_taggroups_json(
            taggroups_v2, '[SH] Textarea 1'))
        self.assertEqual(len(get_taggroup_by_main_tag(
            taggroups_v2, '[SH] Textfield 1')['tags']), 1)

    def test_combination_of_attribute_edits(self):
        uid = self.create('sh', get_new_diff(205), return_uid=True)
        self.review('sh', uid)
        self.create('sh', get_edit_diff(207, uid, version=1))
        res = self.read_one('sh', uid, 'json')
        self.assertEqual(res['total'], 2)
        self.assertEqual(STATUS_PENDING, get_status_from_item_json(res, 0))
        self.assertEqual(STATUS_ACTIVE, get_status_from_item_json(res, 1))
        taggroups_v2 = res['data'][0]['taggroups']
        taggroups_v1 = res['data'][1]['taggroups']
        self.assertEqual(len(taggroups_v1), 8)
        self.assertEqual(len(taggroups_v2), 9)
        self.assertTrue(find_key_value_in_taggroups_json(
            taggroups_v1, '[SH] Textarea 1'))
        self.assertFalse(find_key_value_in_taggroups_json(
            taggroups_v2, '[SH] Textarea 1'))
        self.assertTrue(find_key_value_in_taggroups_json(
            taggroups_v1, '[SH] Checkbox 1', value='[SH] Value D2'))
        self.assertFalse(find_key_value_in_taggroups_json(
            taggroups_v2, '[SH] Checkbox 1', value='[SH] Value D2'))
        self.assertFalse(find_key_value_in_taggroups_json(
            taggroups_v1, '[SH] Checkbox 1', value='[SH] Value D4'))
        self.assertTrue(find_key_value_in_taggroups_json(
            taggroups_v2, '[SH] Checkbox 1', value='[SH] Value D4'))
        self.assertFalse(find_key_value_in_taggroups_json(
            taggroups_v1, '[SH] Integerdropdown 1', value='1'))
        self.assertTrue(find_key_value_in_taggroups_json(
            taggroups_v2, '[SH] Integerdropdown 1', value='1'))

    def test_involvement_attribute_change_does_not_uouch_attributes(self):
        sh_uid = self.create('sh', get_new_diff(201), return_uid=True)
        inv_data = [{
            'id': sh_uid,
            'version': 1,
            'role': 1,
            'op': 'add'
        }]
        a_uid = self.create(
            'a', get_new_diff(103, data=inv_data), return_uid=True)
        # Edit the Activity
        self.create('a', get_edit_diff(101, a_uid, version=1))

        # On Stakeholder side, there are 2 versions:
        # [0] v2: with involvement to v2 of Activity, pending.
        # [1] v1: without involvements, pending.
        res = self.read_one('sh', sh_uid, 'json')
        self.assertEqual(res['total'], 2)
        self.assertEqual(STATUS_PENDING, get_status_from_item_json(res, 0))
        self.assertEqual(STATUS_PENDING, get_status_from_item_json(res, 1))
        inv = get_involvements_from_item_json(res, 0)
        self.assertEqual(len(inv), 1)
        self.assertEqual(get_version_from_involvement_json(inv), 2)
        self.assertEqual(len(get_involvements_from_item_json(res, 1)), 0)

        # On Activity side, there are 2 versions:
        # [0] v2: with involvement to v2 of Stakeholder, pending.
        # [1] v1: with involvement to v2 of Stakeholder, edited.
        res = self.read_one('a', a_uid, 'json')
        self.assertEqual(res['total'], 2)
        self.assertEqual(STATUS_PENDING, get_status_from_item_json(res, 0))
        self.assertEqual(STATUS_EDITED, get_status_from_item_json(res, 1))
        inv_v2 = get_involvements_from_item_json(res, 0)
        self.assertEqual(len(inv_v2), 1)
        self.assertEqual(get_version_from_involvement_json(inv_v2), 2)
        inv_v1 = get_involvements_from_item_json(res, 1)
        self.assertEqual(len(inv_v1), 1)
        self.assertEqual(get_version_from_involvement_json(inv_v1), 2)
