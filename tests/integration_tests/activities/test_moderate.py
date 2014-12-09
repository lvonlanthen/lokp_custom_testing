import pytest

from ..base import (
    LmkpTestCase,
    get_status_from_item_json,
    get_involvements_from_item_json,
)
from ..diffs import (
    get_new_diff,
    get_edit_diff,
)
from ...base import (
    FEEDBACK_MANDATORY_KEYS_MISSING,
    STATUS_ACTIVE,
    STATUS_DELETED,
    STATUS_EDITED,
    STATUS_INACTIVE,
    STATUS_PENDING,
    STATUS_REJECTED,
)


@pytest.mark.usefixtures('app')
@pytest.mark.integration
@pytest.mark.activities
@pytest.mark.moderation
class ActivityModerateTests(LmkpTestCase):

    def setUp(self):
        self.login()
        super(ActivityModerateTests, self).setUp()

    def test_new_activities_can_be_approved(self):
        """
        New Activities with all mandatory keys can be approved.
        """
        uid = self.create('a', get_new_diff(101), return_uid=True)

        res = self.read_one_history('a', uid, 'json')
        status = get_status_from_item_json(res)
        self.assertEqual(STATUS_PENDING, status)

        self.review('a', uid)

        res = self.read_one_history('a', uid, 'json')
        status = get_status_from_item_json(res)
        self.assertEqual(STATUS_ACTIVE, status)

    def test_new_activities_can_be_rejected(self):
        """
        New Activities with all mandatory keys can be rejected.
        """
        uid = self.create('a', get_new_diff(101), return_uid=True)

        res = self.read_one_history('a', uid, 'json')
        status = get_status_from_item_json(res)
        self.assertEqual(STATUS_PENDING, status)

        self.review('a', uid, decision='reject')

        # Rejected Activities are still displayed in history json.
        res = self.read_one_history('a', uid, 'json')
        self.assertEqual(res['total'], 1)
        status = get_status_from_item_json(res)
        self.assertEqual(STATUS_REJECTED, status)

    def test_new_incomplete_activities_can_be_rejected(self):
        """
        New Activities with missing mandatory keys can be rejected.
        """
        uid = self.create('a', get_new_diff(102), return_uid=True)

        res = self.read_one_history('a', uid, 'json')
        status = get_status_from_item_json(res)
        self.assertEqual(STATUS_PENDING, status)

        self.review('a', uid, decision='reject')

        # Rejected Activities are still displayed in history json.
        res = self.read_one_history('a', uid, 'json')
        self.assertEqual(res['total'], 1)
        status = get_status_from_item_json(res)
        self.assertEqual(STATUS_REJECTED, status)

    def test_new_incomplete_activities_cannot_be_approved(self):
        """
        New Activities with missing mandatory keys can NOT be approved.
        """
        uid = self.create('a', get_new_diff(102), return_uid=True)

        res = self.read_one_history('a', uid, 'json')
        status = get_status_from_item_json(res)
        self.assertEqual(STATUS_PENDING, status)

        res = self.review('a', uid, expect_errors=True)

        self.assertEqual(400, res.status_int)
        res.mustcontain(FEEDBACK_MANDATORY_KEYS_MISSING)

        # The Activity is still there and pending
        res = self.read_one_history('a', uid, 'json')
        self.assertEqual(res['total'], 1)
        status = get_status_from_item_json(res)
        self.assertEqual(STATUS_PENDING, status)

    def test_new_activities_with_existing_stakeholder_can_be_approved(self):
        """
        New Activities with an existing (active) Stakeholder can be approved.
        This will implicitly approve the Stakeholder version 2.
        """
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

        # One pending Activity version should have been created, with the
        # Stakeholder (version 2, active) attached to it.
        res = self.read_one_history('a', a_uid, 'json')
        self.assertEqual(res['total'], 1)
        status = get_status_from_item_json(res)
        self.assertEqual(STATUS_ACTIVE, status)
        inv = get_involvements_from_item_json(res)[0]['data']
        self.assertEqual(inv['id'], sh_uid)
        self.assertEqual(inv['version'], 2)
        self.assertEqual(inv['status_id'], 2)

        # On the Stakeholder side, there should be 2 versions: Version 1 is now
        # inactive, version 2 is active and contains the involvement to the
        # Activity (version 1, active). Note that the newest version is on top!
        res = self.read_one_history('sh', sh_uid, 'json')
        self.assertEqual(res['total'], 2)
        self.assertEqual(res['data'][1]['status_id'], 3)
        self.assertEqual(res['data'][0]['status_id'], 2)
        self.assertTrue('involvements' not in res['data'][1])
        inv = get_involvements_from_item_json(res)[0]['data']
        self.assertEqual(inv['id'], a_uid)
        self.assertEqual(inv['version'], 1)
        self.assertEqual(inv['status_id'], 2)

    def test_new_activities_with_new_stakeholder_cannot_be_approved(self):
        """
        New Activities with a new (pending) Stakeholder cannot be approved
        directly. It is necessary to review a first version of the Stakeholder
        first.
        """
        sh_uid = self.create('sh', get_new_diff(201), return_uid=True)
        inv_data = [{
            'id': sh_uid,
            'version': 1,
            'role': 6
        }]
        a_uid = self.create(
            'a', get_new_diff(103, data=inv_data), return_uid=True)

        res = self.review('a', a_uid)
        self.review_not_possible('a', 1, res)
        res = self.read_one_history('a', a_uid, 'json')
        status = get_status_from_item_json(res)
        self.assertEqual(STATUS_PENDING, status)

    def test_new_stakeholders_with_multiple_activities_can_be_reviewed(self):
        """

        """
        sh_uid = self.create('sh', get_new_diff(201), return_uid=True)
        inv_data1 = [{
            'id': sh_uid,
            'version': 1,
            'role': 6
        }]
        a_uid1 = self.create(
            'a', get_new_diff(103, data=inv_data1), return_uid=True)
        inv_data2 = inv_data1
        inv_data2[0]['version'] = 2
        a_uid2 = self.create(
            'a', get_new_diff(103, data=inv_data2), return_uid=True)

        # Check that everything was created correctly
        res = self.read_one_history('a', a_uid1, 'json')
        self.assertEqual(res['total'], 1)
        self.assertEqual(STATUS_PENDING, get_status_from_item_json(res))
        res = self.read_one_history('a', a_uid2, 'json')
        self.assertEqual(res['total'], 1)
        self.assertEqual(STATUS_PENDING, get_status_from_item_json(res))
        res = self.read_one_history('sh', sh_uid, 'json')
        self.assertEqual(res['total'], 3)
        self.assertEqual(STATUS_PENDING, get_status_from_item_json(res, 0))
        self.assertEqual(STATUS_EDITED, get_status_from_item_json(res, 1))
        self.assertEqual(STATUS_PENDING, get_status_from_item_json(res, 2))

        # A1v1 cannot be reviewed because of SH1
        res = self.review('a', a_uid1)
        self.review_not_possible('a', 1, res)

        # SH1v1 can be reviewed
        self.review('sh', sh_uid, version=1)

        # A1v1 can now be reviewed, will set SH1v2 to ACTIVE (!!)
        self.review('a', a_uid1)
        res = self.read_one_history('a', a_uid1, 'json')
        self.assertEqual(STATUS_ACTIVE, get_status_from_item_json(res))
        res = self.read_one_history('sh', sh_uid, 'json')
        self.assertEqual(res['total'], 3)
        self.assertEqual(STATUS_PENDING, get_status_from_item_json(res, 0))
        self.assertEqual(STATUS_ACTIVE, get_status_from_item_json(res, 1))
        self.assertEqual(STATUS_INACTIVE, get_status_from_item_json(res, 2))

        # A2v1 can be reviewed, will set SH1v2 to inactive, SH1v3 to active.
        self.review('a', a_uid2)
        res = self.read_one_history('a', a_uid2, 'json')
        self.assertEqual(STATUS_ACTIVE, get_status_from_item_json(res))
        res = self.read_one_history('sh', sh_uid, 'json')
        self.assertEqual(res['total'], 3)
        self.assertEqual(STATUS_ACTIVE, get_status_from_item_json(res, 0))
        self.assertEqual(STATUS_INACTIVE, get_status_from_item_json(res, 1))
        self.assertEqual(STATUS_INACTIVE, get_status_from_item_json(res, 2))
        self.assertEqual(len(get_involvements_from_item_json(res, 0)), 2)
        self.assertEqual(len(get_involvements_from_item_json(res, 1)), 1)
        self.assertEqual(len(get_involvements_from_item_json(res, 2)), 0)

    def test_review_add_pending_stakeholder_to_pending_activity(self):
        """

        """
        # Create a first Stakeholder
        sh_uid = self.create('sh', get_new_diff(201), return_uid=True)
        # Create a first Activity
        a_uid = self.create('a', get_new_diff(101), return_uid=True)
        # Edit the Activity and add the Stakeholder as involvement
        inv_data1 = [{
            'id': sh_uid,
            'version': 1,
            'role': 6
        }]
        self.create('a', get_edit_diff(102, a_uid, version=1, data=inv_data1))

        # A1v2 cannot be reviewed because of SH
        res = self.review('a', a_uid, version=2)
        self.review_not_possible('a', 1, res)

        # SH1v1 can be reviewed
        self.review('sh', sh_uid, version=1)

        # A1v2 can now be reviewed, will set SH1v2 active and SH1v1 inactive
        self.review('a', a_uid, version=2)

        res = self.read_one_history('a', a_uid, 'json')
        self.assertEqual(res['total'], 2)
        self.assertEqual(STATUS_ACTIVE, get_status_from_item_json(res, 0))
        self.assertEqual(STATUS_EDITED, get_status_from_item_json(res, 1))
        self.assertEqual(len(get_involvements_from_item_json(res, 0)), 1)
        self.assertEqual(len(get_involvements_from_item_json(res, 1)), 0)
        res = self.read_one_history('sh', sh_uid, 'json')
        self.assertEqual(res['total'], 2)
        self.assertEqual(STATUS_ACTIVE, get_status_from_item_json(res, 0))
        self.assertEqual(STATUS_INACTIVE, get_status_from_item_json(res, 1))
        self.assertEqual(len(get_involvements_from_item_json(res, 0)), 1)
        self.assertEqual(len(get_involvements_from_item_json(res, 1)), 0)

    def test_review_add_pending_stakeholder_to_multiple_pending_activities(
            self):
        """

        """
        # Create a first Stakeholder
        sh_uid = self.create('sh', get_new_diff(201), return_uid=True)
        # Create a first Activity
        a_uid1 = self.create('a', get_new_diff(101), return_uid=True)
        # Edit the Activity and add the Stakeholder as involvement
        inv_data1 = [{
            'id': sh_uid,
            'version': 1,
            'role': 6
        }]
        self.create('a', get_edit_diff(102, a_uid1, version=1, data=inv_data1))
        # Create a second Activity
        a_uid2 = self.create('a', get_new_diff(101), return_uid=True)
        # Edit the Activity and add the Stakeholder as involvement
        inv_data2 = [{
            'id': sh_uid,
            'version': 2,
            'role': 6
        }]
        self.create('a', get_edit_diff(102, a_uid2, version=1, data=inv_data2))

        # A1v2 cannot be reviewed because of SH
        res = self.review('a', a_uid1, version=2)
        self.review_not_possible('a', 1, res)
        # A2v2 cannot be reviewed because of SH
        res = self.review('a', a_uid2, version=2)
        self.review_not_possible('a', 1, res)

        # SH1v1 can be reviewed
        self.review('sh', sh_uid, version=1)

        # A1v2 can now be reviewed
        self.review('a', a_uid1, version=2)

        # A2v2 can also be reviewed
        self.review('a', a_uid2, version=2)

        res = self.read_one_history('a', a_uid1, 'json')
        self.assertEqual(res['total'], 2)
        self.assertEqual(STATUS_ACTIVE, get_status_from_item_json(res, 0))
        self.assertEqual(STATUS_EDITED, get_status_from_item_json(res, 1))
        self.assertEqual(len(get_involvements_from_item_json(res, 0)), 1)
        self.assertEqual(len(get_involvements_from_item_json(res, 1)), 0)
        res = self.read_one_history('a', a_uid2, 'json')
        self.assertEqual(res['total'], 2)
        self.assertEqual(STATUS_ACTIVE, get_status_from_item_json(res, 0))
        self.assertEqual(STATUS_EDITED, get_status_from_item_json(res, 1))
        self.assertEqual(len(get_involvements_from_item_json(res, 0)), 1)
        self.assertEqual(len(get_involvements_from_item_json(res, 1)), 0)
        res = self.read_one_history('sh', sh_uid, 'json')
        self.assertEqual(res['total'], 3)
        self.assertEqual(STATUS_ACTIVE, get_status_from_item_json(res, 0))
        self.assertEqual(STATUS_INACTIVE, get_status_from_item_json(res, 1))
        self.assertEqual(STATUS_INACTIVE, get_status_from_item_json(res, 2))
        self.assertEqual(len(get_involvements_from_item_json(res, 0)), 2)
        self.assertEqual(len(get_involvements_from_item_json(res, 1)), 1)
        self.assertEqual(len(get_involvements_from_item_json(res, 2)), 0)

    def test_review_add_pending_stakeholder_to_multiple_activities(self):
        """

        """
        # Create a first Stakeholder
        sh_uid = self.create('sh', get_new_diff(201), return_uid=True)
        # Create a first Activity
        a_uid1 = self.create('a', get_new_diff(101), return_uid=True)
        # Edit the Activity and add the Stakeholder as involvement
        inv_data1 = [{
            'id': sh_uid,
            'version': 1,
            'role': 6
        }]
        self.create('a', get_edit_diff(102, a_uid1, version=1, data=inv_data1))
        # Create a second Activity, directly with SH 1
        inv_data2 = [{
            'id': sh_uid,
            'version': 2,
            'role': 6
        }]
        a_uid2 = self.create(
            'a', get_new_diff(103, data=inv_data2), return_uid=True)

        # A1v2 cannot be reviewed because of SH
        res = self.review('a', a_uid1, version=2)
        self.review_not_possible('a', 1, res)

        # A2v1 cannot be reviewed because of SH
        res = self.review('a', a_uid2, version=1)
        self.review_not_possible('a', 1, res)

        # SH1v1 can be reviewed
        self.review('sh', sh_uid, version=1)

        # A1v2 can now be reviewed
        self.review('a', a_uid1, version=2)

        # A2v1 can also be reviewed
        self.review('a', a_uid2, version=1)

        res = self.read_one_history('a', a_uid1, 'json')
        self.assertEqual(res['total'], 2)
        self.assertEqual(STATUS_ACTIVE, get_status_from_item_json(res, 0))
        self.assertEqual(STATUS_EDITED, get_status_from_item_json(res, 1))
        self.assertEqual(len(get_involvements_from_item_json(res, 0)), 1)
        self.assertEqual(len(get_involvements_from_item_json(res, 1)), 0)
        res = self.read_one_history('a', a_uid2, 'json')
        self.assertEqual(res['total'], 1)
        self.assertEqual(STATUS_ACTIVE, get_status_from_item_json(res, 0))
        self.assertEqual(len(get_involvements_from_item_json(res, 0)), 1)
        res = self.read_one_history('sh', sh_uid, 'json')
        self.assertEqual(res['total'], 3)
        self.assertEqual(STATUS_ACTIVE, get_status_from_item_json(res, 0))
        self.assertEqual(STATUS_INACTIVE, get_status_from_item_json(res, 1))
        self.assertEqual(STATUS_INACTIVE, get_status_from_item_json(res, 2))
        self.assertEqual(len(get_involvements_from_item_json(res, 0)), 2)
        self.assertEqual(len(get_involvements_from_item_json(res, 1)), 1)
        self.assertEqual(len(get_involvements_from_item_json(res, 2)), 0)

    def test_review_first_pending_activity_remove_pending_stakeholder(self):
        # Create a first Stakeholder
        sh_uid = self.create('sh', get_new_diff(201), return_uid=True)
        # Create a first Activity with the involvement
        inv_data_add = [{
            'id': sh_uid,
            'version': 1,
            'role': 6,
            'op': 'add'
        }]
        a_uid = self.create(
            'a', get_new_diff(103, data=inv_data_add), return_uid=True)
        # Edit the Activity and remove the involvement
        inv_data_delete = [{
            'id': sh_uid,
            'version': 2,
            'role': 6,
            'op': 'delete'
        }]
        self.create(
            'a', get_edit_diff(102, a_uid, version=1, data=inv_data_delete))

        # Activity v2 can be reviewed because it does not contain an
        # involvement anymore.
        self.review('a', a_uid, decision='approve', version=2)

        # On Activity side, there are 2 versions:
        # [0] v2: without involvement, active
        # [1] v1: with involvement, edited
        res = self.read_one_history('a', a_uid, 'json')
        self.assertEqual(res['total'], 2)
        self.assertEqual(STATUS_ACTIVE, get_status_from_item_json(res, 0))
        self.assertEqual(STATUS_EDITED, get_status_from_item_json(res, 1))
        self.assertEqual(len(get_involvements_from_item_json(res, 0)), 0)
        self.assertEqual(len(get_involvements_from_item_json(res, 1)), 1)

        # On Stakeholder side, there are 3 versions:
        # [0] v3: without involvement, [edited].
        # [1] v2: with involvement to v1 of Activity, edited.
        # [2] v1: blank Stakeholder, no involvements, pending.
        res = self.read_one_history('sh', sh_uid, 'json')
        self.assertEqual(res['total'], 3)
        self.assertEqual(STATUS_EDITED, get_status_from_item_json(res, 0))
        self.assertEqual(STATUS_EDITED, get_status_from_item_json(res, 1))
        self.assertEqual(STATUS_PENDING, get_status_from_item_json(res, 2))
        self.assertEqual(len(get_involvements_from_item_json(res, 0)), 0)
        self.assertEqual(len(get_involvements_from_item_json(res, 1)), 1)
        self.assertEqual(len(get_involvements_from_item_json(res, 2)), 0)

    def test_review_deleted_active_activity(self):
        a_uid = self.create('a', get_new_diff(101), return_uid=True)
        self.review('a', a_uid)
        self.create('a', get_edit_diff(110, a_uid))
        self.review('a', a_uid, version=2)

        res = self.read_one_history('a', a_uid, 'json')
        self.assertEqual(res['total'], 2)
        self.assertEqual(STATUS_DELETED, get_status_from_item_json(res, 0))
        self.assertEqual(STATUS_INACTIVE, get_status_from_item_json(res, 1))

    def test_review_deleted_pending_activity(self):
        a_uid = self.create('a', get_new_diff(101), return_uid=True)
        self.create('a', get_edit_diff(110, a_uid))
        self.review('a', a_uid, version=2)

        res = self.read_one_history('a', a_uid, 'json')
        self.assertEqual(res['total'], 2)
        self.assertEqual(STATUS_DELETED, get_status_from_item_json(res, 0))
        self.assertEqual(STATUS_EDITED, get_status_from_item_json(res, 1))

    def test_review_deleted_active_activity_with_involvement(self):
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
        }]
        self.create('a', get_edit_diff(110, a_uid, data=inv_data))
        self.review('a', a_uid, version=2)

        res = self.read_one_history('a', a_uid, 'json')
        self.assertEqual(res['total'], 2)
        self.assertEqual(STATUS_DELETED, get_status_from_item_json(res, 0))
        self.assertEqual(STATUS_INACTIVE, get_status_from_item_json(res, 1))

        res = self.read_one_history('sh', sh_uid, 'json')
        self.assertEqual(res['total'], 3)
        self.assertEqual(STATUS_ACTIVE, get_status_from_item_json(res, 0))
        v3_inv = get_involvements_from_item_json(res, 0)
        self.assertEqual(len(v3_inv), 0)
        self.assertEqual(STATUS_INACTIVE, get_status_from_item_json(res, 1))
        self.assertEqual(STATUS_INACTIVE, get_status_from_item_json(res, 2))

    def test_review_deleted_pending_activity_with_involvement(self):
        sh_uid = self.create('sh', get_new_diff(201), return_uid=True)
        self.review('sh', sh_uid)
        inv_data = [{
            'id': sh_uid,
            'version': 1,
            'role': 6
        }]
        a_uid = self.create(
            'a', get_new_diff(103, data=inv_data), return_uid=True)
        inv_data = [{
            'id': sh_uid,
            'version': 2,
            'role': 6,
            'op': 'delete'
        }]
        self.create('a', get_edit_diff(110, a_uid, data=inv_data))
        self.review('a', a_uid, version=2)

        res = self.read_one_history('a', a_uid, 'json')
        self.assertEqual(res['total'], 2)
        self.assertEqual(STATUS_DELETED, get_status_from_item_json(res, 0))
        self.assertEqual(STATUS_EDITED, get_status_from_item_json(res, 1))

        res = self.read_one_history('sh', sh_uid, 'json')
        self.assertEqual(res['total'], 3)
        self.assertEqual(STATUS_EDITED, get_status_from_item_json(res, 0))
        v3_inv = get_involvements_from_item_json(res, 0)
        self.assertEqual(len(v3_inv), 0)
        self.assertEqual(STATUS_EDITED, get_status_from_item_json(res, 1))
        self.assertEqual(STATUS_ACTIVE, get_status_from_item_json(res, 2))
