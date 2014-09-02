#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pytest

from ..integration_tests.base import (
    LmkpTestCase,
)
from lmkp.views.protocol import (
    get_value_by_key_from_item_json,
    get_main_keys_from_item_json
)


@pytest.mark.usefixtures('app')
@pytest.mark.unittest
@pytest.mark.protocol
class GetValueByKeyFromItemJsonTest(LmkpTestCase):

    def test_get_value_by_key_from_item_json_handles_invalid_json(self):
        json = {'foo': 'bar'}
        self.assertIsNone(get_value_by_key_from_item_json(json, 'xyz'))

    def test_get_value_by_key_from_item_json_handles_non_json(self):
        json = 'foo'
        self.assertIsNone(get_value_by_key_from_item_json(json, 'xyz'))

    def test_get_value_by_key_from_item_json_finds_value(self):
        json = {
            'taggroups': [
                {
                    'tags': [
                        {
                            'key': 'abc',
                            'value': 'def'
                        }, {
                            'key': 'foo',
                            'value': 'bar'
                        }
                    ]
                }, {
                    'tags': [
                        {
                            'key': 'xyz',
                            'value': 123.45
                        }
                    ]
                }
            ]
        }
        self.assertEqual(get_value_by_key_from_item_json(json, 'foo'), 'bar')
        self.assertEqual(get_value_by_key_from_item_json(json, 'xyz'), 123.45)

    def test_get_value_by_key_from_item_json_finds_value_by_special_char(self):
        json = {
            'taggroups': [
                {
                    'tags': [
                        {
                            'key': 'ສອບ',
                            'value': 'dróżką'
                        }
                    ]
                }
            ]
        }
        self.assertEqual(
            get_value_by_key_from_item_json(json, 'ສອບ'), 'dróżką')

    def test_get_value_by_key_from_item_json_finds_first_value(self):
        json = {
            'taggroups': [
                {
                    'tags': [
                        {
                            'key': 'abc',
                            'value': 'foo'
                        }, {
                            'key': 'abc',
                            'value': 'bar'
                        }
                    ]
                }
            ]
        }
        self.assertEqual(get_value_by_key_from_item_json(json, 'abc'), 'foo')


@pytest.mark.usefixtures('app')
@pytest.mark.unittest
@pytest.mark.protocol
class GetMainKeysFromItemJsonTest(LmkpTestCase):

    def test_get_main_keys_from_item_json_handles_invalid_json(self):
        json = {'foo': 'bar'}
        self.assertEqual(get_main_keys_from_item_json(json), [])

    def test_get_value_by_key_from_item_json_finds_invalid_json2(self):
        json = {
            'taggroups': [
                {
                    'main_tag': {
                        'foo': 'abc'
                    }
                }, {
                    'tags': [
                        {
                            'key': 'foo',
                            'value': 'bar'
                        }
                    ]
                }
            ]
        }
        self.assertEqual(get_main_keys_from_item_json(json), [])

    def test_get_main_keys_from_item_json_handles_non_json(self):
        json = 'foo'
        self.assertEqual(get_main_keys_from_item_json(json), [])

    def test_get_main_keys_from_item_json_returns_main_keys(self):
        json = {
            'taggroups': [
                {
                    'main_tag': {
                        'key': 'abc',
                        'value': 'def'
                    },
                    'tags': [
                        {
                            'key': 'abc',
                            'value': 'def'
                        }, {
                            'key': 'foo',
                            'value': 'bar'
                        }
                    ]
                }, {
                    'main_tag': {
                        'key': 'xyz',
                        'value': 123.45
                    },
                    'tags': [
                        {
                            'key': 'xyz',
                            'value': 123.45
                        }
                    ]
                }
            ]
        }
        self.assertEqual(get_main_keys_from_item_json(json), ['abc', 'xyz'])
