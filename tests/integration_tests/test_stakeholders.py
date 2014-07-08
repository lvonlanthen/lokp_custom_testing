import pytest
from unittest import TestCase

from .activities import *
from .base import *
from .stakeholders import *

@pytest.mark.usefixtures('app')
@pytest.mark.integration
@pytest.mark.stakeholders
class StakeholderCreateTests(TestCase):
        
    def test_stakeholder_cannot_be_created_without_login(self):
        """
        New Stakeholders cannot be created if the user is not logged in.
        """
        res = createStakeholder(self, {})
        
        self.assertEqual(res.status_int, 200)
        self.assertIn(b'Please login', res.body)
        
    def test_stakeholder_can_be_created(self):
        """
        New Stakeholders can be created if the user is logged in.
        """
        doLogin(self)
        res = createStakeholder(self, getNewStakeholderDiff())
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
        doLogin(self)
        
        json = getReadManyStakeholders(self, 'json')
        self.assertEqual(json['data'], [])
        self.assertEqual(json['total'], 0)
        
        createStakeholder(self, getNewStakeholderDiff())
        
        json = getReadManyStakeholders(self, 'json')
        self.assertEqual(json['total'], 1)
    
    
@pytest.mark.usefixtures('app')
@pytest.mark.integration
@pytest.mark.stakeholders
@pytest.mark.moderation
class StakeholderModerateTests(TestCase):

    def test_new_stakeholders_can_be_approved(self):
        """
        New Stakeholders with all mandatory keys can be approved.
        """
        doLogin(self)
        uid = createStakeholder(self, getNewStakeholderDiff(), returnUid=True)
        
        res = getReadOneStakeholder(self, uid, 'json')
        status = getStatusFromItemJSON(res)
        self.assertEqual('pending', status)
        
        reviewStakeholder(self, uid)
        
        res = getReadOneStakeholder(self, uid, 'json')
        status = getStatusFromItemJSON(res)
        self.assertEqual('active', status)
    
    def test_new_stakeholders_can_be_rejected(self):
        """
        New Stakeholders with all mandatory keys can be rejected.
        """
        doLogin(self)
        uid = createStakeholder(self, getNewStakeholderDiff(), returnUid=True)
        
        res = getReadOneStakeholder(self, uid, 'json')
        status = getStatusFromItemJSON(res)
        self.assertEqual('pending', status)
        
        reviewStakeholder(self, uid, reviewDecision='reject')
        
        # Rejected Stakeholders are currently not displayed anymore.
        res = getReadOneStakeholder(self, uid, 'json')
        self.assertEqual(res['total'], 0)
        
    def test_new_incomplete_stakeholders_can_be_rejected(self):
        """
        New Stakeholders with missing mandatory keys can be rejected.
        """
        doLogin(self)
        uid = createStakeholder(self, getNewStakeholderDiff(2), returnUid=True)
        
        res = getReadOneStakeholder(self, uid, 'json')
        status = getStatusFromItemJSON(res)
        self.assertEqual('pending', status)
        
        reviewStakeholder(self, uid, reviewDecision='reject')
        
        # Rejected Stakeholders are currently not displayed anymore.
        res = getReadOneStakeholder(self, uid, 'json')
        self.assertEqual(res['total'], 0)
    
    def test_new_incomplete_stakeholders_cannot_be_approved(self):
        """
        New Stakeholders with missing mandatory keys can NOT be approved.
        """
        doLogin(self)
        uid = createStakeholder(self, getNewStakeholderDiff(2), returnUid=True)
        
        res = getReadOneStakeholder(self, uid, 'json')
        status = getStatusFromItemJSON(res)
        self.assertEqual('pending', status)
        
        res = reviewStakeholder(self, uid, expectErrors=True)

        self.assertEqual(400, res.status_int)
        self.assertIn('Not all mandatory keys are provided', res.body)
        
        # The Stakeholder is still there and pending
        res = getReadOneStakeholder(self, uid, 'json')
        self.assertEqual(res['total'], 1)
        status = getStatusFromItemJSON(res)
        self.assertEqual('pending', status)
    
    def test_edited_stakeholders_without_involvements_can_be_approved(self):
        """
        Edited Stakeholders without an involvement can be approved.
        """
        doLogin(self)
        uid = createStakeholder(self, getNewStakeholderDiff(), returnUid=True)
        reviewStakeholder(self, uid)

        createStakeholder(self, getEditStakeholderDiff(uid))
        reviewStakeholder(self, uid, version=2)
        
        # Version 1 is inactive, version 2 is active
        res = getReadOneStakeholder(self, uid, 'json')
        self.assertEqual(res['total'], 2)
        self.assertEqual(res['data'][1]['status_id'], 3)
        self.assertEqual(res['data'][0]['status_id'], 2)
        
    def test_edited_stakeholders_with_involvements_can_be_approved(self):
        """
        Bugfix: Edited Stakeholders with an involvement could not be approved
        from Stakeholder side, thus blocking the review process.
        """
        doLogin(self)
        shUid = createStakeholder(self, getNewStakeholderDiff(), returnUid=True)
        reviewStakeholder(self, shUid)
        invData = {
            'id': shUid,
            'version': 1,
            'role': 6
        }
        aUid = createActivity(self, getActivityDiff(3, data=invData),
            returnUid=True)
        reviewActivity(self, aUid)

        createStakeholder(self, getEditStakeholderDiff(shUid, version=2))
        reviewStakeholder(self, shUid, version=3)

        # Version 1 is inactive, version 2 is inactive, version 3 is active
        res = getReadOneStakeholder(self, shUid, 'json')
        self.assertEqual(res['total'], 3)
        self.assertEqual(res['data'][2]['status_id'], 3)
        self.assertEqual(res['data'][1]['status_id'], 3)
        self.assertEqual(res['data'][0]['status_id'], 2)
    