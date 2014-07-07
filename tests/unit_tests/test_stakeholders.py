import unittest
import pytest
from webtest import TestApp
from pyramid.paster import get_appsettings

from lmkp import main
from .base import *
from .stakeholders import *

@pytest.mark.usefixtures("db_session")
class StakeholderCreateTests(unittest.TestCase):
    def setUp(self):
        settings = get_appsettings(CONFIG_FILE)
        app = main({}, settings=settings)
        self.testapp = TestApp(app)
        
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
        res = createStakeholder(self, getStakeholderDiff())
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
        
        createStakeholder(self, getStakeholderDiff())
        
        json = getReadManyStakeholders(self, 'json')
        self.assertEqual(json['total'], 1)
    
    
@pytest.mark.usefixtures("db_session")
class StakeholderModerateTests(unittest.TestCase):

    def setUp(self):
        settings = get_appsettings(CONFIG_FILE)
        app = main({}, settings=settings)
        self.testapp = TestApp(app)
    
    def test_new_stakeholders_can_be_approved(self):
        """
        New Stakeholders with all mandatory keys can be approved.
        """
        doLogin(self)
        uid = createStakeholder(self, getStakeholderDiff(), returnUid=True)
        
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
        uid = createStakeholder(self, getStakeholderDiff(), returnUid=True)
        
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
        uid = createStakeholder(self, getStakeholderDiff(2), returnUid=True)
        
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
        uid = createStakeholder(self, getStakeholderDiff(2), returnUid=True)
        
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