import pytest

from ..base import (
    LmkpTestCase,
)
from ..diffs import (
    get_new_diff,
)


@pytest.mark.usefixtures('app')
@pytest.mark.integration
@pytest.mark.stakeholders
class StakeholderFilterTests(LmkpTestCase):

    def test_stakeholders_ilike_wildcard_filter(self):
        """
        Used in the search
        """
        self.login()
        uid = self.create('sh', get_new_diff(201), return_uid=True)

        filter = {
            'sh__[SH] Textfield 1__ilike': 'asdf'
        }
        json = self.read_many('sh', 'json', params=filter)
        self.assertEqual(json['total'], 1)
        self.assertEqual(json['data'][0]['id'], uid)

        filter = {
            'sh__[SH] Textfield 1__ilike': 'asd%'
        }
        json = self.read_many('sh', 'json', params=filter)
        self.assertEqual(json['total'], 1)
        self.assertEqual(json['data'][0]['id'], uid)

        filter = {
            'sh__[SH] Textfield 1__ilike': '%%sdf'
        }
        json = self.read_many('sh', 'json', params=filter)
        self.assertEqual(json['total'], 1)
        self.assertEqual(json['data'][0]['id'], uid)

        filter = {
            'sh__[SH] Textfield 1__ilike': '%%sd%'
        }
        json = self.read_many('sh', 'json', params=filter)
        self.assertEqual(json['total'], 1)
        self.assertEqual(json['data'][0]['id'], uid)

        filter = {
            'sh__[SH] Textfield 1__ilike': '*sd*'
        }
        json = self.read_many('sh', 'json', params=filter)
        self.assertEqual(json['total'], 1)
        self.assertEqual(json['data'][0]['id'], uid)

        filter = {
            'sh__[SH] Textfield 1__ilike': '%%foo%'
        }
        json = self.read_many('sh', 'json', params=filter)
        self.assertEqual(json['total'], 0)
