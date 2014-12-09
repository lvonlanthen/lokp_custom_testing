import pytest
import uuid
from pyramid import testing
from ...base import get_settings

from ..base import (
    LmkpTestCase,
    get_base_url_by_item_type,
)
from ..diffs import (
    get_edit_diff,
    get_new_diff,
)
from ...base import (
    FEEDBACK_HISTORY_NOT_FOUND,
    TEXT_INACTIVE_VERSION,
    TITLE_HISTORY_RSS,
    TITLE_HISTORY_VIEW,
)


@pytest.mark.read
@pytest.mark.usefixtures('app')
@pytest.mark.integration
@pytest.mark.stakeholders
class StakeholderReadOneJSONTests(LmkpTestCase):

    def setUp(self):
        self.request = testing.DummyRequest()
        settings = get_settings()
        self.config = testing.setUp(request=self.request, settings=settings)
        self.login()

    def tearDown(self):
        testing.tearDown()

    def test_read_one_json_returns_empty_if_not_found(self):
        json = self.read_one('sh', uuid.uuid4(), 'json')
        self.assertEqual(json, {})

    def test_stakeholder_appears_in_read_one_json(self):
        uid = self.create('sh', get_new_diff(201), return_uid=True)

        json = self.read_one('sh', uid, 'json')
        self.assertEqual(json.get('status'), 'pending')
        self.assertEqual(json.get('status_id'), 1)
        self.assertIsNone(json['previous_version'])
        self.assertNotIn('geometry', json)
        self.assertEqual(json.get('version'), 1)
        self.assertIn('timestamp', json)
        self.assertIn('id', json)
        self.assertEqual(len(json.get('taggroups')), 2)
        tg1 = json.get('taggroups')[0]
        self.assertEqual(tg1.get('tg_id'), 1)
        self.assertEqual(tg1.get('main_tag').get('key'), '[SH] Numberfield 1')
        self.assertEqual(tg1.get('main_tag').get('value'), '123.0')
        self.assertEqual(len(tg1.get('tags')), 1)
        t1 = tg1.get('tags')[0]
        self.assertEqual(t1.get('key'), '[SH] Numberfield 1')
        self.assertEqual(t1.get('value'), '123.0')
        tg2 = json.get('taggroups')[1]
        self.assertEqual(tg2.get('tg_id'), 2)
        self.assertEqual(tg2.get('main_tag').get('key'), '[SH] Textfield 1')
        self.assertEqual(tg2.get('main_tag').get('value'), 'asdf')
        self.assertEqual(len(tg2.get('tags')), 1)
        t2 = tg2.get('tags')[0]
        self.assertEqual(t2.get('key'), '[SH] Textfield 1')
        self.assertEqual(t2.get('value'), 'asdf')

    def test_stakeholder_read_one_json_public_does_not_see_pending(self):

        json = self.read_one('sh', uuid.uuid4(), 'json')
        self.assertEqual(json, {})

        uid = self.create('sh', get_new_diff(201), return_uid=True)
        self.logout()

        json = self.read_one('sh', uid, 'json')
        self.assertEqual(json, {})

    def test_stakeholder_read_one_json_by_version_logged_in(self):
        uid = self.create('sh', get_new_diff(201), return_uid=True)
        self.create('sh', get_edit_diff(201, uid))
        self.create('sh', get_edit_diff(201, uid, version=2))

        json = self.read_one('sh', uid, 'json')
        self.assertEqual(json.get('version'), 3)

        json = self.read_one('sh', uid, 'json', params={'v': 2})
        self.assertEqual(json.get('version'), 2)

        self.logout()
        json = self.read_one('sh', uid, 'json', params={'v': 2})
        self.assertEqual(json, {})

    def test_stakeholder_read_one_json_by_version_moderator(self):
        # Create SH as user1
        self.logout()
        self.login(username='user1', password='asdfasdf')
        uid = self.create('sh', get_new_diff(201), return_uid=True)
        self.create('sh', get_edit_diff(201, uid))
        self.create('sh', get_edit_diff(201, uid, version=2))

        # Admin is moderator, can see pending
        self.logout()
        self.login()
        profile_params = {'_PROFILE_': 'global'}
        json = self.read_one('sh', uid, 'json', params=profile_params)
        self.assertEqual(json.get('version'), 3)
        json = self.read_one('sh', uid, 'json', params={'v': 2})
        self.assertEqual(json.get('version'), 2)

        # User 2 is moderator of cambodia, cannot see pending in laos
        self.logout()
        self.login(username='user2', password='asdfasdf')
        profile_params = {'_PROFILE_': 'laos'}
        json = self.read_one('sh', uid, 'json', params=profile_params)
        self.assertEqual(json, {})
        json = self.read_one('sh', uid, 'json', params={'v': 2})
        self.assertEqual(json, {})


@pytest.mark.read
@pytest.mark.usefixtures('app')
@pytest.mark.integration
@pytest.mark.stakeholders
class StakeholderReadOneHTMLTests(LmkpTestCase):

    def setUp(self):
        self.request = testing.DummyRequest()
        settings = get_settings()
        self.config = testing.setUp(request=self.request, settings=settings)
        self.login()

    def tearDown(self):
        testing.tearDown()

    def test_read_one_html_returns_404_if_not_found(self):
        url = get_base_url_by_item_type('sh')
        html = self.app.get('%s/html/%s' % (url, uuid.uuid4()), status=404)
        self.assertEqual(html.status_int, 404)

    def test_read_one_html_finds_activity(self):

        uid = self.create('sh', get_new_diff(201), return_uid=True)
        html = self.read_one('sh', uid, 'html')

        self.assertIn(uid, html)

    def test_read_one_html_finds_activity_by_version(self):
        uid = self.create('sh', get_new_diff(201), return_uid=True)
        self.create('sh', get_edit_diff(201, uid))
        self.create('sh', get_edit_diff(201, uid, version=2))

        html_v2 = self.read_one('sh', uid, 'html', params={'v': 2})
        self.assertIn(uid, html_v2)
        self.assertIn(TEXT_INACTIVE_VERSION, html_v2)


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


@pytest.mark.read
@pytest.mark.usefixtures('app')
@pytest.mark.integration
@pytest.mark.stakeholders
class StakeholderReadManyByActivitiesTests(LmkpTestCase):

    def setUp(self):
        self.request = testing.DummyRequest()
        settings = get_settings()
        self.config = testing.setUp(request=self.request, settings=settings)
        self.login()

    def tearDown(self):
        testing.tearDown()

    def test_read_many_by_a_basic(self):
        self.create('sh', get_new_diff(201), return_uid=True)
        sh2 = self.create('sh', get_new_diff(201), return_uid=True)
        inv_data = [{
            'id': sh2,
            'version': 1,
            'role': 6
        }]
        self.create(
            'a', get_new_diff(103, data=inv_data), return_uid=True)

        res = self.read_by('sh', 'json')
        self.assertEqual(len(res.get('data')), 1)
        res_1 = res.get('data')[0]
        self.assertEqual(res_1.get('id'), sh2)


@pytest.mark.usefixtures('app')
@pytest.mark.integration
@pytest.mark.stakeholders
class StakeholderHistoryTests(LmkpTestCase):

    def setUp(self):
        self.request = testing.DummyRequest()
        settings = get_settings()
        self.config = testing.setUp(request=self.request, settings=settings)
        self.login()

    def tearDown(self):
        testing.tearDown()

    def test_history_view_json(self):
        uid = self.create('sh', get_new_diff(201), return_uid=True)

        res = self.app.get('/stakeholders/history/json/%s' % uid)
        self.assertEqual(res.status_int, 200)
        self.assertEqual(res.json.get('total'), 1)
        self.assertEqual(len(res.json.get('data')), 1)
        a1 = res.json.get('data')[0]
        self.assertEqual(a1.get('id'), uid)

    def test_history_view_json_not_found(self):
        uid = str(uuid.uuid4())

        res = self.app.get('/stakeholders/history/json/%s' % uid)
        self.assertEqual(res.status_int, 200)
        self.assertEqual(res.json.get('total'), 0)
        self.assertEqual(res.json.get('data'), [])

    def test_history_view_html(self):
        uid = self.create('sh', get_new_diff(201), return_uid=True)

        res = self.app.get('/stakeholders/history/html/%s' % uid)
        self.assertEqual(res.status_int, 200)
        self.assertIn(TITLE_HISTORY_VIEW, res)
        self.assertIn(uid, res)

    def test_history_view_html_not_found(self):
        uid = str(uuid.uuid4())

        res = self.app.get('/stakeholders/history/html/%s' % uid)
        self.assertEqual(res.status_int, 200)
        self.assertIn(TITLE_HISTORY_VIEW, res)
        self.assertIn(FEEDBACK_HISTORY_NOT_FOUND, res)

    def test_history_view_rss(self):
        uid = self.create('sh', get_new_diff(201), return_uid=True)

        res = self.app.get('/stakeholders/history/rss/%s' % uid)
        self.assertEqual(res.status_int, 200)
        self.assertIn(TITLE_HISTORY_RSS, res)
        self.assertIn(uid, res)

    def test_history_view_rss_not_found(self):
        uid = str(uuid.uuid4())
        res = self.app.get('/stakeholders/history/rss/%s' % uid, status=404)
        self.assertEqual(res.status_int, 404)
