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
    FEEDBACK_NO_GEOMETRY_PROVIDED,
    FEEDBACK_NOT_VALID_FORMAT,
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

    def test_cannot_create_empty_activity(self):
        """
        When trying to create an Activity with an empty JSON, a 400
        (Bad Response) code is returned with an error message in the
        body.
        """
        self.login()
        res = self.create('a', {}, expect_errors=True)
        self.assertEqual(res.status_int, 400)
        res.mustcontain(FEEDBACK_NOT_VALID_FORMAT)

    def test_activity_can_be_created_with_all_mandatory_fields(self):
        """
        New Activities can be created with all mandatory fields.
        """
        self.login()
        res = self.create('a', get_new_diff(101))
        self.assertEqual(res.status_int, 201)
        json = res.json
        self.assertEqual(json['total'], 1)
        self.assertTrue(json['created'])
        self.assertEqual(len(json['data']), 1)
        self.assertIn('id', json['data'][0])

    def test_activity_can_be_created_without_mandatory_fields(self):
        """
        New Activities can be created even without any mandatory fields.
        """
        self.login()
        res = self.create('a', get_new_diff(102))
        self.assertEqual(res.status_int, 201)
        json = res.json
        self.assertEqual(json['total'], 1)
        self.assertTrue(json['created'])
        self.assertEqual(len(json['data']), 1)
        self.assertIn('id', json['data'][0])

    def test_activity_cannot_be_created_with_invalid_key(self):
        self.login()
        diff = get_new_diff(101)
        diff['activities'][0]['taggroups'][0]['main_tag']['key'] = 'Foo'
        diff['activities'][0]['taggroups'][0]['tags'][0]['key'] = 'Foo'
        res = self.create('a', diff, expect_errors=True)
        self.assertEqual(res.status_int, 400)
        res.mustcontain("Key: Foo or Value: [A] Value A1 is not valid.")

    def test_activity_cannot_be_created_with_invalid_value(self):
        self.login()
        diff = get_new_diff(101)
        diff['activities'][0]['taggroups'][0]['main_tag']['value'] = 'Foo'
        diff['activities'][0]['taggroups'][0]['tags'][0]['value'] = 'Foo'
        res = self.create('a', diff, expect_errors=True)
        self.assertEqual(res.status_int, 400)
        res.mustcontain("Key: [A] Dropdown 1 or Value: Foo is not valid.")

    def test_activity_can_be_created_with_special_chars(self):
        self.login()
        res = self.create('a', get_new_diff(105))
        self.assertEqual(res.status_int, 201)
        json = res.json
        self.assertEqual(json['total'], 1)
        self.assertTrue(json['created'])
        self.assertEqual(len(json['data']), 1)
        self.assertIn('id', json['data'][0])

    def test_activity_cannot_be_created_without_geometry(self):
        """
        When trying to create an Activity without a geometry, a 400
        (Bad Response) code is returned with an error message in the
        body.
        """
        self.login()
        diff = get_new_diff(101)
        del diff['activities'][0]['geometry']
        res = self.create('a', diff, expect_errors=True)
        self.assertEqual(res.status_int, 400)
        res.mustcontain(FEEDBACK_NO_GEOMETRY_PROVIDED)

    def test_new_activities_with_active_involvement_can_be_created(self):
        """
        New Activities can be created with an existing (active) Stakeholder
        attached to it.
        This also creates a new version of the Stakeholder.
        """
        self.login()

        sh_uid = self.create('sh', get_new_diff(201), return_uid=True)
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
            'a', get_new_diff(103, data=inv_data), return_uid=True)

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

    def test_new_activities_with_pending_involvement_can_be_created(self):
        """
        New Activities can be created with a new pending Stakeholder attached
        to it. This results in 2 pending SH versions (1 blank, 1 with the
        Involvement) and 1 A version.
        """
        self.login()

        sh_uid = self.create('sh', get_new_diff(201), return_uid=True)

        inv_data = [{
            'id': sh_uid,
            'version': 1,
            'role': 6
        }]
        a_uid = self.create(
            'a', get_new_diff(103, data=inv_data), return_uid=True)

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

    def test_new_activities_have_status_pending(self):
        """
        Test that new Activities are created with status "pending".
        """
        self.login()
        uid = self.create('a', get_new_diff(101), return_uid=True)
        json = self.read_one('a', uid, 'json')
        self.assertEqual(json['total'], 1)
        status = get_status_from_item_json(json)
        self.assertEqual(STATUS_PENDING, status)
