import pytest

from .diffs import (
    get_edit_diff,
    get_new_diff,
)
from .base import (
    get_status_from_item_json,
    LmkpTestCase,
)
from ..base import (
    TITLE_HISTORY_VIEW,
)


@pytest.mark.usefixtures('app')
@pytest.mark.integration
@pytest.mark.stakeholders
class StakeholderCreateTests(LmkpTestCase):

    def test_stakeholder_cannot_be_created_without_login(self):
        """
        New Stakeholders cannot be created if the user is not logged in.
        """
        res = self.create('sh', {})

        self.assertEqual(res.status_int, 200)
        self.assertIn(b'Please login', res.body)

    def test_stakeholder_can_be_created(self):
        """
        New Stakeholders can be created if the user is logged in.
        """
        self.login()
        res = self.create('sh', get_new_diff('sh'))
        self.assertEqual(res.status_int, 201)
        json = res.json
        self.assertEqual(json['total'], 1)
        self.assertTrue(json['created'])
        self.assertEqual(len(json['data']), 1)
        self.assertIn('id', json['data'][0])

    def test_new_stakeholders_appear_in_read_many_json_service(self):
        """
        Newly created Stakeholders appear in the JSON service "read many".
        """
        self.login()

        json = self.read_many('sh', 'json')
        self.assertEqual(json['data'], [])
        self.assertEqual(json['total'], 0)

        self.create('sh', get_new_diff('sh'))

        json = self.read_many('sh', 'json')
        self.assertEqual(json['total'], 1)


@pytest.mark.usefixtures('app')
@pytest.mark.integration
@pytest.mark.stakeholders
@pytest.mark.moderation
class StakeholderModerateTests(LmkpTestCase):

    def test_new_stakeholders_can_be_approved(self):
        """
        New Stakeholders with all mandatory keys can be approved.
        """
        self.login()
        uid = self.create('sh', get_new_diff('sh'), return_uid=True)

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
        self.login()
        uid = self.create('sh', get_new_diff('sh'), return_uid=True)

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
        self.login()
        uid = self.create('sh', get_new_diff('sh', 2), return_uid=True)

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
        self.login()
        uid = self.create('sh', get_new_diff('sh', 2), return_uid=True)

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
        self.login()
        uid = self.create('sh', get_new_diff('sh'), return_uid=True)
        self.review('sh', uid)

        self.create('sh', get_edit_diff('sh', uid))
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
        self.login()
        shUid = self.create('sh', get_new_diff('sh'), return_uid=True)
        self.review('sh', shUid)
        inv_data = [{
            'id': shUid,
            'version': 1,
            'role': 6
        }]
        a_uid = self.create(
            'a', get_new_diff('a', 3, data=inv_data), return_uid=True)
        self.review('a', a_uid)

        self.create('sh', get_edit_diff('sh', shUid, version=2))
        self.review('sh', shUid, version=3)

        # Version 1 is inactive, version 2 is inactive, version 3 is active
        res = self.read_one('sh', shUid, 'json')
        self.assertEqual(res['total'], 3)
        self.assertEqual(res['data'][2]['status_id'], 3)
        self.assertEqual(res['data'][1]['status_id'], 3)
        self.assertEqual(res['data'][0]['status_id'], 2)


@pytest.mark.usefixtures('app')
@pytest.mark.integration
@pytest.mark.stakeholders
@pytest.mark.moderation
class StakeholderHistoryTests(LmkpTestCase):

    def test_history_view(self):
        """
        Test that a history view is available for newly created Activities.
        """
        self.login()
        uid = self.create('sh', get_new_diff('sh'), return_uid=True)

        res = self.app.get('/stakeholders/history/html/%s' % uid)
        self.assertEqual(res.status_int, 200)
        self.assertIn(TITLE_HISTORY_VIEW, res.body)
