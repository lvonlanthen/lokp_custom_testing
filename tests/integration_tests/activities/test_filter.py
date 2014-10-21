#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pytest

from ..base import (
    LmkpTestCase,
)
from ..diffs import (
    get_new_diff,
)


@pytest.mark.usefixtures('app')
@pytest.mark.integration
@pytest.mark.activities
class ActivityFilterTests(LmkpTestCase):

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
            'a__éèà__ilike': 'üäö'
        }
        json = self.read_many('a', 'json', params=filter)
        self.assertEqual(json['total'], 0)
        html = self.read_many('a', 'html', params=filter)
        self.assertEqual(html.status_int, 200)
