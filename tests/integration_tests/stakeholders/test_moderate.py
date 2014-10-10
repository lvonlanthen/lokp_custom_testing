import pytest

from ..diffs import (
    get_edit_diff,
    get_new_diff,
)
from ..base import (
    get_involvements_from_item_json,
    get_status_from_item_json,
    LmkpTestCase,
)
from ...base import(
    STATUS_ACTIVE,
    STATUS_DELETED,
    STATUS_INACTIVE,
)


@pytest.mark.usefixtures('app')
@pytest.mark.integration
@pytest.mark.stakeholders
@pytest.mark.moderation
class StakeholderModerateTests(LmkpTestCase):

    def setUp(self):
        self.login()
        super(StakeholderModerateTests, self).setUp()

    def test_new_stakeholders_can_be_approved(self):
        """
        New Stakeholders with all mandatory keys can be approved.
        """
        uid = self.create('sh', get_new_diff(201), return_uid=True)

        res = self.read_one('sh', uid, 'json')
        status = get_status_from_item_json(res)
        self.assertEqual('pending', status)

        self.review('sh', uid)

        res = self.read_one('sh', uid, 'json')
        status = get_status_from_item_json(res)
        self.assertEqual('active', status)

    def test_new_stakeholders_can_be_rejected(self):
        """
        New Stakeholders with all mandatory keys can be rejected.
        """
        uid = self.create('sh', get_new_diff(201), return_uid=True)

        res = self.read_one('sh', uid, 'json')
        status = get_status_from_item_json(res)
        self.assertEqual('pending', status)

        self.review('sh', uid, decision='reject')

        # Rejected Stakeholders are currently not displayed anymore.
        res = self.read_one('sh', uid, 'json')
        self.assertEqual(res['total'], 0)

    def test_new_incomplete_stakeholders_can_be_rejected(self):
        """
        New Stakeholders with missing mandatory keys can be rejected.
        """
        uid = self.create('sh', get_new_diff(202), return_uid=True)

        res = self.read_one('sh', uid, 'json')
        status = get_status_from_item_json(res)
        self.assertEqual('pending', status)

        self.review('sh', uid, decision='reject')

        # Rejected Stakeholders are currently not displayed anymore.
        res = self.read_one('sh', uid, 'json')
        self.assertEqual(res['total'], 0)

    def test_new_incomplete_stakeholders_cannot_be_approved(self):
        """
        New Stakeholders with missing mandatory keys can NOT be approved.
        """
        uid = self.create('sh', get_new_diff(202), return_uid=True)

        res = self.read_one('sh', uid, 'json')
        status = get_status_from_item_json(res)
        self.assertEqual('pending', status)

        res = self.review('sh', uid, expect_errors=True)

        self.assertEqual(400, res.status_int)
        self.assertIn('Not all mandatory keys are provided', res.body)

        # The Stakeholder is still there and pending
        res = self.read_one('sh', uid, 'json')
        self.assertEqual(res['total'], 1)
        status = get_status_from_item_json(res)
        self.assertEqual('pending', status)

    def test_edited_stakeholders_without_involvements_can_be_approved(self):
        """
        Edited Stakeholders without an involvement can be approved.
        """
        uid = self.create('sh', get_new_diff(201), return_uid=True)
        self.review('sh', uid)

        self.create('sh', get_edit_diff(201, uid))
        self.review('sh', uid, version=2)

        # Version 1 is inactive, version 2 is active
        res = self.read_one('sh', uid, 'json')
        self.assertEqual(res['total'], 2)
        self.assertEqual(res['data'][1]['status_id'], 3)
        self.assertEqual(res['data'][0]['status_id'], 2)

    def test_edited_stakeholders_with_involvements_can_be_approved(self):
        """
        Bugfix: Edited Stakeholders with an involvement could not be approved
        from Stakeholder side, thus blocking the review process.
        """
        shUid = self.create('sh', get_new_diff(201), return_uid=True)
        self.review('sh', shUid)
        inv_data = [{
            'id': shUid,
            'version': 1,
            'role': 6
        }]
        a_uid = self.create(
            'a', get_new_diff(103, data=inv_data), return_uid=True)
        self.review('a', a_uid)

        self.create('sh', get_edit_diff(201, shUid, version=2))
        self.review('sh', shUid, version=3)

        # Version 1 is inactive, version 2 is inactive, version 3 is active
        res = self.read_one('sh', shUid, 'json')
        self.assertEqual(res['total'], 3)
        self.assertEqual(res['data'][2]['status_id'], 3)
        self.assertEqual(res['data'][1]['status_id'], 3)
        self.assertEqual(res['data'][0]['status_id'], 2)

    def test_foo(self):
        sh_uid = self.create('sh', get_new_diff(201), return_uid=True)
        self.review('sh', sh_uid)
        inv_data_1 = [{
            'id': sh_uid,
            'version': 1,
            'role': 6
        }]
        a_uid = self.create(
            'a', get_new_diff(103, data=inv_data_1), return_uid=True)
        self.review('a', a_uid)

        inv_data_2 = [{
            'id': sh_uid,
            'version': 2,
            'role': 6,
            'op': 'delete'
        }]
        self.create('a', get_edit_diff(102, a_uid, version=1, data=inv_data_2))

        # From Stakeholder side, the removal cannot be approved
        res = self.review('sh', sh_uid, version=3)
        self.review_not_possible('sh', 2, res)
        res = self.review('sh', sh_uid, version=3, decision='reject')
        self.review_not_possible('sh', 2, res)

        self.review('a', a_uid, version=2)
        res = self.read_one('a', a_uid, 'json')
        self.assertEqual(res['total'], 2)
        self.assertEqual(STATUS_ACTIVE, get_status_from_item_json(res, 0))
        self.assertEqual(STATUS_INACTIVE, get_status_from_item_json(res, 1))

        res = self.read_one('sh', sh_uid, 'json')
        self.assertEqual(res['total'], 3)
        self.assertEqual(STATUS_ACTIVE, get_status_from_item_json(res, 0))
        self.assertEqual(STATUS_INACTIVE, get_status_from_item_json(res, 1))
        self.assertEqual(STATUS_INACTIVE, get_status_from_item_json(res, 2))

    def test_deleted_stakeholder_with_involvement_can_be_approved(self):
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
            'id': a_uid,
            'version': 1,
            'role': 6,
            'op': 'delete'
        }]
        self.create('sh', get_edit_diff(208, sh_uid, version=2, data=inv_data))

        self.app.post(str('/stakeholders/review'), {
            'identifier': sh_uid,
            'version': 3,
            'review_decision': 'approve'
        })

        res = self.read_one('sh', sh_uid, 'json')
        self.assertEqual(res['total'], 3)
        self.assertEqual(STATUS_DELETED, get_status_from_item_json(res, 0))
        self.assertEqual(STATUS_INACTIVE, get_status_from_item_json(res, 1))
        self.assertEqual(STATUS_INACTIVE, get_status_from_item_json(res, 2))
        v1_inv = get_involvements_from_item_json(res, 2)
        v2_inv = get_involvements_from_item_json(res, 1)
        v3_inv = get_involvements_from_item_json(res, 0)
        self.assertEqual(len(v1_inv), 0)
        self.assertEqual(len(v2_inv), 1)
        self.assertEqual(len(v3_inv), 0)

        res = self.read_one('a', a_uid, 'json')
        self.assertEqual(res['total'], 2)
        self.assertEqual(STATUS_ACTIVE, get_status_from_item_json(res, 0))
        self.assertEqual(STATUS_INACTIVE, get_status_from_item_json(res, 1))
        v1_inv = get_involvements_from_item_json(res, 1)
        v2_inv = get_involvements_from_item_json(res, 0)
        self.assertEqual(len(v1_inv), 1)
        self.assertEqual(len(v2_inv), 0)

    def test_deleted_stakeholder_with_involvement_can_be_rejected(self):
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
            'id': a_uid,
            'version': 1,
            'role': 6,
            'op': 'delete'
        }]
        self.create('sh', get_edit_diff(208, sh_uid, version=2, data=inv_data))

        self.app.post(str('/stakeholders/review'), {
            'identifier': sh_uid,
            'version': 3,
            'review_decision': 'reject'
        })

        res = self.read_one('sh', sh_uid, 'json')
        self.assertEqual(res['total'], 2)
        self.assertEqual(STATUS_ACTIVE, get_status_from_item_json(res, 0))
        self.assertEqual(STATUS_INACTIVE, get_status_from_item_json(res, 1))
        v1_inv = get_involvements_from_item_json(res, 1)
        v2_inv = get_involvements_from_item_json(res, 0)
        self.assertEqual(len(v1_inv), 0)
        self.assertEqual(len(v2_inv), 1)

        res = self.read_one('a', a_uid, 'json')
        self.assertEqual(res['total'], 1)
        self.assertEqual(STATUS_ACTIVE, get_status_from_item_json(res, 0))
        v1_inv = get_involvements_from_item_json(res, 0)
        self.assertEqual(len(v1_inv), 1)
