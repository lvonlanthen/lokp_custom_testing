import pytest

from .base import (
    LmkpTestCase
)
from .diffs import (
    get_new_diff,
)
from lmkp.views.evaluation import EvaluationView


@pytest.mark.usefixtures('app')
@pytest.mark.integration
class EvaluationTests(LmkpTestCase):

    def setUp(self):
        self.data1 = {
            'item': 'Activity',
            'attributes': {
                'Activity': 'count'
            },
            'group_by': ['[A] Dropdown 1']
        }
        self.data2 = {
            'item': 'Activity',
            'attributes': {
                'Activity': 'count',
                '[A] Numberfield 1': 'sum'
            },
            'translate': {
                'keys': [
                    ['[A] Dropdown 1']
                ]
            },
            'group_by': ['[A] Dropdown 1'],
            'locales': ['es']
        }
        self.data3 = {
            'item': 'Activity',
            'attributes': {
                'Activity': 'count',
                '[A] Numberfield 1': 'sum'
            },
            'translate': {
                'keys': [
                    ['[A] Dropdown 1', '[A] Dropdown 2'],
                    ['[A] Textfield 1']
                ]
            },
            'group_by': ['[A] Dropdown 1', '[A] Dropdown 2']
        }
        self.login()
        super(EvaluationTests, self).setUp()
        self.view = EvaluationView(self.request)

        # Create some Activities
        created_activities = [101, 104, 101, 106, 109]
        for a in created_activities:
            uid = self.create('a', get_new_diff(a), return_uid=True)
            self.review('a', uid)

    def test_check_basic_format(self):
        res = self.view.evaluation(data=self.data3)
        self.assertTrue(res.get('success'))
        self.assertIn('data', res)
        self.assertIn('translate', res)

    def test_group_by_one_attribute(self):
        res = self.view.evaluation(data=self.data1)
        self.assertEqual(len(res.get('data')), 2)
        for d in res.get('data'):
            self.assertIn('values', d)
            self.assertEqual(len(d.get('values')), 1)
            self.assertIn('group', d)

    def test_group_by_two_attributes(self):
        res = self.view.evaluation(data=self.data3)
        self.assertEqual(len(res.get('data')), 2)
        d1 = res.get('data')[0]
        d2 = res.get('data')[1]
        children = []
        self.assertEqual(len(d1.get('children')), 3)
        children.extend(d1.get('children'))
        self.assertEqual(len(d2.get('children')), 1)
        children.extend(d2.get('children'))
        for c in children:
            self.assertIn('values', c)
            self.assertEqual(len(c.get('values')), 2)
            self.assertIn('group', c)

    def test_group_names_with_label(self):
        res = self.view.evaluation(data=self.data1)
        group = res.get('data')[0].get('group')
        self.assertIn('key', group)
        k = group.get('key')
        self.assertEqual(k.get('key'), '[A] Dropdown 1')
        self.assertEqual(k.get('default'), '[A] Dropdown 1')
        self.assertIn('value', group)
        v = group.get('value')
        self.assertEqual(v.get('value'), '[A] Value A1')
        self.assertEqual(v.get('default'), '[A] Value A1')

    def test_group_names_are_translated_automatically(self):
        self.request.params = {'_LOCALE_': 'es'}
        res = self.view.evaluation(data=self.data1)
        group = res.get('data')[0].get('group')
        self.assertIn('key', group)
        k = group.get('key')
        self.assertEqual(k.get('key'), '[A] Dropdown 1')
        self.assertEqual(k.get('default'), '[A-T] Dropdown 1')
        self.assertIn('value', group)
        v = group.get('value')
        self.assertEqual(v.get('value'), '[A] Value A1')
        self.assertEqual(v.get('default'), '[A-T] Value A1')

    def test_group_names_are_translated_by_parameter(self):
        res = self.view.evaluation(data=self.data2)
        group = res.get('data')[0].get('group')
        self.assertIn('key', group)
        k = group.get('key')
        self.assertEqual(k.get('key'), '[A] Dropdown 1')
        self.assertEqual(k.get('default'), '[A] Dropdown 1')
        self.assertEqual(k.get('es'), '[A-T] Dropdown 1')
        self.assertIn('value', group)
        v = group.get('value')
        self.assertEqual(v.get('value'), '[A] Value A1')
        self.assertEqual(v.get('default'), '[A] Value A1')
        self.assertEqual(v.get('es'), '[A-T] Value A1')

    def test_group_names_are_translated_by_parameter_identical_lang(self):
        self.request.params = {'_LOCALE_': 'es'}
        res = self.view.evaluation(data=self.data2)
        group = res.get('data')[0].get('group')
        self.assertIn('key', group)
        k = group.get('key')
        self.assertEqual(k.get('key'), '[A] Dropdown 1')
        self.assertEqual(k.get('default'), '[A-T] Dropdown 1')
        self.assertEqual(k.get('es'), '[A-T] Dropdown 1')
        self.assertIn('value', group)
        v = group.get('value')
        self.assertEqual(v.get('value'), '[A] Value A1')
        self.assertEqual(v.get('default'), '[A-T] Value A1')
        self.assertEqual(v.get('es'), '[A-T] Value A1')

    def test_value_key_names_are_translated_automatically(self):
        self.request.params = {'_LOCALE_': 'es'}
        res = self.view.evaluation(data=self.data3)
        value = res.get('data')[0].get('children')[0].get('values')[0]
        self.assertIn('key', value)
        k = value.get('key')
        self.assertEqual(k.get('key'), '[A] Numberfield 1')
        self.assertEqual(k.get('default'), '[A-T] Numberfield 1')
        self.assertEqual(value.get('value'), 123.45)

    def test_value_key_names_are_translated_by_parameter(self):
        res = self.view.evaluation(data=self.data2)
        value = res.get('data')[0].get('values')[0]
        self.assertIn('key', value)
        k = value.get('key')
        self.assertEqual(k.get('key'), '[A] Numberfield 1')
        self.assertEqual(k.get('default'), '[A] Numberfield 1')
        self.assertEqual(k.get('es'), '[A-T] Numberfield 1')
        self.assertEqual(value.get('value'), 493.8)

    def test_value_key_names_are_translated_by_parameter_identical_lang(self):
        self.request.params = {'_LOCALE_': 'es'}
        res = self.view.evaluation(data=self.data2)
        value = res.get('data')[0].get('values')[0]
        self.assertIn('key', value)
        k = value.get('key')
        self.assertEqual(k.get('key'), '[A] Numberfield 1')
        self.assertEqual(k.get('default'), '[A-T] Numberfield 1')
        self.assertEqual(k.get('es'), '[A-T] Numberfield 1')
        self.assertEqual(value.get('value'), 493.8)

    def test_keys_are_translated_automatically(self):
        self.request.params = {'_LOCALE_': 'es'}
        res = self.view.evaluation(data=self.data3)
        translate_keys = res.get('translate').get('keys')
        self.assertEqual(len(translate_keys), 2)
        g1 = translate_keys[0]
        g2 = translate_keys[1]
        self.assertEqual(len(g1), 2)
        g1_1 = g1[0]
        g1_2 = g1[1]
        self.assertEqual(g1_1.get('key'), '[A] Dropdown 1')
        self.assertEqual(g1_1.get('default'), '[A-T] Dropdown 1')
        self.assertEqual(g1_2.get('key'), '[A] Dropdown 2')
        self.assertEqual(g1_2.get('default'), '[A-T] Dropdown 2')
        self.assertEqual(len(g2), 1)
        g2_1 = g2[0]
        self.assertEqual(g2_1.get('key'), '[A] Textfield 1')
        self.assertEqual(g2_1.get('default'), '[A-T] Identical Translation')

    def test_keys_are_translated_by_parameter(self):
        res = self.view.evaluation(data=self.data2)
        translate_keys = res.get('translate').get('keys')
        self.assertEqual(len(translate_keys), 1)
        g1 = translate_keys[0]
        self.assertEqual(len(g1), 1)
        g1_1 = g1[0]
        self.assertEqual(g1_1.get('key'), '[A] Dropdown 1')
        self.assertEqual(g1_1.get('default'), '[A] Dropdown 1')
        self.assertEqual(g1_1.get('es'), '[A-T] Dropdown 1')

    def test_keys_are_translated_by_parameter_identical_lang(self):
        self.request.params = {'_LOCALE_': 'es'}
        res = self.view.evaluation(data=self.data2)
        translate_keys = res.get('translate').get('keys')
        self.assertEqual(len(translate_keys), 1)
        g1 = translate_keys[0]
        self.assertEqual(len(g1), 1)
        g1_1 = g1[0]
        self.assertEqual(g1_1.get('key'), '[A] Dropdown 1')
        self.assertEqual(g1_1.get('default'), '[A-T] Dropdown 1')
        self.assertEqual(g1_1.get('es'), '[A-T] Dropdown 1')
