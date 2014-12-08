#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pytest
import uuid
from pyramid import testing
from ...base import get_settings

from ..base import (
    LmkpTestCase,
    get_base_url_by_item_type,
    find_key_value_in_taggroups_json,
)
from ..diffs import (
    get_new_diff,
    get_edit_diff,
)
from ...base import (
    TEXT_INACTIVE_VERSION,
    TITLE_HISTORY_VIEW,
)


@pytest.mark.read
@pytest.mark.usefixtures('app')
@pytest.mark.integration
@pytest.mark.activities
class ActivityReadOneJSONTests(LmkpTestCase):

    def setUp(self):
        self.request = testing.DummyRequest()
        settings = get_settings()
        self.config = testing.setUp(request=self.request, settings=settings)
        self.login()

    def tearDown(self):
        testing.tearDown()

    def test_read_one_json_returns_empty_if_not_found(self):
        json = self.read_one('a', uuid.uuid4(), 'json')
        self.assertEqual(json, {})

    def test_activity_appears_in_read_one_json(self):
        uid = self.create('a', get_new_diff(101), return_uid=True)

        json = self.read_one('a', uid, 'json')
        self.assertEqual(json.get('status'), 'pending')
        self.assertEqual(json.get('status_id'), 1)
        self.assertIsNone(json['previous_version'])
        self.assertEqual(json.get('geometry').get('type'), 'Point')
        self.assertEqual(len(json.get('geometry').get('coordinates')), 2)
        self.assertEqual(json.get('version'), 1)
        self.assertIn('timestamp', json)
        self.assertIn('id', json)
        self.assertEqual(len(json.get('taggroups')), 2)
        tg1 = json.get('taggroups')[0]
        self.assertEqual(tg1.get('tg_id'), 1)
        self.assertEqual(tg1.get('main_tag').get('key'), '[A] Dropdown 1')
        self.assertEqual(tg1.get('main_tag').get('value'), '[A] Value A1')
        self.assertEqual(len(tg1.get('tags')), 1)
        t1 = tg1.get('tags')[0]
        self.assertEqual(t1.get('key'), '[A] Dropdown 1')
        self.assertEqual(t1.get('value'), '[A] Value A1')
        tg2 = json.get('taggroups')[1]
        self.assertEqual(tg2.get('tg_id'), 2)
        self.assertEqual(tg2.get('main_tag').get('key'), '[A] Numberfield 1')
        self.assertEqual(tg2.get('main_tag').get('value'), '123.45')
        self.assertEqual(len(tg2.get('tags')), 1)
        t2 = tg2.get('tags')[0]
        self.assertEqual(t2.get('key'), '[A] Numberfield 1')
        self.assertEqual(t2.get('value'), '123.45')

    def test_activity_read_one_json_public_does_not_see_pending(self):

        json = self.read_one('a', uuid.uuid4(), 'json')
        self.assertEqual(json, {})

        uid = self.create('a', get_new_diff(101), return_uid=True)
        self.logout()

        json = self.read_one('a', uid, 'json')
        self.assertEqual(json, {})

    def test_activity_read_one_json_by_version_logged_in(self):
        uid = self.create('a', get_new_diff(101), return_uid=True)
        self.create('a', get_edit_diff(101, uid))
        self.create('a', get_edit_diff(101, uid, version=2))

        json = self.read_one('a', uid, 'json')
        self.assertEqual(json.get('version'), 3)

        json = self.read_one('a', uid, 'json', params={'v': 2})
        self.assertEqual(json.get('version'), 2)

        self.logout()
        json = self.read_one('a', uid, 'json', params={'v': 2})
        self.assertEqual(json, {})

    def test_activity_read_one_json_by_version_moderator(self):
        # Create A as user1
        self.logout()
        self.login(username='user1', password='asdfasdf')
        uid = self.create('a', get_new_diff(101), return_uid=True)
        self.create('a', get_edit_diff(101, uid))
        self.create('a', get_edit_diff(101, uid, version=2))

        # Admin is moderator, can see pending
        self.logout()
        self.login()
        json = self.read_one('a', uid, 'json')
        self.assertEqual(json.get('version'), 3)
        json = self.read_one('a', uid, 'json', params={'v': 2})
        self.assertEqual(json.get('version'), 2)

        # User 2 is moderator of cambodia, cannot see pending in laos
        self.logout()
        self.login(username='user2', password='asdfasdf')
        profile_params = {'_PROFILE_': 'laos'}
        json = self.read_one('a', uid, 'json', params=profile_params)
        self.assertEqual(json, {})
        json = self.read_one('a', uid, 'json', params={'v': 2})
        self.assertEqual(json, {})


@pytest.mark.read
@pytest.mark.usefixtures('app')
@pytest.mark.integration
@pytest.mark.activities
class ActivityReadOneHTMLTests(LmkpTestCase):

    def setUp(self):
        self.request = testing.DummyRequest()
        settings = get_settings()
        self.config = testing.setUp(request=self.request, settings=settings)
        self.login()

    def tearDown(self):
        testing.tearDown()

    def test_read_one_html_returns_404_if_not_found(self):
        url = get_base_url_by_item_type('a')
        html = self.app.get('%s/html/%s' % (url, uuid.uuid4()), status=404)
        self.assertEqual(html.status_int, 404)

    def test_read_one_html_finds_activity(self):

        uid = self.create('a', get_new_diff(101), return_uid=True)
        html = self.read_one('a', uid, 'html')

        self.assertIn(uid, html)

    def test_read_one_html_finds_activity_by_version(self):
        uid = self.create('a', get_new_diff(101), return_uid=True)
        self.create('a', get_edit_diff(101, uid))
        self.create('a', get_edit_diff(101, uid, version=2))

        html_v2 = self.read_one('a', uid, 'html', params={'v': 2})
        self.assertIn(uid, html_v2)
        self.assertIn(TEXT_INACTIVE_VERSION, html_v2)


@pytest.mark.read
@pytest.mark.usefixtures('app')
@pytest.mark.integration
@pytest.mark.activities
class ActivityReadManyTests(LmkpTestCase):

    def setUp(self):
        self.request = testing.DummyRequest()
        settings = get_settings()
        self.config = testing.setUp(request=self.request, settings=settings)
        self.login()

    def tearDown(self):
        testing.tearDown()

    def test_activities_appear_in_read_many_json(self):
        json = self.read_many('a', 'json')
        self.assertEqual(json['data'], [])
        self.assertEqual(json['total'], 0)

        self.create('a', get_new_diff(101))

        json = self.read_many('a', 'json')
        self.assertEqual(json['total'], 1)
        a1 = json['data'][0]
        self.assertEqual(a1.get('status'), 'pending')
        self.assertEqual(a1.get('status_id'), 1)
        self.assertIsNone(a1['previous_version'])
        self.assertEqual(a1.get('geometry').get('type'), 'Point')
        self.assertEqual(len(a1.get('geometry').get('coordinates')), 2)
        self.assertEqual(a1.get('version'), 1)
        self.assertIn('timestamp', a1)
        self.assertIn('id', a1)
        self.assertEqual(len(a1.get('taggroups')), 2)
        tg1 = a1.get('taggroups')[0]
        self.assertEqual(tg1.get('tg_id'), 1)
        self.assertEqual(tg1.get('main_tag').get('key'), '[A] Dropdown 1')
        self.assertEqual(tg1.get('main_tag').get('value'), '[A] Value A1')
        self.assertEqual(len(tg1.get('tags')), 1)
        t1 = tg1.get('tags')[0]
        self.assertEqual(t1.get('key'), '[A] Dropdown 1')
        self.assertEqual(t1.get('value'), '[A] Value A1')
        tg2 = a1.get('taggroups')[1]
        self.assertEqual(tg2.get('tg_id'), 2)
        self.assertEqual(tg2.get('main_tag').get('key'), '[A] Numberfield 1')
        self.assertEqual(tg2.get('main_tag').get('value'), '123.45')
        self.assertEqual(len(tg2.get('tags')), 1)
        t2 = tg2.get('tags')[0]
        self.assertEqual(t2.get('key'), '[A] Numberfield 1')
        self.assertEqual(t2.get('value'), '123.45')

    def test_only_active_activities_appear_in_many_json_public(self):
        uid_1 = self.create('a', get_new_diff(101), return_uid=True)
        self.review('a', uid_1)
        self.create('a', get_new_diff(101))

        url = get_base_url_by_item_type('a')
        json = self.app.get('%s/public/json' % url).json

        self.assertEqual(json['total'], 1)
        self.assertEqual(json['data'][0]['id'], uid_1)

    def test_activities_appear_in_read_many_html(self):
        uid = self.create('a', get_new_diff(101), return_uid=True)
        url = get_base_url_by_item_type('a')
        res = self.app.get('%s/html' % url)

        self.assertIn(uid, res)

    def test_activities_appear_in_read_many_html_public(self):
        uid_1 = self.create('a', get_new_diff(101), return_uid=True)
        self.review('a', uid_1)
        uid_2 = self.create('a', get_new_diff(101), return_uid=True)

        url = get_base_url_by_item_type('a')
        res = self.app.get('%s/public/html' % url)

        self.assertIn(uid_1, res)
        self.assertNotIn(uid_2, res)

    def test_activities_pending_not_visible_if_not_logged_in(self):
        self.create('a', get_new_diff(101))
        self.logout()
        json = self.read_many('a', 'json')
        self.assertEqual(json['data'], [])
        self.assertEqual(json['total'], 0)

    def test_activities_like_filter(self):
        self.login()
        uid_1 = self.create('a', get_new_diff(101), return_uid=True)
        uid_2 = self.create('a', get_new_diff(104), return_uid=True)
        uid_3 = self.create('a', get_new_diff(105), return_uid=True)

        json = self.read_many('a', 'json')
        self.assertEqual(json['total'], 3)

        filter_1 = {
            'a__[A] Dropdown 1__like': '[A] Value A1'
        }
        json = self.read_many('a', 'json', params=filter_1)
        self.assertEqual(json['total'], 2)
        uids = [j['id'] for j in json.get('data', [])]
        self.assertIn(uid_1, uids)
        self.assertNotIn(uid_2, uids)
        self.assertIn(uid_3, uids)

        filter_2 = {
            'a__[A] Dropdown 1__like': '[A] Value A2'
        }
        json = self.read_many('a', 'json', params=filter_2)
        self.assertEqual(json['total'], 1)
        uids = [j['id'] for j in json.get('data', [])]
        self.assertNotIn(uid_1, uids)
        self.assertIn(uid_2, uids)
        self.assertNotIn(uid_3, uids)

        filter_3 = {
            'a__[A] Dropdown 1__like': '[a] value a2'
        }
        json = self.read_many('a', 'json', params=filter_3)
        self.assertEqual(json['total'], 0)
        uids = [j['id'] for j in json.get('data', [])]
        self.assertNotIn(uid_1, uids)
        self.assertNotIn(uid_2, uids)
        self.assertNotIn(uid_3, uids)

    def test_activities_ilike_filter(self):
        self.login()
        uid_1 = self.create('a', get_new_diff(101), return_uid=True)
        uid_2 = self.create('a', get_new_diff(104), return_uid=True)
        uid_3 = self.create('a', get_new_diff(105), return_uid=True)

        json = self.read_many('a', 'json')
        self.assertEqual(json['total'], 3)

        filter_1 = {
            'a__[A] Dropdown 1__ilike': '[A] Value A1'
        }
        json = self.read_many('a', 'json', params=filter_1)
        self.assertEqual(json['total'], 2)
        uids = [j['id'] for j in json.get('data', [])]
        self.assertIn(uid_1, uids)
        self.assertNotIn(uid_2, uids)
        self.assertIn(uid_3, uids)

        filter_2 = {
            'a__[A] Dropdown 1__ilike': '[A] Value A2'
        }
        json = self.read_many('a', 'json', params=filter_2)
        self.assertEqual(json['total'], 1)
        uids = [j['id'] for j in json.get('data', [])]
        self.assertNotIn(uid_1, uids)
        self.assertIn(uid_2, uids)
        self.assertNotIn(uid_3, uids)

        filter_3 = {
            'a__[A] Dropdown 1__ilike': '[a] value a2'
        }
        json = self.read_many('a', 'json', params=filter_3)
        self.assertEqual(json['total'], 1)
        uids = [j['id'] for j in json.get('data', [])]
        self.assertNotIn(uid_1, uids)
        self.assertIn(uid_2, uids)
        self.assertNotIn(uid_3, uids)

    def test_activities_special_chars_in_filter(self):
        filter = {
            'a__[A] Dropdown 1__ilike': 'üäö'
        }
        json = self.read_many('a', 'json', params=filter)
        self.assertEqual(json['total'], 0)
        html = self.read_many('a', 'html', params=filter)
        self.assertEqual(html.status_int, 200)

        filter = {
            'a__éèà__ilike': 'foo'
        }
        json = self.read_many('a', 'json', params=filter)
        self.assertEqual(json['total'], 0)
        html = self.read_many('a', 'html', params=filter)
        self.assertEqual(html.status_int, 200)

        filter = {
            'a__[A] Textarea 3__ilike': 'üäö'
        }
        json = self.read_many('a', 'json', params=filter)
        self.assertEqual(json['total'], 0)
        html = self.read_many('a', 'html', params=filter)
        self.assertEqual(html.status_int, 200)

        filter.update({'_LOCALE_': 'es'})
        json = self.read_many('a', 'json', params=filter)
        self.assertEqual(json['total'], 0)
        html = self.read_many('a', 'html', params=filter)
        self.assertEqual(html.status_int, 200)

    def test_activities_filter_not_like(self):
        uid_1 = self.create('a', get_new_diff(101), return_uid=True)  # A1
        self.create('a', get_new_diff(104), return_uid=True)  # A2
        uid_3 = self.create('a', get_new_diff(110), return_uid=True)  # A3

        filter_params = {'a__[A] Dropdown 1__nlike': '[A] Value A2'}
        res = self.read_many('a', 'json', params=filter_params)
        self.assertEqual(len(res.get('data')), 2)
        res_1 = res.get('data')[0]
        self.assertEqual(res_1.get('id'), uid_3)
        res_2 = res.get('data')[1]
        self.assertEqual(res_2.get('id'), uid_1)

    def test_activities_filter_eq(self):
        self.create('a', get_new_diff(101), return_uid=True)  # 123.45
        uid_2 = self.create('a', get_new_diff(110), return_uid=True)  # 99
        self.create('a', get_new_diff(111), return_uid=True)  # 1000

        filter_params = {'a__[A] Numberfield 1__eq': '99'}
        res = self.read_many('a', 'json', params=filter_params)
        self.assertEqual(len(res.get('data')), 1)
        res_1 = res.get('data')[0]
        self.assertEqual(res_1.get('id'), uid_2)

        filter_params = {'a__[A] Numberfield 1__eq': '99.0'}
        res = self.read_many('a', 'json', params=filter_params)
        self.assertEqual(len(res.get('data')), 1)
        res_1 = res.get('data')[0]
        self.assertEqual(res_1.get('id'), uid_2)

    def test_activities_filter_ne(self):
        uid_1 = self.create('a', get_new_diff(101), return_uid=True)  # 123.45
        self.create('a', get_new_diff(110), return_uid=True)  # 99
        uid_3 = self.create('a', get_new_diff(111), return_uid=True)  # 1000

        filter_params = {'a__[A] Numberfield 1__ne': '99'}
        res = self.read_many('a', 'json', params=filter_params)
        self.assertEqual(len(res.get('data')), 2)
        res_1 = res.get('data')[0]
        self.assertEqual(res_1.get('id'), uid_3)
        res_3 = res.get('data')[1]
        self.assertEqual(res_3.get('id'), uid_1)

        filter_params = {'a__[A] Numberfield 1__ne': '99.0'}
        res = self.read_many('a', 'json', params=filter_params)
        self.assertEqual(len(res.get('data')), 2)
        res_1 = res.get('data')[0]
        self.assertEqual(res_1.get('id'), uid_3)
        res_3 = res.get('data')[1]
        self.assertEqual(res_3.get('id'), uid_1)

    def test_activities_filter_lt_lte(self):
        uid_1 = self.create('a', get_new_diff(101), return_uid=True)  # 123.45
        uid_2 = self.create('a', get_new_diff(110), return_uid=True)  # 99
        self.create('a', get_new_diff(111), return_uid=True)  # 1000

        filter_params = {'a__[A] Numberfield 1__lt': '123.45'}
        res = self.read_many('a', 'json', params=filter_params)
        self.assertEqual(len(res.get('data')), 1)
        res_1 = res.get('data')[0]
        self.assertEqual(res_1.get('id'), uid_2)

        filter_params = {'a__[A] Numberfield 1__lte': '123.45'}
        res = self.read_many('a', 'json', params=filter_params)
        self.assertEqual(len(res.get('data')), 2)
        res_1 = res.get('data')[0]
        self.assertEqual(res_1.get('id'), uid_2)
        res_3 = res.get('data')[1]
        self.assertEqual(res_3.get('id'), uid_1)

    def test_activities_filter_gt_gte(self):
        uid_1 = self.create('a', get_new_diff(101), return_uid=True)  # 123.45
        self.create('a', get_new_diff(110), return_uid=True)  # 99
        uid_3 = self.create('a', get_new_diff(111), return_uid=True)  # 1000

        filter_params = {'a__[A] Numberfield 1__gt': '123.45'}
        res = self.read_many('a', 'json', params=filter_params)
        self.assertEqual(len(res.get('data')), 1)
        res_1 = res.get('data')[0]
        self.assertEqual(res_1.get('id'), uid_3)

        filter_params = {'a__[A] Numberfield 1__gte': '123.45'}
        res = self.read_many('a', 'json', params=filter_params)
        self.assertEqual(len(res.get('data')), 2)
        res_1 = res.get('data')[0]
        self.assertEqual(res_1.get('id'), uid_3)
        res_3 = res.get('data')[1]
        self.assertEqual(res_3.get('id'), uid_1)

    def test_activities_with_stakeholder_filter(self):
        sh_uid_1 = self.create('sh', get_new_diff(201), return_uid=True)
        sh_uid_2 = self.create('sh', get_new_diff(204), return_uid=True)
        inv_data_1 = [{
            'id': sh_uid_1,
            'version': 1,
            'role': 6
        }]
        a_uid_1 = self.create(
            'a', get_new_diff(103, data=inv_data_1), return_uid=True)
        inv_data_2 = [{
            'id': sh_uid_2,
            'version': 1,
            'role': 6
        }]
        self.create(
            'a', get_new_diff(103, data=inv_data_2), return_uid=True)

        filter_params = {'sh__[SH] Textfield 1__like': 'asdf'}
        res = self.read_many('a', 'json', params=filter_params)
        self.assertEqual(len(res.get('data')), 1)
        res_1 = res.get('data')[0]
        self.assertEqual(res_1.get('id'), a_uid_1)
        inv_1 = res_1.get('involvements')
        self.assertEqual(len(inv_1), 1)
        self.assertEqual(inv_1[0].get('id'), sh_uid_1)

    def test_activities_filter_logical_operator(self):
        uid_1 = self.create('a', get_new_diff(101), return_uid=True)  # A1
        uid_2 = self.create('a', get_new_diff(104), return_uid=True)  # A2
        self.create('a', get_new_diff(110), return_uid=True)  # A3

        filter_params = {
            'a__[A] Dropdown 1__like': '[A] Value A1',
            'a__[A] Numberfield 1__eq': '123.45'
        }
        res = self.read_many('a', 'json', params=filter_params)
        self.assertEqual(len(res.get('data')), 1)
        res_1 = res.get('data')[0]
        self.assertEqual(res_1.get('id'), uid_1)
        filter_params['logical_op'] = 'or'
        res = self.read_many('a', 'json', params=filter_params)
        self.assertEqual(len(res.get('data')), 2)
        res_1 = res.get('data')[0]
        self.assertEqual(res_1.get('id'), uid_2)
        res_2 = res.get('data')[1]
        self.assertEqual(res_2.get('id'), uid_1)

    # def test_activities_filter_logical_operator_same_attribute(self):
    #     uid_1 = self.create('a', get_new_diff(101), return_uid=True)  # A1
    #     uid_2 = self.create('a', get_new_diff(104), return_uid=True)  # A2
    #     self.create('a', get_new_diff(110), return_uid=True)  # A3

    #     filter_params = {
    #         'a__[A] Dropdown 1__like': '[A] Value A1',
    #         'a__[A] Dropdown 1__like': '[A] Value A2'
    #     }
    #     res = self.read_many('a', 'json', params=filter_params)

    #     # res_1 = res.get('data')[0]
    #     # self.assertEqual(res_1.get('id'), uid_2)

    #     self.assertEqual(len(res.get('data')), 0)

    #     filter_params['logical_op'] = 'or'
    #     res = self.read_many('a', 'json', params=filter_params)
    #     self.assertEqual(len(res.get('data')), 2)
    #     res_1 = res.get('data')[0]
    #     self.assertEqual(res_1.get('id'), uid_1)
    #     res_2 = res.get('data')[1]
    #     self.assertEqual(res_2.get('id'), uid_2)

    def test_activities_filter_logical_operator_stakeholder(self):
        sh_uid_1 = self.create('sh', get_new_diff(201), return_uid=True)
        sh_uid_2 = self.create('sh', get_new_diff(204), return_uid=True)
        inv_data_1 = [{
            'id': sh_uid_1,
            'version': 1,
            'role': 6
        }]
        a_uid_1 = self.create(
            'a', get_new_diff(103, data=inv_data_1), return_uid=True)
        inv_data_2 = [{
            'id': sh_uid_2,
            'version': 1,
            'role': 6
        }]
        self.create(
            'a', get_new_diff(103, data=inv_data_2), return_uid=True)

        filter_params = {
            'sh__[SH] Textfield 1__like': 'asdf',
            'a__[A] Dropdown 1__like': '[A] Value A2'
        }
        res = self.read_many('a', 'json', params=filter_params)
        self.assertEqual(len(res.get('data')), 0)
        filter_params['logical_op'] = 'or'
        res = self.read_many('a', 'json', params=filter_params)
        self.assertEqual(len(res.get('data')), 1)
        res_1 = res.get('data')[0]
        self.assertEqual(res_1.get('id'), a_uid_1)
        inv_1 = res_1.get('involvements')
        self.assertEqual(len(inv_1), 1)
        self.assertEqual(inv_1[0].get('id'), sh_uid_1)

    def test_activities_order_default_by_timestamp(self):
        uid_1 = self.create('a', get_new_diff(101), return_uid=True)
        uid_2 = self.create('a', get_new_diff(110), return_uid=True)
        uid_3 = self.create('a', get_new_diff(111), return_uid=True)

        res = self.read_many('a', 'json')
        self.assertEqual(len(res.get('data')), 3)
        res_1 = res.get('data')[0]
        res_2 = res.get('data')[1]
        res_3 = res.get('data')[2]

        self.assertEqual(res_1.get('id'), uid_3)
        self.assertEqual(res_2.get('id'), uid_2)
        self.assertEqual(res_3.get('id'), uid_1)

    def test_activities_order_by_numbers(self):
        uid_1 = self.create('a', get_new_diff(101), return_uid=True)  # 123.4
        uid_2 = self.create('a', get_new_diff(110), return_uid=True)  # 99
        uid_3 = self.create('a', get_new_diff(111), return_uid=True)  # 1000

        order_params = {'order_by': '[A] Numberfield 1'}
        res = self.read_many('a', 'json', params=order_params)
        self.assertEqual(len(res.get('data')), 3)
        res_1 = res.get('data')[0]
        res_2 = res.get('data')[1]
        res_3 = res.get('data')[2]

        self.assertEqual(res_1.get('id'), uid_2)
        self.assertEqual(res_2.get('id'), uid_1)
        self.assertEqual(res_3.get('id'), uid_3)

    def test_activities_order_by_strings(self):
        uid_1 = self.create('a', get_new_diff(101), return_uid=True)  # A1
        uid_2 = self.create('a', get_new_diff(110), return_uid=True)  # A3
        uid_3 = self.create('a', get_new_diff(111), return_uid=True)  # A2

        order_params = {'order_by': '[A] Dropdown 1'}
        res = self.read_many('a', 'json', params=order_params)
        self.assertEqual(len(res.get('data')), 3)
        res_1 = res.get('data')[0]
        res_2 = res.get('data')[1]
        res_3 = res.get('data')[2]

        self.assertEqual(res_1.get('id'), uid_1)
        self.assertEqual(res_2.get('id'), uid_3)
        self.assertEqual(res_3.get('id'), uid_2)

    def test_activities_translation(self):
        self.create('a', get_new_diff(101))
        res = self.read_many('a', 'json', params={'_LOCALE_': 'es'})
        self.assertEqual(len(res.get('data')), 1)
        res_1 = res.get('data')[0]
        self.assertFalse(find_key_value_in_taggroups_json(
            res_1.get('taggroups'), '[A] Dropdown 1', '[A] Value A1'))
        self.assertTrue(find_key_value_in_taggroups_json(
            res_1.get('taggroups'), '[A-T] Dropdown 1', '[A-T] Value A1'))

    def test_activities_status_active(self):
        uid_1 = self.create('a', get_new_diff(101), return_uid=True)
        self.review('a', uid_1)
        self.create('a', get_new_diff(101))

        status_params = {'status': 'active'}
        res = self.read_many('a', 'json', params=status_params)
        self.assertEqual(len(res.get('data')), 1)
        self.assertEqual(res.get('data')[0].get('id'), uid_1)

    def test_activities_status_inactive(self):
        uid_1 = self.create('a', get_new_diff(101), return_uid=True)
        self.review('a', uid_1)
        self.create('a', get_edit_diff(101, uid_1))
        self.review('a', uid_1, version=2)
        self.create('a', get_new_diff(101), return_uid=True)

        status_params = {'status': 'inactive'}
        res = self.read_many('a', 'json', params=status_params)
        self.assertEqual(len(res.get('data')), 1)
        res_1 = res.get('data')[0]
        self.assertEqual(res_1.get('id'), uid_1)
        self.assertEqual(res_1.get('version'), 1)

    def test_activities_status_pending(self):
        uid_1 = self.create('a', get_new_diff(101), return_uid=True)
        self.review('a', uid_1)
        uid_2 = self.create('a', get_new_diff(101), return_uid=True)

        status_params = {'status': 'pending'}
        res = self.read_many('a', 'json', params=status_params)
        self.assertEqual(len(res.get('data')), 1)
        res_1 = res.get('data')[0]
        self.assertEqual(res_1.get('id'), uid_2)
        self.assertEqual(res_1.get('version'), 1)

    def test_read_moderator_sees_pending_inside_profile(self):
        self.create('a', get_new_diff(101))
        self.logout()

        self.login(username='user1', password='asdfasdf')
        profile_params = {'_PROFILE_': 'laos'}
        json = self.read_many('a', 'json', params=profile_params)
        self.assertEqual(json['total'], 1)

    def test_read_moderator_does_not_see_pending_outside_profile(self):
        self.create('a', get_new_diff(101))
        self.logout()

        self.login(username='user2', password='asdfasdf')
        profile_params = {'_PROFILE_': 'laos'}
        json = self.read_many('a', 'json', params=profile_params)
        self.assertEqual(json['total'], 0)

    def test_read_single_activity_with_involvement(self):
        sh = self.create('sh', get_new_diff(201), return_uid=True)
        inv_data = [{
            'id': sh,
            'version': 1,
            'role': 6
        }]
        self.create(
            'a', get_new_diff(103, data=inv_data), return_uid=True)

        res = self.read_many('a', 'json')
        self.assertEqual(len(res.get('data')), 1)
        a = res.get('data')[0]
        self.assertEqual(len(a.get('involvements')), 1)

    def test_read_single_activity_with_pending_involvement(self):
        sh_uid = self.create('sh', get_new_diff(201), return_uid=True)
        self.review('sh', sh_uid)
        a_uid = self.create('a', get_new_diff(101), return_uid=True)
        self.review('a', a_uid)
        inv_data = [{
            'id': sh_uid,
            'version': 1,
            'role': 6
        }]
        self.create(
            'a', get_edit_diff(102, a_uid, data=inv_data))

        res = self.read_many('a', 'json')
        self.assertEqual(len(res.get('data')), 1)
        a = res.get('data')[0]
        self.assertEqual(len(a.get('involvements')), 1)

    def test_read_single_activity_with_pending_involvement_not_logged_in(self):
        sh_uid = self.create('sh', get_new_diff(201), return_uid=True)
        self.review('sh', sh_uid)
        a_uid = self.create('a', get_new_diff(101), return_uid=True)
        self.review('a', a_uid)
        inv_data = [{
            'id': sh_uid,
            'version': 1,
            'role': 6
        }]
        self.create(
            'a', get_edit_diff(102, a_uid, data=inv_data))
        self.logout()

        res = self.read_many('a', 'json')
        self.assertEqual(len(res.get('data')), 1)
        a = res.get('data')[0]
        self.assertIsNone(a.get('involvements'))

    # def test_read_activity_with_taggroup_geometry(self):
    #     self.login()
    #     self.create('a', get_new_diff(112))

    #     json = self.read_many('a', 'json')
    #     self.assertEqual(json['total'], 1)
    #     geom_taggroup = json.get('data')[0].get('taggroups')[1]
    #     self.assertIn('geometry', geom_taggroup)


@pytest.mark.read
@pytest.mark.usefixtures('app')
@pytest.mark.integration
@pytest.mark.activities
class ActivityReadManyGeojsonTests(LmkpTestCase):

    def setUp(self):
        self.request = testing.DummyRequest()
        settings = get_settings()
        self.config = testing.setUp(request=self.request, settings=settings)
        self.login()

    def tearDown(self):
        testing.tearDown()

    def test_activities_appear_in_read_many_geojson(self):
        json = self.read_many('a', 'geojson')
        self.assertEqual(json['features'], [])
        self.assertEqual(json['type'], 'FeatureCollection')

        uid = self.create('a', get_new_diff(101), return_uid=True)

        json = self.read_many('a', 'geojson')
        self.assertEqual(json['type'], 'FeatureCollection')
        self.assertEqual(len(json['features']), 1)
        f1 = json['features'][0]
        self.assertEqual(f1.get('geometry').get('type'), 'Point')
        self.assertEqual(len(f1.get('geometry').get('coordinates')), 2)
        self.assertEqual(f1.get('type'), 'Feature')
        self.assertEqual(len(f1.get('properties')), 4)
        self.assertEqual(f1.get('properties').get('activity_identifier'), uid)
        self.assertEqual(f1.get('properties').get('status'), 'pending')
        self.assertEqual(f1.get('properties').get('status_id'), 1)
        self.assertEqual(f1.get('properties').get('version'), 1)
        self.assertIn('id', f1)
        self.assertIn('fid', f1)

    def test_activities_geojson_single_attribute(self):
        self.create('a', get_new_diff(101))

        attributes = {'attributes': '[A] Dropdown 1'}
        json = self.read_many('a', 'geojson', params=attributes)
        self.assertEqual(len(json['features']), 1)
        f1 = json['features'][0]
        self.assertEqual(len(f1.get('properties')), 5)
        self.assertEqual(
            f1.get('properties').get('[A] Dropdown 1'), '[A] Value A1')

    def test_activities_geojson_multiple_attributes(self):
        self.create('a', get_new_diff(101))

        attributes = {'attributes': '[A] Dropdown 1,[A] Numberfield 1'}
        json = self.read_many('a', 'geojson', params=attributes)
        self.assertEqual(len(json['features']), 1)
        f1 = json['features'][0]
        self.assertEqual(len(f1.get('properties')), 6)
        self.assertEqual(
            f1.get('properties').get('[A] Dropdown 1'), '[A] Value A1')
        self.assertEqual(
            f1.get('properties').get('[A] Numberfield 1'), 123.45)

    def test_activities_geojson_attributes_translated(self):
        self.create('a', get_new_diff(101))

        attributes = {
            'attributes': '[A] Dropdown 1',
            '_LOCALE_': 'es'
        }
        json = self.read_many('a', 'geojson', params=attributes)
        self.assertEqual(len(json['features']), 1)
        f1 = json['features'][0]
        self.assertEqual(len(f1.get('properties')), 5)
        self.assertEqual(
            f1.get('properties').get('[A-T] Dropdown 1'), '[A-T] Value A1')


@pytest.mark.usefixtures('app')
@pytest.mark.integration
@pytest.mark.activities
class ActivityHistoryTests(LmkpTestCase):

    def test_history_view(self):
        """
        Test that a history view is available for newly created
        Activities.
        """
        self.login()
        uid = self.create('a', get_new_diff(101), return_uid=True)

        res = self.app.get('/activities/history/html/%s' % uid)
        self.assertEqual(res.status_int, 200)
        self.assertIn(TITLE_HISTORY_VIEW, res.body)
