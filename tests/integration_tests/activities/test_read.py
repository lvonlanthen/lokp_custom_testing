import pytest

from ..base import (
    LmkpTestCase,
    get_base_url_by_item_type,
    get_involvements_from_item_json,
)
from ..diffs import (
    get_new_diff,
    get_edit_diff,
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

    def test_change_involvement_role_does_not_create_duplicate_invs(self):
        self.login()
        sh_uid = self.create('sh', get_new_diff(201), return_uid=True)
        self.review('sh', sh_uid)

        inv_data = [{
            'id': sh_uid,
            'version': 1,
            'role': 6
        }]
        a_uid = self.create(
            'a', get_new_diff(103, data=inv_data), return_uid=True)
        self.review('a', a_uid)

        inv_data = [{
            'id': sh_uid,
            'version': 2,
            'role': 6,
            'op': 'delete'
        }, {
            'id': sh_uid,
            'version': 2,
            'role': 5,
            'op': 'add'
        }]
        self.create(
            'a', get_edit_diff(102, a_uid, version=1, data=inv_data))

        res = self.read_one('sh', sh_uid)
        inv_v1 = get_involvements_from_item_json(res)
        self.assertEqual(len(inv_v1), 1)


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
