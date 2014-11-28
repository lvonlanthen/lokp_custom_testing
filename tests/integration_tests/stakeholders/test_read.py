import pytest
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
    TITLE_HISTORY_VIEW,
)


@pytest.mark.read
@pytest.mark.usefixtures('app')
@pytest.mark.integration
@pytest.mark.stakeholders
class StakeholderReadManyTests(LmkpTestCase):

    def setUp(self):
        self.request = testing.DummyRequest()
        settings = get_settings()
        self.config = testing.setUp(request=self.request, settings=settings)
        self.login()

    def tearDown(self):
        testing.tearDown()

    def test_stakeholders_appear_in_read_many_json(self):
        json = self.read_many('sh', 'json')
        self.assertEqual(json['data'], [])
        self.assertEqual(json['total'], 0)

        self.create('sh', get_new_diff(201))

        json = self.read_many('sh', 'json')
        self.assertEqual(json['total'], 1)

    def test_read_single_stakeholder_with_involvement(self):
        sh = self.create('sh', get_new_diff(201), return_uid=True)
        inv_data = [{
            'id': sh,
            'version': 1,
            'role': 6
        }]
        self.create(
            'a', get_new_diff(103, data=inv_data), return_uid=True)

        res = self.read_many('sh', 'json')
        self.assertEqual(len(res.get('data')), 1)
        sh = res.get('data')[0]
        self.assertEqual(len(sh.get('involvements')), 1)

    def test_stakeholders_with_activities_filter(self):
        sh_uid_1 = self.create('sh', get_new_diff(201), return_uid=True)
        sh_uid_2 = self.create('sh', get_new_diff(201), return_uid=True)
        inv_data_1 = [{
            'id': sh_uid_1,
            'version': 1,
            'role': 6
        }]
        self.create(
            'a', get_new_diff(103, data=inv_data_1), return_uid=True)
        inv_data_2 = [{
            'id': sh_uid_2,
            'version': 1,
            'role': 6
        }]
        a_uid_2 = self.create(
            'a', get_new_diff(106, data=inv_data_2), return_uid=True)

        filter_params = {'a__[A] Checkbox 1__like': '[A] Value D2'}
        res = self.read_many('sh', 'json', params=filter_params)
        self.assertEqual(len(res.get('data')), 1)
        res_1 = res.get('data')[0]
        self.assertEqual(res_1.get('id'), sh_uid_2)
        inv_1 = res_1.get('involvements')
        self.assertEqual(len(inv_1), 1)
        self.assertEqual(inv_1[0].get('id'), a_uid_2)
