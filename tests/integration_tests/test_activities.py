import pytest
import unittest

from .base import *
from .activities import *
from .stakeholders import *


@pytest.mark.usefixtures('app')
@pytest.mark.integration
@pytest.mark.activities
class ActivityCreateTests(unittest.TestCase):
        
    def test_activity_cannot_be_created_without_login(self):
        """
        New Activities cannot be created if the user is not logged in.
        """
        res = createActivity(self, {})
        
        self.assertEqual(res.status_int, 200)
        self.assertIn(b'Please login', res.body)
        
    def test_activity_can_be_created(self):
        """
        New Activities can be created if the user is logged in.
        """
        doLogin(self)
        res = createActivity(self, getActivityDiff())
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
        doLogin(self)
        
        json = getReadManyActivities(self, 'json')
        self.assertEqual(json['data'], [])
        self.assertEqual(json['total'], 0)
        
        createActivity(self, getActivityDiff())
        
        json = getReadManyActivities(self, 'json')
        self.assertEqual(json['total'], 1)
    
    def test_new_activities_with_existing_stakeholder_can_be_created(self):
        """
        New Activities can be created with an existing (active) Stakeholder
        attached to it.
        This also creates a new version of the Stakeholder.
        """
        doLogin(self)
        
        shUid = createStakeholder(self, getNewStakeholderDiff(), returnUid=True)
        reviewStakeholder(self, shUid)
        
        res = getReadOneStakeholder(self, shUid, 'json')
        status = getStatusFromItemJSON(res)
        self.assertEqual('active', status)
        
        invData = {
            'id': shUid,
            'version': 1,
            'role': 6
        }
        aUid = createActivity(self, getActivityDiff(3, data=invData), 
            returnUid=True)
        
        # One pending Activity version should have been created, with the 
        # Stakeholder (version 2, pending) attached to it
        res = getReadOneActivity(self, aUid, 'json')
        self.assertEqual(res['total'], 1)
        status = getStatusFromItemJSON(res)
        self.assertEqual('pending', status)
        inv = getInvolvementsFromItemJSON(res)[0]['data']
        self.assertEqual(inv['id'], shUid)
        self.assertEqual(inv['version'], 2)
        self.assertEqual(inv['status_id'], 1)
    
        # On the Stakeholder side, there should be 2 versions: Version 1 is 
        # still active, version 2 is pending and contains the involvement to the
        # Activity (version 1, pending). Note that the newest version is on top!
        res = getReadOneStakeholder(self, shUid, 'json')
        self.assertEqual(res['total'], 2)
        self.assertEqual(res['data'][1]['status_id'], 2)
        self.assertEqual(res['data'][0]['status_id'], 1)
        self.assertTrue('involvements' not in res['data'][1])
        inv = getInvolvementsFromItemJSON(res)[0]['data']
        self.assertEqual(inv['id'], aUid)
        self.assertEqual(inv['version'], 1)
        self.assertEqual(inv['status_id'], 1)
    
    def test_new_activities_with_new_involvement_can_be_created(self):
        """
        New Activities can be created with a new pending Stakeholder attached to
        it.
        This results in 2 pending SH versions (1 blank, 1 with the Involvement)
        and 1 A version.
        """
        doLogin(self)
        
        shUid = createStakeholder(self, getNewStakeholderDiff(), returnUid=True)
        
        invData = {
            'id': shUid,
            'version': 1,
            'role': 6
        }
        aUid = createActivity(self, getActivityDiff(3, data=invData), 
            returnUid=True)
        
        # One pending Activity version should have been created, with the 
        # Stakeholder (version 2, pending) attached to it
        res = getReadOneActivity(self, aUid, 'json')
        self.assertEqual(res['total'], 1)
        status = getStatusFromItemJSON(res)
        self.assertEqual('pending', status)
        inv = getInvolvementsFromItemJSON(res)[0]['data']
        self.assertEqual(inv['id'], shUid)
        self.assertEqual(inv['version'], 2)
        self.assertEqual(inv['status_id'], 1)
    
        # On the Stakeholder side, there should be 2 versions: Version 1 is now
        # inactive, version 2 is pending and contains the involvement to the
        # Activity (version 1, pending). Note that the newest version is on top!
        res = getReadOneStakeholder(self, shUid, 'json')
        self.assertEqual(res['total'], 2)
        self.assertEqual(res['data'][1]['status_id'], 1)
        self.assertEqual(res['data'][0]['status_id'], 1)
        self.assertTrue('involvements' not in res['data'][1])
        inv = getInvolvementsFromItemJSON(res)[0]['data']
        self.assertEqual(inv['id'], aUid)
        self.assertEqual(inv['version'], 1)
        self.assertEqual(inv['status_id'], 1)


@pytest.mark.usefixtures('app')
@pytest.mark.integration
@pytest.mark.activities
@pytest.mark.moderation
class ActivityModerateTests(unittest.TestCase):

    def test_new_activities_can_be_approved(self):
        """
        New Activities with all mandatory keys can be approved.
        """
        doLogin(self)
        uid = createActivity(self, getActivityDiff(), returnUid=True)
        
        res = getReadOneActivity(self, uid, 'json')
        status = getStatusFromItemJSON(res)
        self.assertEqual('pending', status)
        
        reviewActivity(self, uid)
        
        res = getReadOneActivity(self, uid, 'json')
        status = getStatusFromItemJSON(res)
        self.assertEqual('active', status)
    
    def test_new_activities_can_be_rejected(self):
        """
        New Activities with all mandatory keys can be rejected.
        """
        doLogin(self)
        uid = createActivity(self, getActivityDiff(), returnUid=True)
        
        res = getReadOneActivity(self, uid, 'json')
        status = getStatusFromItemJSON(res)
        self.assertEqual('pending', status)
        
        reviewActivity(self, uid, reviewDecision='reject')
        
        # Rejected Activities are currently not displayed anymore.
        res = getReadOneActivity(self, uid, 'json')
        self.assertEqual(res['total'], 0)
        
    def test_new_incomplete_activities_can_be_rejected(self):
        """
        New Activities with missing mandatory keys can be rejected.
        """
        doLogin(self)
        uid = createActivity(self, getActivityDiff(2), returnUid=True)
        
        res = getReadOneActivity(self, uid, 'json')
        status = getStatusFromItemJSON(res)
        self.assertEqual('pending', status)
        
        reviewActivity(self, uid, reviewDecision='reject')
        
        # Rejected Activities are currently not displayed anymore.
        res = getReadOneActivity(self, uid, 'json')
        self.assertEqual(res['total'], 0)
    
    def test_new_incomplete_activities_cannot_be_approved(self):
        """
        New Activities with missing mandatory keys can NOT be approved.
        """
        doLogin(self)
        uid = createActivity(self, getActivityDiff(2), returnUid=True)
        
        res = getReadOneActivity(self, uid, 'json')
        status = getStatusFromItemJSON(res)
        self.assertEqual('pending', status)
        
        res = reviewActivity(self, uid, expectErrors=True)

        self.assertEqual(400, res.status_int)
        self.assertIn('Not all mandatory keys are provided', res.body)
        
        # The Activity is still there and pending
        res = getReadOneActivity(self, uid, 'json')
        self.assertEqual(res['total'], 1)
        status = getStatusFromItemJSON(res)
        self.assertEqual('pending', status)
    
    def test_new_activities_with_existing_stakeholder_can_be_approved(self):
        """
        New Activities with an existing (active) Stakeholder can be approved.
        This will implicitly approve the Stakeholder version 2.
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
        
        # One pending Activity version should have been created, with the
        # Stakeholder (version 2, active) attached to it.
        res = getReadOneActivity(self, aUid, 'json')
        self.assertEqual(res['total'], 1)
        status = getStatusFromItemJSON(res)
        self.assertEqual('active', status)
        inv = getInvolvementsFromItemJSON(res)[0]['data']
        self.assertEqual(inv['id'], shUid)
        self.assertEqual(inv['version'], 2)
        self.assertEqual(inv['status_id'], 2)
        
        # On the Stakeholder side, there should be 2 versions: Version 1 is now 
        # inactive, version 2 is active and contains the involvement to the
        # Activity (version 1, active). Note that the newest version is on top!
        res = getReadOneStakeholder(self, shUid, 'json')
        self.assertEqual(res['total'], 2)
        self.assertEqual(res['data'][1]['status_id'], 3)
        self.assertEqual(res['data'][0]['status_id'], 2)
        self.assertTrue('involvements' not in res['data'][1])
        inv = getInvolvementsFromItemJSON(res)[0]['data']
        self.assertEqual(inv['id'], aUid)
        self.assertEqual(inv['version'], 1)
        self.assertEqual(inv['status_id'], 2)
    
    def test_new_activities_with_new_stakeholder_cannot_be_approved(self):
        """
        New Activities with a new (pending) Stakeholder cannot be approved 
        directly. It is necessary to review a first version of the Stakeholder 
        first.
        """
        doLogin(self)
        shUid = createStakeholder(self, getNewStakeholderDiff(), returnUid=True)
        invData = {
            'id': shUid,
            'version': 1,
            'role': 6
        }
        aUid = createActivity(self, getActivityDiff(3, data=invData), 
            returnUid=True)
        
        res = reviewActivity(self, aUid, expectErrors=True)
        # If a review cannot be done, the response still returns a valid HTTP
        # status code and redirects to the history page, but flashes an error 
        # message and does not approve the item.
        res = res.follow()
        self.assertEqual(200, res.status_int)
        self.assertIn('At least one of the involved Stakeholders cannot be reviewed', res.body)
        res = getReadOneActivity(self, aUid, 'json')
        status = getStatusFromItemJSON(res)
        self.assertEqual('pending', status)
        
        