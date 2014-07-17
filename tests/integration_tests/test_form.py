import pytest
from unittest import TestCase

from .base import *
from .activities import createActivity, getNewActivityDiff, getReadOneActivity
from .stakeholders import createStakeholder, getNewStakeholderDiff, \
    getReadOneStakeholder
from ..base import *

@pytest.mark.usefixtures('app')
@pytest.mark.integration
@pytest.mark.form
class FormConfigTests(TestCase):
    
    def test_activities_thmg_show_in_details(self):
        """
        Test that the YAML configuration "showindetails" for Thematic Groups 
        works for Activities.
        """
        doLogin(self)
        uid = createActivity(self, getNewActivityDiff(4), returnUid=True)
        res = getReadOneActivity(self, uid, 'html')
        res.mustcontain('[A] Subcategory 8')
    
    def test_stakeholders_thmg_show_in_details(self):
        """
        Test that the YAML configuration "showindetails" for Thematic Groups
        works for Stakeholders.
        """
        doLogin(self)
        uid = createStakeholder(self, getNewStakeholderDiff(3), returnUid=True)
        res = getReadOneStakeholder(self, uid, 'html')
        res.mustcontain('[SH] Subcategory 6')