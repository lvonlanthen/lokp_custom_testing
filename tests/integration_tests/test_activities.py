# Some of the more complicated test setups and procedures are explained 
# schematically in files available in a Google Drive folder:
# https://drive.google.com/folderview?id=0B49ePOKDgdN-WFZXVGlCX2ZZR2M&usp=sharing

import pytest
from unittest import TestCase

from .base import *
from .activities import *
from .stakeholders import *
from ..base import *


@pytest.mark.usefixtures('app')
@pytest.mark.integration
@pytest.mark.activities
class ActivityCreateTests(TestCase):
        
    def test_activity_cannot_be_created_without_login(self):
        """
        New Activities cannot be created if the user is not logged in.
        """
        res = createActivity(self, {})
        
        self.assertEqual(res.status_int, 200)
        res.mustcontain(FEEDBACK_LOGIN_NEEDED)
        
    def test_activity_can_be_created(self):
        """
        New Activities can be created if the user is logged in.
        """
        doLogin(self)
        res = createActivity(self, getNewActivityDiff())
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
        
        createActivity(self, getNewActivityDiff())
        
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
        
        invData = [{
            'id': shUid,
            'version': 1,
            'role': 6
        }]
        aUid = createActivity(self, getNewActivityDiff(3, data=invData), 
            returnUid=True)
        
        # One pending Activity version should have been created, with the 
        # Stakeholder (version 2, pending) attached to it
        res = getReadOneActivity(self, aUid, 'json')
        self.assertEqual(res['total'], 1)
        status = getStatusFromItemJSON(res)
        self.assertEqual(STATUS_PENDING, status)
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
        
        invData = [{
            'id': shUid,
            'version': 1,
            'role': 6
        }]
        aUid = createActivity(self, getNewActivityDiff(3, data=invData), 
            returnUid=True)
        
        # One pending Activity version should have been created, with the 
        # Stakeholder (version 2, pending) attached to it
        res = getReadOneActivity(self, aUid, 'json')
        self.assertEqual(res['total'], 1)
        status = getStatusFromItemJSON(res)
        self.assertEqual(STATUS_PENDING, status)
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
class ActivityModerateTests(TestCase):

    def test_new_activities_can_be_approved(self):
        """
        New Activities with all mandatory keys can be approved.
        """
        doLogin(self)
        uid = createActivity(self, getNewActivityDiff(), returnUid=True)
        
        res = getReadOneActivity(self, uid, 'json')
        status = getStatusFromItemJSON(res)
        self.assertEqual(STATUS_PENDING, status)
        
        reviewActivity(self, uid)
        
        res = getReadOneActivity(self, uid, 'json')
        status = getStatusFromItemJSON(res)
        self.assertEqual(STATUS_ACTIVE, status)
    
    def test_new_activities_can_be_rejected(self):
        """
        New Activities with all mandatory keys can be rejected.
        """
        doLogin(self)
        uid = createActivity(self, getNewActivityDiff(), returnUid=True)
        
        res = getReadOneActivity(self, uid, 'json')
        status = getStatusFromItemJSON(res)
        self.assertEqual(STATUS_PENDING, status)
        
        reviewActivity(self, uid, reviewDecision='reject')
        
        # Rejected Activities are currently not displayed anymore.
        res = getReadOneActivity(self, uid, 'json')
        self.assertEqual(res['total'], 0)
        
    def test_new_incomplete_activities_can_be_rejected(self):
        """
        New Activities with missing mandatory keys can be rejected.
        """
        doLogin(self)
        uid = createActivity(self, getNewActivityDiff(2), returnUid=True)
        
        res = getReadOneActivity(self, uid, 'json')
        status = getStatusFromItemJSON(res)
        self.assertEqual(STATUS_PENDING, status)
        
        reviewActivity(self, uid, reviewDecision='reject')
        
        # Rejected Activities are currently not displayed anymore.
        res = getReadOneActivity(self, uid, 'json')
        self.assertEqual(res['total'], 0)
    
    def test_new_incomplete_activities_cannot_be_approved(self):
        """
        New Activities with missing mandatory keys can NOT be approved.
        """
        doLogin(self)
        uid = createActivity(self, getNewActivityDiff(2), returnUid=True)
        
        res = getReadOneActivity(self, uid, 'json')
        status = getStatusFromItemJSON(res)
        self.assertEqual(STATUS_PENDING, status)
        
        res = reviewActivity(self, uid, expectErrors=True)

        self.assertEqual(400, res.status_int)
        res.mustcontain(FEEDBACK_MANDATORY_KEYS_MISSING)
        
        # The Activity is still there and pending
        res = getReadOneActivity(self, uid, 'json')
        self.assertEqual(res['total'], 1)
        status = getStatusFromItemJSON(res)
        self.assertEqual(STATUS_PENDING, status)
    
    def test_new_activities_with_existing_stakeholder_can_be_approved(self):
        """
        New Activities with an existing (active) Stakeholder can be approved.
        This will implicitly approve the Stakeholder version 2.
        """
        doLogin(self)
        shUid = createStakeholder(self, getNewStakeholderDiff(), returnUid=True)
        reviewStakeholder(self, shUid)
        invData = [{
            'id': shUid,
            'version': 1,
            'role': 6
        }]
        aUid = createActivity(self, getNewActivityDiff(3, data=invData), 
            returnUid=True)
        
        reviewActivity(self, aUid)
        
        # One pending Activity version should have been created, with the
        # Stakeholder (version 2, active) attached to it.
        res = getReadOneActivity(self, aUid, 'json')
        self.assertEqual(res['total'], 1)
        status = getStatusFromItemJSON(res)
        self.assertEqual(STATUS_ACTIVE, status)
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
        invData = [{
            'id': shUid,
            'version': 1,
            'role': 6
        }]
        aUid = createActivity(self, getNewActivityDiff(3, data=invData), 
            returnUid=True)
        
        res = reviewActivity(self, aUid)
        checkReviewActivityNotPossibleBcStakeholder(self, res)
        res = getReadOneActivity(self, aUid, 'json')
        status = getStatusFromItemJSON(res)
        self.assertEqual(STATUS_PENDING, status)

    def test_new_stakeholders_with_multiple_activities_can_be_reviewed(self):
        """
        
        """
        doLogin(self)
        shUid = createStakeholder(self, getNewStakeholderDiff(), returnUid=True)
        invData1 = [{
            'id': shUid,
            'version': 1,
            'role': 6
        }]
        aUid1 = createActivity(self, getNewActivityDiff(3, data=invData1), 
            returnUid=True)
        invData2 = invData1
        invData2[0]['version'] = 2
        aUid2 = createActivity(self, getNewActivityDiff(3, data=invData2),
            returnUid=True)
        
        # Check that everything was created correctly
        res = getReadOneActivity(self, aUid1, 'json')
        self.assertEqual(res['total'], 1)
        self.assertEqual(STATUS_PENDING, getStatusFromItemJSON(res))
        res = getReadOneActivity(self, aUid2, 'json')
        self.assertEqual(res['total'], 1)
        self.assertEqual(STATUS_PENDING, getStatusFromItemJSON(res))
        res = getReadOneStakeholder(self, shUid, 'json')
        self.assertEqual(res['total'], 3)
        self.assertEqual(STATUS_PENDING, getStatusFromItemJSON(res, 0))
        self.assertEqual(STATUS_EDITED, getStatusFromItemJSON(res, 1))
        self.assertEqual(STATUS_PENDING, getStatusFromItemJSON(res, 2))
        
        # A1v1 cannot be reviewed because of SH1
        res = reviewActivity(self, aUid1)
        checkReviewActivityNotPossibleBcStakeholder(self, res)
        
        # SH1v1 can be reviewed
        reviewStakeholder(self, shUid, version=1)
        
        # A1v1 can now be reviewed, will set SH1v2 to ACTIVE (!!)
        reviewActivity(self, aUid1)
        res = getReadOneActivity(self, aUid1, 'json')
        self.assertEqual(STATUS_ACTIVE, getStatusFromItemJSON(res))
        res = getReadOneStakeholder(self, shUid, 'json')
        self.assertEqual(res['total'], 3)
        self.assertEqual(STATUS_PENDING, getStatusFromItemJSON(res, 0))
        self.assertEqual(STATUS_ACTIVE, getStatusFromItemJSON(res, 1))
        self.assertEqual(STATUS_INACTIVE, getStatusFromItemJSON(res, 2))
        
        # A2v1 can be reviewed, will set SH1v2 to inactive, SH1v3 to active.
        reviewActivity(self, aUid2)
        res = getReadOneActivity(self, aUid2, 'json')
        self.assertEqual(STATUS_ACTIVE, getStatusFromItemJSON(res))
        res = getReadOneStakeholder(self, shUid, 'json')
        self.assertEqual(res['total'], 3)
        self.assertEqual(STATUS_ACTIVE, getStatusFromItemJSON(res, 0))
        self.assertEqual(STATUS_INACTIVE, getStatusFromItemJSON(res, 1))
        self.assertEqual(STATUS_INACTIVE, getStatusFromItemJSON(res, 2))
        self.assertEqual(len(getInvolvementsFromItemJSON(res, 0)), 2)
        self.assertEqual(len(getInvolvementsFromItemJSON(res, 1)), 1)
        self.assertEqual(len(getInvolvementsFromItemJSON(res, 2)), 0)

    def test_add_pending_stakeholder_to_pending_activity(self):
        """
        
        """
        doLogin(self)
        # Create a first Stakeholder
        shUid = createStakeholder(self, getNewStakeholderDiff(), returnUid=True)
        # Create a first Activity
        aUid = createActivity(self, getNewActivityDiff(1), returnUid=True)
        # Edit the Activity and add the Stakeholder as involvement
        invData1 = [{
            'id': shUid,
            'version': 1,
            'role': 6
        }]
        createActivity(self, getEditActivityDiff(aUid, version=1, type=2, 
            data=invData1))
        
        # Check that everything was added correctly
        res = getReadOneActivity(self, aUid, 'json')
        self.assertEqual(res['total'], 2)
        self.assertEqual(STATUS_PENDING, getStatusFromItemJSON(res, 0))
        self.assertEqual(STATUS_EDITED, getStatusFromItemJSON(res, 1))
        self.assertEqual(len(getInvolvementsFromItemJSON(res, 0)), 1)
        self.assertEqual(len(getInvolvementsFromItemJSON(res, 1)), 0)
        res = getReadOneStakeholder(self, shUid, 'json')
        self.assertEqual(res['total'], 2)
        self.assertEqual(STATUS_PENDING, getStatusFromItemJSON(res, 0))
        self.assertEqual(STATUS_PENDING, getStatusFromItemJSON(res, 1))
        self.assertEqual(len(getInvolvementsFromItemJSON(res, 0)), 1)
        self.assertEqual(len(getInvolvementsFromItemJSON(res, 1)), 0)
    
    def test_review_add_pending_stakeholder_to_pending_activity(self):
        """
        
        """
        doLogin(self)
        # Create a first Stakeholder
        shUid = createStakeholder(self, getNewStakeholderDiff(), returnUid=True)
        # Create a first Activity
        aUid = createActivity(self, getNewActivityDiff(1), returnUid=True)
        # Edit the Activity and add the Stakeholder as involvement
        invData1 = [{
            'id': shUid,
            'version': 1,
            'role': 6
        }]
        createActivity(self, getEditActivityDiff(aUid, version=1, type=2, 
            data=invData1))
        
        # A1v2 cannot be reviewed because of SH
        res = reviewActivity(self, aUid, version=2)
        checkReviewActivityNotPossibleBcStakeholder(self, res)
        
        # SH1v1 can be reviewed
        reviewStakeholder(self, shUid, version=1)
        
        # A1v2 can now be reviewed, will set SH1v2 active and SH1v1 inactive
        reviewActivity(self, aUid, version=2)
        
        res = getReadOneActivity(self, aUid, 'json')
        self.assertEqual(res['total'], 2)
        self.assertEqual(STATUS_ACTIVE, getStatusFromItemJSON(res, 0))
        self.assertEqual(STATUS_EDITED, getStatusFromItemJSON(res, 1))
        self.assertEqual(len(getInvolvementsFromItemJSON(res, 0)), 1)
        self.assertEqual(len(getInvolvementsFromItemJSON(res, 1)), 0)
        res = getReadOneStakeholder(self, shUid, 'json')
        self.assertEqual(res['total'], 2)
        self.assertEqual(STATUS_ACTIVE, getStatusFromItemJSON(res, 0))
        self.assertEqual(STATUS_INACTIVE, getStatusFromItemJSON(res, 1))
        self.assertEqual(len(getInvolvementsFromItemJSON(res, 0)), 1)
        self.assertEqual(len(getInvolvementsFromItemJSON(res, 1)), 0)
        
    def test_add_pending_stakeholder_to_multiple_pending_activities(self):
        """
        
        """
        doLogin(self)
        # Create a first Stakeholder
        shUid = createStakeholder(self, getNewStakeholderDiff(), returnUid=True)
        # Create a first Activity
        aUid1 = createActivity(self, getNewActivityDiff(1), returnUid=True)
        # Edit the Activity and add the Stakeholder as involvement
        invData1 = [{
            'id': shUid,
            'version': 1,
            'role': 6
        }]
        createActivity(self, getEditActivityDiff(aUid1, version=1, type=2, 
            data=invData1))
        # Create a second Activity
        aUid2 = createActivity(self, getNewActivityDiff(1), returnUid=True)
        # Edit the Activity and add the Stakeholder as involvement
        invData2 = [{
            'id': shUid,
            'version': 2,
            'role': 6
        }]
        createActivity(self, getEditActivityDiff(aUid2, version=1, type=2, 
            data=invData2))
        
        # Check that everything was added correctly
        res = getReadOneActivity(self, aUid1, 'json')
        self.assertEqual(res['total'], 2)
        self.assertEqual(STATUS_PENDING, getStatusFromItemJSON(res, 0))
        self.assertEqual(STATUS_EDITED, getStatusFromItemJSON(res, 1))
        self.assertEqual(len(getInvolvementsFromItemJSON(res, 0)), 1)
        self.assertEqual(len(getInvolvementsFromItemJSON(res, 1)), 0)
        res = getReadOneActivity(self, aUid2, 'json')
        self.assertEqual(res['total'], 2)
        self.assertEqual(STATUS_PENDING, getStatusFromItemJSON(res, 0))
        self.assertEqual(STATUS_EDITED, getStatusFromItemJSON(res, 1))
        self.assertEqual(len(getInvolvementsFromItemJSON(res, 0)), 1)
        self.assertEqual(len(getInvolvementsFromItemJSON(res, 1)), 0)
        res = getReadOneStakeholder(self, shUid, 'json')
        self.assertEqual(res['total'], 3)
        self.assertEqual(STATUS_PENDING, getStatusFromItemJSON(res, 0))
        self.assertEqual(STATUS_EDITED, getStatusFromItemJSON(res, 1))
        self.assertEqual(STATUS_PENDING, getStatusFromItemJSON(res, 2))
        self.assertEqual(len(getInvolvementsFromItemJSON(res, 0)), 2)
        self.assertEqual(len(getInvolvementsFromItemJSON(res, 1)), 1)
        self.assertEqual(len(getInvolvementsFromItemJSON(res, 2)), 0)

    def test_review_add_pending_stakeholder_to_multiple_pending_activities(self):
        """
        
        """
        doLogin(self)
        # Create a first Stakeholder
        shUid = createStakeholder(self, getNewStakeholderDiff(), returnUid=True)
        # Create a first Activity
        aUid1 = createActivity(self, getNewActivityDiff(1), returnUid=True)
        # Edit the Activity and add the Stakeholder as involvement
        invData1 = [{
            'id': shUid,
            'version': 1,
            'role': 6
        }]
        createActivity(self, getEditActivityDiff(aUid1, version=1, type=2, 
            data=invData1))
        # Create a second Activity
        aUid2 = createActivity(self, getNewActivityDiff(1), returnUid=True)
        # Edit the Activity and add the Stakeholder as involvement
        invData2 = [{
            'id': shUid,
            'version': 2,
            'role': 6
        }]
        createActivity(self, getEditActivityDiff(aUid2, version=1, type=2, 
            data=invData2))
        
        # A1v2 cannot be reviewed because of SH
        res = reviewActivity(self, aUid1, version=2)
        checkReviewActivityNotPossibleBcStakeholder(self, res)
        # A2v2 cannot be reviewed because of SH
        res = reviewActivity(self, aUid2, version=2)
        checkReviewActivityNotPossibleBcStakeholder(self, res)
        
        # SH1v1 can be reviewed
        reviewStakeholder(self, shUid, version=1)
        
        # A1v2 can now be reviewed
        reviewActivity(self, aUid1, version=2)
        
        # A2v2 can also be reviewed
        reviewActivity(self, aUid2, version=2)
        
        res = getReadOneActivity(self, aUid1, 'json')
        self.assertEqual(res['total'], 2)
        self.assertEqual(STATUS_ACTIVE, getStatusFromItemJSON(res, 0))
        self.assertEqual(STATUS_EDITED, getStatusFromItemJSON(res, 1))
        self.assertEqual(len(getInvolvementsFromItemJSON(res, 0)), 1)
        self.assertEqual(len(getInvolvementsFromItemJSON(res, 1)), 0)
        res = getReadOneActivity(self, aUid2, 'json')
        self.assertEqual(res['total'], 2)
        self.assertEqual(STATUS_ACTIVE, getStatusFromItemJSON(res, 0))
        self.assertEqual(STATUS_EDITED, getStatusFromItemJSON(res, 1))
        self.assertEqual(len(getInvolvementsFromItemJSON(res, 0)), 1)
        self.assertEqual(len(getInvolvementsFromItemJSON(res, 1)), 0)
        res = getReadOneStakeholder(self, shUid, 'json')
        self.assertEqual(res['total'], 3)
        self.assertEqual(STATUS_ACTIVE, getStatusFromItemJSON(res, 0))
        self.assertEqual(STATUS_INACTIVE, getStatusFromItemJSON(res, 1))
        self.assertEqual(STATUS_INACTIVE, getStatusFromItemJSON(res, 2))
        self.assertEqual(len(getInvolvementsFromItemJSON(res, 0)), 2)
        self.assertEqual(len(getInvolvementsFromItemJSON(res, 1)), 1)
        self.assertEqual(len(getInvolvementsFromItemJSON(res, 2)), 0)

    def test_add_pending_stakeholder_to_multiple_activities(self):
        """
        
        """
        doLogin(self)
        # Create a first Stakeholder
        shUid = createStakeholder(self, getNewStakeholderDiff(), returnUid=True)
        # Create a first Activity
        aUid1 = createActivity(self, getNewActivityDiff(1), returnUid=True)
        # Edit the Activity and add the Stakeholder as involvement
        invData1 = [{
            'id': shUid,
            'version': 1,
            'role': 6
        }]
        createActivity(self, getEditActivityDiff(aUid1, version=1, type=2, 
            data=invData1))
        # Create a second Activity, directly with SH 1
        invData2 = [{
            'id': shUid,
            'version': 2,
            'role': 6
        }]
        aUid2 = createActivity(self, getNewActivityDiff(3, data=invData2), 
            returnUid=True)
        
        # Check that everything was added correctly
        res = getReadOneActivity(self, aUid1, 'json')
        self.assertEqual(res['total'], 2)
        self.assertEqual(STATUS_PENDING, getStatusFromItemJSON(res, 0))
        self.assertEqual(STATUS_EDITED, getStatusFromItemJSON(res, 1))
        self.assertEqual(len(getInvolvementsFromItemJSON(res, 0)), 1)
        self.assertEqual(len(getInvolvementsFromItemJSON(res, 1)), 0)
        res = getReadOneActivity(self, aUid2, 'json')
        self.assertEqual(res['total'], 1)
        self.assertEqual(STATUS_PENDING, getStatusFromItemJSON(res, 0))
        self.assertEqual(len(getInvolvementsFromItemJSON(res, 0)), 1)
        res = getReadOneStakeholder(self, shUid, 'json')
        self.assertEqual(res['total'], 3)
        self.assertEqual(STATUS_PENDING, getStatusFromItemJSON(res, 0))
        self.assertEqual(STATUS_EDITED, getStatusFromItemJSON(res, 1))
        self.assertEqual(STATUS_PENDING, getStatusFromItemJSON(res, 2))
        self.assertEqual(len(getInvolvementsFromItemJSON(res, 0)), 2)
        self.assertEqual(len(getInvolvementsFromItemJSON(res, 1)), 1)
        self.assertEqual(len(getInvolvementsFromItemJSON(res, 2)), 0)

    def test_review_add_pending_stakeholder_to_multiple_activities(self):
        """
        
        """
        doLogin(self)
        # Create a first Stakeholder
        shUid = createStakeholder(self, getNewStakeholderDiff(), returnUid=True)
        # Create a first Activity
        aUid1 = createActivity(self, getNewActivityDiff(1), returnUid=True)
        # Edit the Activity and add the Stakeholder as involvement
        invData1 = [{
            'id': shUid,
            'version': 1,
            'role': 6
        }]
        createActivity(self, getEditActivityDiff(aUid1, version=1, type=2, 
            data=invData1))
        # Create a second Activity, directly with SH 1
        invData2 = [{
            'id': shUid,
            'version': 2,
            'role': 6
        }]
        aUid2 = createActivity(self, getNewActivityDiff(3, data=invData2), 
            returnUid=True)
        
        # A1v2 cannot be reviewed because of SH
        res = reviewActivity(self, aUid1, version=2)
        checkReviewActivityNotPossibleBcStakeholder(self, res)
        
        # A2v1 cannot be reviewed because of SH
        res = reviewActivity(self, aUid2, version=1)
        checkReviewActivityNotPossibleBcStakeholder(self, res)
        
        # SH1v1 can be reviewed
        reviewStakeholder(self, shUid, version=1)
        
        # A1v2 can now be reviewed
        reviewActivity(self, aUid1, version=2)
        
        # A2v1 can also be reviewed
        reviewActivity(self, aUid2, version=1)
        
        res = getReadOneActivity(self, aUid1, 'json')
        self.assertEqual(res['total'], 2)
        self.assertEqual(STATUS_ACTIVE, getStatusFromItemJSON(res, 0))
        self.assertEqual(STATUS_EDITED, getStatusFromItemJSON(res, 1))
        self.assertEqual(len(getInvolvementsFromItemJSON(res, 0)), 1)
        self.assertEqual(len(getInvolvementsFromItemJSON(res, 1)), 0)
        res = getReadOneActivity(self, aUid2, 'json')
        self.assertEqual(res['total'], 1)
        self.assertEqual(STATUS_ACTIVE, getStatusFromItemJSON(res, 0))
        self.assertEqual(len(getInvolvementsFromItemJSON(res, 0)), 1)
        res = getReadOneStakeholder(self, shUid, 'json')
        self.assertEqual(res['total'], 3)
        self.assertEqual(STATUS_ACTIVE, getStatusFromItemJSON(res, 0))
        self.assertEqual(STATUS_INACTIVE, getStatusFromItemJSON(res, 1))
        self.assertEqual(STATUS_INACTIVE, getStatusFromItemJSON(res, 2))
        self.assertEqual(len(getInvolvementsFromItemJSON(res, 0)), 2)
        self.assertEqual(len(getInvolvementsFromItemJSON(res, 1)), 1)
        self.assertEqual(len(getInvolvementsFromItemJSON(res, 2)), 0)

    def test_setup_01(self):
        """
        For the rather complicated setup of this test, have a look at 
        "Setup Test 01" in the drive folder.
        """
        doLogin(self)
        # Create a first Stakeholder
        shUid1 = createStakeholder(self, getNewStakeholderDiff(), returnUid=True)
        # Create a second Stakeholder
        shUid2 = createStakeholder(self, getNewStakeholderDiff(), returnUid=True)
        # Create a first Activity
        aUid1 = createActivity(self, getNewActivityDiff(1), returnUid=True)
        # Edit the Activity and add the first Stakeholder as involvement
        invData1 = [{
            'id': shUid1,
            'version': 1,
            'role': 6
        }]
        createActivity(self, getEditActivityDiff(aUid1, version=1, type=2, 
            data=invData1))
        # Create a second Activity and add the second Stakeholder as involvement
        invData2 = [{
            'id': shUid2,
            'version': 1,
            'role': 6
        }]
        aUid2 = createActivity(self, getNewActivityDiff(3, data=invData2), 
            returnUid=True)
        # Create a third Activity and add both Stakeholders as involvement
        invData3 = [{
            'id': shUid1,
            'version': 2,
            'role': 6
        }, {
            'id': shUid2,
            'version': 2,
            'role': 6
        }]
        aUid3 = createActivity(self, getNewActivityDiff(3, data=invData3), 
            returnUid=True)
        
        # Check that everything was added correctly
        res = getReadOneActivity(self, aUid1, 'json')
        self.assertEqual(res['total'], 2)
        self.assertEqual(STATUS_PENDING, getStatusFromItemJSON(res, 0))
        self.assertEqual(STATUS_EDITED, getStatusFromItemJSON(res, 1))
        self.assertEqual(len(getInvolvementsFromItemJSON(res, 0)), 1)
        self.assertEqual(len(getInvolvementsFromItemJSON(res, 1)), 0)
        res = getReadOneActivity(self, aUid2, 'json')
        self.assertEqual(res['total'], 1)
        self.assertEqual(STATUS_PENDING, getStatusFromItemJSON(res, 0))
        self.assertEqual(len(getInvolvementsFromItemJSON(res, 0)), 1)
        res = getReadOneActivity(self, aUid3, 'json')
        self.assertEqual(res['total'], 1)
        self.assertEqual(STATUS_PENDING, getStatusFromItemJSON(res, 0))
        self.assertEqual(len(getInvolvementsFromItemJSON(res, 0)), 2)
        res = getReadOneStakeholder(self, shUid1, 'json')
        self.assertEqual(res['total'], 3)
        self.assertEqual(STATUS_PENDING, getStatusFromItemJSON(res, 0))
        self.assertEqual(STATUS_EDITED, getStatusFromItemJSON(res, 1))
        self.assertEqual(STATUS_PENDING, getStatusFromItemJSON(res, 2))
        self.assertEqual(len(getInvolvementsFromItemJSON(res, 0)), 2)
        self.assertEqual(len(getInvolvementsFromItemJSON(res, 1)), 1)
        self.assertEqual(len(getInvolvementsFromItemJSON(res, 2)), 0)
        res = getReadOneStakeholder(self, shUid2, 'json')
        self.assertEqual(res['total'], 3)
        self.assertEqual(STATUS_PENDING, getStatusFromItemJSON(res, 0))
        self.assertEqual(STATUS_EDITED, getStatusFromItemJSON(res, 1))
        self.assertEqual(STATUS_PENDING, getStatusFromItemJSON(res, 2))
        self.assertEqual(len(getInvolvementsFromItemJSON(res, 0)), 2)
        self.assertEqual(len(getInvolvementsFromItemJSON(res, 1)), 1)
        self.assertEqual(len(getInvolvementsFromItemJSON(res, 2)), 0)

    def test_setup_01_review(self):
        """
        For the rather complicated setup of this test, have a look at 
        "Setup Test 01" in the drive folder.
        """
        doLogin(self)
        # Create a first Stakeholder
        shUid1 = createStakeholder(self, getNewStakeholderDiff(), returnUid=True)
        # Create a second Stakeholder
        shUid2 = createStakeholder(self, getNewStakeholderDiff(), returnUid=True)
        # Create a first Activity
        aUid1 = createActivity(self, getNewActivityDiff(1), returnUid=True)
        # Edit the Activity and add the first Stakeholder as involvement
        invData1 = [{
            'id': shUid1,
            'version': 1,
            'role': 6
        }]
        createActivity(self, getEditActivityDiff(aUid1, version=1, type=2, 
            data=invData1))
        # Create a second Activity and add the second Stakeholder as involvement
        invData2 = [{
            'id': shUid2,
            'version': 1,
            'role': 6
        }]
        aUid2 = createActivity(self, getNewActivityDiff(3, data=invData2), 
            returnUid=True)
        # Create a third Activity and add both Stakeholders as involvement
        invData3 = [{
            'id': shUid1,
            'version': 2,
            'role': 6
        }, {
            'id': shUid2,
            'version': 2,
            'role': 6
        }]
        aUid3 = createActivity(self, getNewActivityDiff(3, data=invData3), 
            returnUid=True)

        # None of the Activities can be reviewed because of SH
        res = reviewActivity(self, aUid1, version=2)
        checkReviewActivityNotPossibleBcStakeholder(self, res)
        res = reviewActivity(self, aUid2, version=1)
        checkReviewActivityNotPossibleBcStakeholder(self, res)
        res = reviewActivity(self, aUid3, version=1)
        checkReviewActivityNotPossibleBcStakeholder(self, res)
        
        # SH1v1 can be reviewed
        reviewStakeholder(self, shUid1, version=1)
        
        # A1v2 can be reviewed
        reviewActivity(self, aUid1, version=2)
        
        # SH1v3 cannot be reviewed because of A3
        res = reviewStakeholder(self, shUid1, version=3)
        checkReviewStakeholderNotPossibleBcInvolvements(self, res)
        
        # A3v1 can not be reviewed because of SH2
        res = reviewActivity(self, aUid3, version=1)
        checkReviewActivityNotPossibleBcStakeholder(self, res)

        # SH2v1 can be reviewed
        reviewStakeholder(self, shUid2, version=1)
        
        # A2v1 can now be reviewed
        reviewActivity(self, aUid2, version=1)
        
        # A3v1 can now be reviewed
        reviewActivity(self, aUid3, version=1)
        
        res = getReadOneActivity(self, aUid1, 'json')
        self.assertEqual(res['total'], 2)
        self.assertEqual(STATUS_ACTIVE, getStatusFromItemJSON(res, 0))
        self.assertEqual(STATUS_EDITED, getStatusFromItemJSON(res, 1))
        self.assertEqual(len(getInvolvementsFromItemJSON(res, 0)), 1)
        self.assertEqual(len(getInvolvementsFromItemJSON(res, 1)), 0)
        res = getReadOneActivity(self, aUid2, 'json')
        self.assertEqual(res['total'], 1)
        self.assertEqual(STATUS_ACTIVE, getStatusFromItemJSON(res, 0))
        self.assertEqual(len(getInvolvementsFromItemJSON(res, 0)), 1)
        res = getReadOneActivity(self, aUid3, 'json')
        self.assertEqual(res['total'], 1)
        self.assertEqual(STATUS_ACTIVE, getStatusFromItemJSON(res, 0))
        self.assertEqual(len(getInvolvementsFromItemJSON(res, 0)), 2)
        res = getReadOneStakeholder(self, shUid1, 'json')
        self.assertEqual(res['total'], 3)
        self.assertEqual(STATUS_ACTIVE, getStatusFromItemJSON(res, 0))
        self.assertEqual(STATUS_INACTIVE, getStatusFromItemJSON(res, 1))
        self.assertEqual(STATUS_INACTIVE, getStatusFromItemJSON(res, 2))
        self.assertEqual(len(getInvolvementsFromItemJSON(res, 0)), 2)
        self.assertEqual(len(getInvolvementsFromItemJSON(res, 1)), 1)
        self.assertEqual(len(getInvolvementsFromItemJSON(res, 2)), 0)
        res = getReadOneStakeholder(self, shUid2, 'json')
        self.assertEqual(res['total'], 3)
        self.assertEqual(STATUS_ACTIVE, getStatusFromItemJSON(res, 0))
        self.assertEqual(STATUS_INACTIVE, getStatusFromItemJSON(res, 1))
        self.assertEqual(STATUS_INACTIVE, getStatusFromItemJSON(res, 2))
        self.assertEqual(len(getInvolvementsFromItemJSON(res, 0)), 2)
        self.assertEqual(len(getInvolvementsFromItemJSON(res, 1)), 1)
        self.assertEqual(len(getInvolvementsFromItemJSON(res, 2)), 0)

    def test_setup_02(self):
        """
        For the rather complicated setup of this test, have a look at 
        "Setup Test 02" in the drive folder.
        """
        doLogin(self)
        # Create a first Stakeholder
        shUid1 = createStakeholder(self, getNewStakeholderDiff(), returnUid=True)
        # Create a second Stakeholder
        shUid2 = createStakeholder(self, getNewStakeholderDiff(), returnUid=True)
        # Create a first Activity
        aUid1 = createActivity(self, getNewActivityDiff(1), returnUid=True)
        # Edit the Activity and add the first Stakeholder as involvement
        invData1 = [{
            'id': shUid1,
            'version': 1,
            'role': 6
        }]
        createActivity(self, getEditActivityDiff(aUid1, version=1, type=2, 
            data=invData1))
        # Create a second Activity and add the second Stakeholder as involvement
        invData2 = [{
            'id': shUid2,
            'version': 1,
            'role': 6
        }]
        aUid2 = createActivity(self, getNewActivityDiff(3, data=invData2), 
            returnUid=True)
        # Create a third Activity and add both Stakeholders as involvement
        invData3 = [{
            'id': shUid1,
            'version': 2,
            'role': 6
        }, {
            'id': shUid2,
            'version': 2,
            'role': 6
        }]
        aUid3 = createActivity(self, getNewActivityDiff(3, data=invData3), 
            returnUid=True)
        # Edit the third Activity
        createActivity(self, getEditActivityDiff(aUid3, type=1))
        
        # Check that everything was added correctly
        res = getReadOneActivity(self, aUid1, 'json')
        self.assertEqual(res['total'], 2)
        self.assertEqual(STATUS_PENDING, getStatusFromItemJSON(res, 0))
        self.assertEqual(STATUS_EDITED, getStatusFromItemJSON(res, 1))
        self.assertEqual(len(getInvolvementsFromItemJSON(res, 0)), 1)
        self.assertEqual(len(getInvolvementsFromItemJSON(res, 1)), 0)
        res = getReadOneActivity(self, aUid2, 'json')
        self.assertEqual(res['total'], 1)
        self.assertEqual(STATUS_PENDING, getStatusFromItemJSON(res, 0))
        self.assertEqual(len(getInvolvementsFromItemJSON(res, 0)), 1)
        res = getReadOneActivity(self, aUid3, 'json')
        self.assertEqual(res['total'], 2)
        self.assertEqual(STATUS_PENDING, getStatusFromItemJSON(res, 0))
        self.assertEqual(STATUS_EDITED, getStatusFromItemJSON(res, 1))
        self.assertEqual(len(getInvolvementsFromItemJSON(res, 0)), 2)
        self.assertEqual(len(getInvolvementsFromItemJSON(res, 1)), 2)
        res = getReadOneStakeholder(self, shUid1, 'json')
        self.assertEqual(res['total'], 3)
        self.assertEqual(STATUS_PENDING, getStatusFromItemJSON(res, 0))
        self.assertEqual(STATUS_EDITED, getStatusFromItemJSON(res, 1))
        self.assertEqual(STATUS_PENDING, getStatusFromItemJSON(res, 2))
        self.assertEqual(len(getInvolvementsFromItemJSON(res, 0)), 2)
        self.assertEqual(len(getInvolvementsFromItemJSON(res, 1)), 1)
        self.assertEqual(len(getInvolvementsFromItemJSON(res, 2)), 0)
        res = getReadOneStakeholder(self, shUid2, 'json')
        self.assertEqual(res['total'], 3)
        self.assertEqual(STATUS_PENDING, getStatusFromItemJSON(res, 0))
        self.assertEqual(STATUS_EDITED, getStatusFromItemJSON(res, 1))
        self.assertEqual(STATUS_PENDING, getStatusFromItemJSON(res, 2))
        self.assertEqual(len(getInvolvementsFromItemJSON(res, 0)), 2)
        self.assertEqual(len(getInvolvementsFromItemJSON(res, 1)), 1)
        self.assertEqual(len(getInvolvementsFromItemJSON(res, 2)), 0)

    def test_setup_02_review(self):
        """
        For the rather complicated setup of this test, have a look at 
        "Setup Test 02" in the drive folder.
        """
        doLogin(self)
        # Create a first Stakeholder
        shUid1 = createStakeholder(self, getNewStakeholderDiff(), returnUid=True)
        # Create a second Stakeholder
        shUid2 = createStakeholder(self, getNewStakeholderDiff(), returnUid=True)
        # Create a first Activity
        aUid1 = createActivity(self, getNewActivityDiff(1), returnUid=True)
        # Edit the Activity and add the first Stakeholder as involvement
        invData1 = [{
            'id': shUid1,
            'version': 1,
            'role': 6
        }]
        createActivity(self, getEditActivityDiff(aUid1, version=1, type=2, 
            data=invData1))
        # Create a second Activity and add the second Stakeholder as involvement
        invData2 = [{
            'id': shUid2,
            'version': 1,
            'role': 6
        }]
        aUid2 = createActivity(self, getNewActivityDiff(3, data=invData2), 
            returnUid=True)
        # Create a third Activity and add both Stakeholders as involvement
        invData3 = [{
            'id': shUid1,
            'version': 2,
            'role': 6
        }, {
            'id': shUid2,
            'version': 2,
            'role': 6
        }]
        aUid3 = createActivity(self, getNewActivityDiff(3, data=invData3), 
            returnUid=True)
        # Edit the third Activity
        createActivity(self, getEditActivityDiff(aUid3, type=1))
        
        # None of the Activities can be reviewed because of SH
        res = reviewActivity(self, aUid1, version=2)
        checkReviewActivityNotPossibleBcStakeholder(self, res)
        res = reviewActivity(self, aUid2, version=1)
        checkReviewActivityNotPossibleBcStakeholder(self, res)
        res = reviewActivity(self, aUid3, version=2)
        checkReviewActivityNotPossibleBcStakeholder(self, res)
        
        # SH1v1 can be reviewed
        reviewStakeholder(self, shUid1, version=1)
        
        # A1v2 can now be reviewed
        reviewActivity(self, aUid1, version=2)
        
        # SH2v1 can be reviewd
        reviewStakeholder(self, shUid2, version=1)
        
        # A2v1 can now be reviewed.
        reviewActivity(self, aUid2, version=1)
        
        # A3v2 can now be reviewed.
        reviewActivity(self, aUid3, version=2)
        
        res = getReadOneActivity(self, aUid1, 'json')
        self.assertEqual(res['total'], 2)
        self.assertEqual(STATUS_ACTIVE, getStatusFromItemJSON(res, 0))
        self.assertEqual(STATUS_EDITED, getStatusFromItemJSON(res, 1))
        self.assertEqual(len(getInvolvementsFromItemJSON(res, 0)), 1)
        self.assertEqual(len(getInvolvementsFromItemJSON(res, 1)), 0)
        res = getReadOneActivity(self, aUid2, 'json')
        self.assertEqual(res['total'], 1)
        self.assertEqual(STATUS_ACTIVE, getStatusFromItemJSON(res, 0))
        self.assertEqual(len(getInvolvementsFromItemJSON(res, 0)), 1)
        res = getReadOneActivity(self, aUid3, 'json')
        self.assertEqual(res['total'], 2)
        self.assertEqual(STATUS_ACTIVE, getStatusFromItemJSON(res, 0))
        self.assertEqual(STATUS_EDITED, getStatusFromItemJSON(res, 1))
        self.assertEqual(len(getInvolvementsFromItemJSON(res, 0)), 2)
        self.assertEqual(len(getInvolvementsFromItemJSON(res, 1)), 2)
        res = getReadOneStakeholder(self, shUid1, 'json')
        res = getReadOneStakeholder(self, shUid2, 'json')
        self.assertEqual(res['total'], 3)
        self.assertEqual(STATUS_ACTIVE, getStatusFromItemJSON(res, 0))
        self.assertEqual(STATUS_INACTIVE, getStatusFromItemJSON(res, 1))
        self.assertEqual(STATUS_INACTIVE, getStatusFromItemJSON(res, 2))
        self.assertEqual(len(getInvolvementsFromItemJSON(res, 0)), 2)
        self.assertEqual(len(getInvolvementsFromItemJSON(res, 1)), 1)
        self.assertEqual(len(getInvolvementsFromItemJSON(res, 2)), 0)
        res = getReadOneStakeholder(self, shUid2, 'json')
        self.assertEqual(res['total'], 3)
        self.assertEqual(STATUS_ACTIVE, getStatusFromItemJSON(res, 0))
        self.assertEqual(STATUS_INACTIVE, getStatusFromItemJSON(res, 1))
        self.assertEqual(STATUS_INACTIVE, getStatusFromItemJSON(res, 2))
        self.assertEqual(len(getInvolvementsFromItemJSON(res, 0)), 2)
        self.assertEqual(len(getInvolvementsFromItemJSON(res, 1)), 1)
        self.assertEqual(len(getInvolvementsFromItemJSON(res, 2)), 0)

@pytest.mark.usefixtures('app')
@pytest.mark.integration
@pytest.mark.activities
@pytest.mark.moderation
class ActivityHistoryTests(TestCase):
    
    def test_history_view(self):
        """
        Test that a history view is available for newly created Activities.
        """
        doLogin(self)
        uid = createActivity(self, getNewActivityDiff(), returnUid=True)
        
        res = self.app.get('/activities/history/html/%s' % uid)
        self.assertEqual(res.status_int, 200)
        self.assertIn(TITLE_HISTORY_VIEW, res.body)
        