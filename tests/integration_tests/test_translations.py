# -*- coding: utf-8 -*-

import pytest

from .base import (
    LmkpTestCase
)
from .diffs import get_new_diff
from lmkp.views.translation import get_translated_keys


@pytest.mark.usefixtures('app')
@pytest.mark.integration
class TranslationTests(LmkpTestCase):

    def test_default_gui_language_is_english(self):
        """
        Test that the title of Map View is in English by default.
        """
        res = self.app.get('/map')
        res.mustcontain('Map View')

    def test_spanish_gui_translation_is_available(self):
        """
        Test that the title of Map View is translated to Spanish.
        """
        res = self.app.get('/map?_LOCALE_=es')
        res.mustcontain('En Español')

    def test_french_gui_translation_is_available(self):
        """
        Test that the title of Map View is translated to French.
        """
        res = self.app.get('/map?_LOCALE_=fr')
        res.mustcontain('En Français')

    def test_database_values_are_translated_in_form(self):
        """
        Test that the form displays translated values.
        """
        self.login()
        res = self.app.get('/activities/form?_LOCALE_=es')
        res.mustcontain('[A-T] Dropdown 1')

    def test_database_values_are_translated_in_details_page(self):
        """
        Test that the details page displays translated database values.
        """
        self.login()
        a_uid = self.create('a', get_new_diff(101), return_uid=True)
        res = self.app.get('/activities/html/%s' % a_uid)
        res.mustcontain('[A] Dropdown 1')
        res.mustcontain('[A] Value A1')
        res = self.app.get('/activities/html/%s?_LOCALE_=es' % a_uid)
        res.mustcontain('[A-T] Dropdown 1')
        res.mustcontain('[A-T] Value A1')


@pytest.mark.usefixtures('app')
@pytest.mark.integration
class TranslationGetTranslatedKeysTests(LmkpTestCase):

    def test_get_translated_keys_returns_a_keys(self):
        keys = ['[A] Dropdown 1', '[A] Textarea 1']
        t = get_translated_keys('a', keys, 'es')
        self.assertEqual(len(keys), len(t))
        k1 = t[1]
        self.assertEqual(k1[0], keys[0])
        self.assertEqual(k1[1], '[A-T] Dropdown 1')
        k2 = t[0]
        self.assertEqual(k2[0], keys[1])
        self.assertEqual(k2[1], '[A-T] Textarea 1')

    def test_get_translated_keys_handles_invalid_locale(self):
        keys = ['[A] Dropdown 1', '[A] Textarea 1']
        t = get_translated_keys('a', keys, 'foo')
        self.assertEqual(t, [])

    def test_get_translated_keys_handles_invalid_keys(self):
        keys = ['foo', 'bar']
        t = get_translated_keys('a', keys, 'es')
        self.assertEqual(t, [])

    def test_get_translated_keys_returns_sh_keys(self):
        keys = ['[SH] Integerfield 1', '[SH] Numberfield 1']
        t = get_translated_keys('sh', keys, 'es')
        self.assertEqual(len(keys), len(t))
        k1 = t[0]
        self.assertEqual(k1[0], keys[0])
        self.assertEqual(k1[1], '[SH-T] Integerfield 1')
        k2 = t[1]
        self.assertEqual(k2[0], keys[1])
        self.assertEqual(k2[1], '[SH-T] Numberfield 1')
