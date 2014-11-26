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

    @pytest.mark.asdf
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
        print res
        self.assertEqual(len(res.get('data')), 1)
        a = res.get('data')[0]
        self.assertEqual(len(a.get('involvements')), 1)

        self.fail()

    # def test_read_activity_with_taggroup_geometry(self):
    #     self.login()
    #     self.create('a', get_new_diff(112))

    #     json = self.read_many('a', 'json')
    #     self.assertEqual(json['total'], 1)
    #     geom_taggroup = json.get('data')[0].get('taggroups')[1]
    #     self.assertIn('geometry', geom_taggroup)


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
