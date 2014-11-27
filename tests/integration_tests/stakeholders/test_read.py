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
