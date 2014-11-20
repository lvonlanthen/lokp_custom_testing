import pytest

from ..base import (
    LmkpTestCase,
    get_base_url_by_item_type,
)
from ..diffs import (
    get_new_diff,
)
from ...base import (
    TITLE_HISTORY_VIEW,
)


@pytest.mark.usefixtures('app')
@pytest.mark.integration
@pytest.mark.activities
class ActivityReadManyTests(LmkpTestCase):

    def test_activities_appear_in_read_many_json(self):
        """
        Newly created Activities appear in the JSON service "read many".
        """
        self.login()

        json = self.read_many('a', 'json')
        self.assertEqual(json['data'], [])
        self.assertEqual(json['total'], 0)

        self.create('a', get_new_diff(101))

        json = self.read_many('a', 'json')
        self.assertEqual(json['total'], 1)

    def test_only_active_activities_appear_in_many_json_public(self):
        self.login()
        uid_1 = self.create('a', get_new_diff(101), return_uid=True)
        self.review('a', uid_1)
        self.create('a', get_new_diff(101))

        url = get_base_url_by_item_type('a')
        json = self.app.get('%s/public/json' % url).json

        self.assertEqual(json['total'], 1)
        self.assertEqual(json['data'][0]['id'], uid_1)

    def test_activities_appear_in_read_many_html(self):
        self.login()

        uid = self.create('a', get_new_diff(101), return_uid=True)
        url = get_base_url_by_item_type('a')
        res = self.app.get('%s/html' % url)

        self.assertIn(uid, res)

    def test_activities_appear_in_read_many_html_public(self):
        self.login()

        uid_1 = self.create('a', get_new_diff(101), return_uid=True)
        self.review('a', uid_1)
        uid_2 = self.create('a', get_new_diff(101), return_uid=True)

        url = get_base_url_by_item_type('a')
        res = self.app.get('%s/public/html' % url)

        self.assertIn(uid_1, res)
        self.assertNotIn(uid_2, res)

    def test_activities_order_default_by_timestamp(self):
        self.login()

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
        self.login()

        uid_1 = self.create('a', get_new_diff(101), return_uid=True)  # 123.4
        uid_2 = self.create('a', get_new_diff(110), return_uid=True)  # 999
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
        self.login()

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
