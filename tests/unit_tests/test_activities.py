import unittest
import pytest
from webtest import TestApp
from pyramid.paster import get_appsettings

from lmkp import main
from .base import *
from .activities import *


@pytest.mark.usefixtures("db_session")
class ActivityCreateTests(unittest.TestCase):
    def setUp(self):
        settings = get_appsettings(CONFIG_FILE)
        app = main({}, settings=settings)
        self.testapp = TestApp(app)
        
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
    

@pytest.mark.usefixtures("db_session")
class ActivityModerateTests(unittest.TestCase):

    def setUp(self):
        settings = get_appsettings(CONFIG_FILE)
        app = main({}, settings=settings)
        self.testapp = TestApp(app)
    
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