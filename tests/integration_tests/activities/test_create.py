import pytest

from ..base import (
    LmkpTestCase,
    get_status_from_item_json,
    get_involvements_from_item_json,
)
from ..diffs import (
    get_new_diff,
)
from ...base import (
    FEEDBACK_LOGIN_NEEDED,
    STATUS_PENDING,
)


@pytest.mark.usefixtures('app')
@pytest.mark.integration
@pytest.mark.activities
class ActivityCreateTests(LmkpTestCase):

    def test_activity_cannot_be_created_without_login(self):
        """
        New Activities cannot be created if the user is not logged in.
        """
        res = self.create('a', {})

        self.assertEqual(res.status_int, 200)
        res.mustcontain(FEEDBACK_LOGIN_NEEDED)

    def test_activity_can_be_created(self):
        """
        New Activities can be created if the user is logged in.
        """
        self.login()
        res = self.create('a', get_new_diff('a'))
        self.assertEqual(res.status_int, 201)
        json = res.json
        self.assertEqual(json['total'], 1)
        self.assertTrue(json['created'])
        self.assertEqual(len(json['data']), 1)
        self.assertIn('id', json['data'][0])

    def test_new_activities_appear_in_read_many_json_service(self):
        """
        Newly created Activities appear in the JSON service "read many".
        """
        self.login()

        json = self.read_many('a', 'json')
        self.assertEqual(json['data'], [])
        self.assertEqual(json['total'], 0)

        self.create('a', get_new_diff('a'))

        json = self.read_many('a', 'json')
        self.assertEqual(json['total'], 1)

    def test_new_activities_with_existing_stakeholder_can_be_created(self):
        """
        New Activities can be created with an existing (active) Stakeholder
        attached to it.
        This also creates a new version of the Stakeholder.
        """
        self.login()

        sh_uid = self.create('sh', get_new_diff('sh'), return_uid=True)
        self.review('sh', sh_uid)

        res = self.read_one('sh', sh_uid, 'json')
        status = get_status_from_item_json(res)
        self.assertEqual('active', status)

        inv_data = [{
            'id': sh_uid,
            'version': 1,
            'role': 6
        }]
        a_uid = self.create(
            'a', get_new_diff('a', 3, data=inv_data), return_uid=True)

        # One pending Activity version should have been created, with the
        # Stakeholder (version 2, pending) attached to it
        res = self.read_one('a', a_uid, 'json')
        self.assertEqual(res['total'], 1)
        status = get_status_from_item_json(res)
        self.assertEqual(STATUS_PENDING, status)
        inv = get_involvements_from_item_json(res)[0]['data']
        self.assertEqual(inv['id'], sh_uid)
        self.assertEqual(inv['version'], 2)
        self.assertEqual(inv['status_id'], 1)

        # On the Stakeholder side, there should be 2 versions: Version 1 is
        # still active, version 2 is pending and contains the involvement to
        # the Activity (version 1, pending). Note that the newest version is
        # on top!
        res = self.read_one('sh', sh_uid, 'json')
        self.assertEqual(res['total'], 2)
        self.assertEqual(res['data'][1]['status_id'], 2)
        self.assertEqual(res['data'][0]['status_id'], 1)
        self.assertTrue('involvements' not in res['data'][1])
        inv = get_involvements_from_item_json(res)[0]['data']
        self.assertEqual(inv['id'], a_uid)
        self.assertEqual(inv['version'], 1)
        self.assertEqual(inv['status_id'], 1)

    def test_new_activities_with_new_involvement_can_be_created(self):
        """
        New Activities can be created with a new pending Stakeholder attached
        to it. This results in 2 pending SH versions (1 blank, 1 with the
        Involvement) and 1 A version.
        """
        self.login()

        sh_uid = self.create('sh', get_new_diff('sh'), return_uid=True)

        inv_data = [{
            'id': sh_uid,
            'version': 1,
            'role': 6
        }]
        a_uid = self.create(
            'a', get_new_diff('a', 3, data=inv_data), return_uid=True)

        # One pending Activity version should have been created, with the
        # Stakeholder (version 2, pending) attached to it
        res = self.read_one('a', a_uid, 'json')
        self.assertEqual(res['total'], 1)
        status = get_status_from_item_json(res)
        self.assertEqual(STATUS_PENDING, status)
        inv = get_involvements_from_item_json(res)[0]['data']
        self.assertEqual(inv['id'], sh_uid)
        self.assertEqual(inv['version'], 2)
        self.assertEqual(inv['status_id'], 1)

        # On the Stakeholder side, there should be 2 versions: Version 1 is now
        # inactive, version 2 is pending and contains the involvement to the
        # Activity (version 1, pending). Note that the newest version is on
        # top!
        res = self.read_one('sh', sh_uid, 'json')
        self.assertEqual(res['total'], 2)
        self.assertEqual(res['data'][1]['status_id'], 1)
        self.assertEqual(res['data'][0]['status_id'], 1)
        self.assertTrue('involvements' not in res['data'][1])
        inv = get_involvements_from_item_json(res)[0]['data']
        self.assertEqual(inv['id'], a_uid)
        self.assertEqual(inv['version'], 1)
        self.assertEqual(inv['status_id'], 1)
