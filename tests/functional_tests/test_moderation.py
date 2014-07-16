import pytest
import uuid
from selenium import webdriver
from unittest import TestCase

from .base import *
from ..base import *


@pytest.mark.functional
@pytest.mark.moderation
class ModerationTests(TestCase):
    
    def setUp(self):
        self.driver = webdriver.Firefox()
    
    def tearDown(self):
        self.driver.quit()
    
    def test_approve_activity(self):
        """
        Test that a new Activity can be approved.
        """
        
        uid = doCreateActivity(self)
        link = createUrl('/activities/html/%s' % uid)

        # Check that it is pending and there is a moderation link
        self.driver.get(link)
        self.assertTrue(checkIsPending(self))
        reviewLink = self.driver.find_element_by_xpath("//a[contains(@href, '/activities/review/')]")
        self.assertIn(LINK_REVIEW, reviewLink.text)
        
        self.driver.get(reviewLink.get_attribute('href'))
        self.assertIn(TITLE_DEAL_MODERATION, self.driver.title)
        btn = self.driver.find_element_by_xpath("//button[contains(concat(' ', @class, ' '), ' btn-success ') and contains(text(), '%s')]" % BUTTON_APPROVE)
        btn.click()
        
        getEl(self, 'class_name', 'alert-success')
        
        # Make sure the Activity is not pending anymore
        self.driver.get(link)
        self.assertFalse(checkIsPending(self))
    
    def test_approve_activity_with_new_involvement(self):
        """
        Test that a new Activity with a new involvement can be approved.
        """
        
        aUid = doCreateActivity(self, createSH=True)
        
        # Check that the Activity cannot be reviewed because of the pending SH
        self.driver.get(createUrl('/activities/review/%s' % aUid))
        self.driver.find_element_by_xpath("//button[contains(concat(' ', @class, ' '), ' disabled ') and contains(text(), '%s')]" % BUTTON_APPROVE)
        getEl(self, 'class_name', 'alert-missing-mandatory-keys')
        
        # Make sure the Stakeholder can be reviewed and do this
        self.driver.find_element_by_xpath("//a[contains(@href, '/stakeholders/review/')]").click()
        self.assertIn(TITLE_STAKEHOLDER_MODERATION, self.driver.title)
        self.driver.find_element_by_xpath("//button[contains(concat(' ', @class, ' '), ' btn-success ') and contains(text(), '%s')]" % BUTTON_APPROVE).click()
        
        # Make sure there is a Success message and a notice that the Activity 
        # can now be reviewed.
        getEl(self, 'class_name', 'alert-success')
        self.assertIn('You had to review this', self.driver.page_source)
        self.driver.find_element_by_link_text('Click here to return to the Activity and review it.').click()
        
        # Make sure the Activity can now be reviewed.
        self.assertIn(TITLE_DEAL_MODERATION, self.driver.title)
        self.driver.find_element_by_xpath("//button[contains(concat(' ', @class, ' '), ' btn-success ') and contains(text(), '%s')]" % BUTTON_APPROVE).click()
        
        # Make sure the Activity is not pending anymore
        self.driver.get(createUrl('/activities/html/%s' % aUid))
        self.assertFalse(checkIsPending(self))
        
        # Go to Stakeholder and make sure it is not pending anymore
        self.driver.find_element_by_link_text(LINK_DEAL_SHOW_INVOLVEMENT).click()
        self.assertFalse(checkIsPending(self))
    
    def test_edited_stakeholders_with_involvements_can_be_approved(self):
        """
        Bugfix: Edited Stakeholders with an involvement could not be approved
        from Stakeholder side, thus blocking the review process.
        """
        
        aUid = doCreateActivity(self, createSH=True)
        
        # Review both Activity (first) and Stakeholder (second)
        self.driver.get(createUrl('/activities/review/%s' % aUid))
        shLink = self.driver.find_element_by_xpath("//a[contains(@href, '/stakeholders/review/')]").get_attribute('href')
        shUid = shLink.split('/')[len(shLink.split('/'))-1]
        self.driver.find_element_by_xpath("//a[contains(@href, '/stakeholders/review/')]").click()
        self.driver.find_element_by_xpath("//button[contains(concat(' ', @class, ' '), ' btn-success ') and contains(text(), '%s')]" % BUTTON_APPROVE).click()
        self.driver.find_element_by_link_text('Click here to return to the Activity and review it.').click()
        self.driver.implicitly_wait(10)
        self.driver.find_element_by_xpath("//button[contains(concat(' ', @class, ' '), ' btn-success ') and contains(text(), '%s')]" % BUTTON_APPROVE).click()
        
        # Go to Stakeholder and edit it
        self.driver.get(createUrl('/stakeholders/form/%s' % shUid))
        self.driver.find_element_by_xpath("//textarea[@name='[SH] Textarea 1']").send_keys('Added input')
        self.driver.find_element_by_id('stakeholderformsubmit').click()
        
        # Go to moderation of the Stakeholder, it should be approvable
        self.driver.get(createUrl('/stakeholders/review/%s' % shUid))
        self.driver.find_element_by_xpath("//button[contains(concat(' ', @class, ' '), ' btn-success ') and contains(text(), '%s')]" % BUTTON_APPROVE).click()

        # Make sure the Stakeholder was approved correctly
        getEl(self, 'class_name', 'alert-success')
        self.driver.get(createUrl('/stakeholders/html/%s' % shUid))
        self.assertFalse(checkIsPending(self))

    def test_show_warning_prevent_automatic_revision_of_involvements(self):
        """
        Test that the warning that indicates prevention of automatic revision is
        shown where it should be.
        It is shown on Activity side if the involved Stakeholder has no active
        version yet.
        It is shown on Stakeholder side if there is an involvement because these
        always have to be reviewed from Activity side.
        """
        
        # Create a Stakeholder with a known name.
        shName = str(uuid.uuid4())
        shValues = {
            'tf1': shName
        }
        doCreateActivity(self, createSH=True, shValues=shValues, noSubmit=True)
        
        # Create an Activity with the Stakeholder
        knownSh = [{
            'name': shName
        }]
        aUid1 = doCreateActivity(self, createSH=True, knownSh=knownSh)
        
        # Create another Activity with the same Stakeholder
        aUid2 = doCreateActivity(self, createSH=True, knownSh=knownSh)
        
        # A1v1 cannot be reviewed because of SH
        self.driver.get(createUrl('/activities/review/%s' % aUid1))
        shLink = self.driver.find_element_by_xpath("//a[contains(@href, '/stakeholders/review/')]").get_attribute('href')
        shUid = shLink.split('/')[len(shLink.split('/'))-1]
        shUid = shUid.split('?')[0]
        
        self.driver.find_element_by_xpath("//button[contains(concat(' ', @class, ' '), ' disabled ') and contains(text(), '%s')]" % BUTTON_APPROVE)
        findTextOnPage(self, FEEDBACK_INVOLVEMENTS_CANNOT_BE_REVIEWED)
        
        # A2v1 cannot be reviewed because of SH
        self.driver.get(createUrl('/activities/review/%s' % aUid2))
        self.driver.find_element_by_xpath("//button[contains(concat(' ', @class, ' '), ' disabled ') and contains(text(), '%s')]" % BUTTON_APPROVE)
        findTextOnPage(self, FEEDBACK_INVOLVEMENTS_CANNOT_BE_REVIEWED)
        
        # SHv3 cannot be reviewed because of A
        self.driver.get(createUrl('/stakeholders/review/%s?new=3' % shUid))
        self.driver.find_element_by_xpath("//button[contains(concat(' ', @class, ' '), ' disabled ') and contains(text(), '%s')]" % BUTTON_APPROVE)
        findTextOnPage(self, FEEDBACK_INVOLVEMENTS_CANNOT_BE_REVIEWED_FROM_STAKEHOLDER)
        
        # SHv1 can now be reviewed
        doReview(self, 'sh', shUid)
        
        # SHv3 can still not be reviewed because of A
        self.driver.get(createUrl('/stakeholders/review/%s?new=3' % shUid))
        self.driver.find_element_by_xpath("//button[contains(concat(' ', @class, ' '), ' disabled ') and contains(text(), '%s')]" % BUTTON_APPROVE)
        findTextOnPage(self, FEEDBACK_INVOLVEMENTS_CANNOT_BE_REVIEWED_FROM_STAKEHOLDER)
        
        # A1v1 can now be reviewed
        doReview(self, 'a', aUid1)
        
        # SHv3 can still not be reviewed because of A
        self.driver.get(createUrl('/stakeholders/review/%s?new=3' % shUid))
        self.driver.find_element_by_xpath("//button[contains(concat(' ', @class, ' '), ' disabled ') and contains(text(), '%s')]" % BUTTON_APPROVE)
        findTextOnPage(self, FEEDBACK_INVOLVEMENTS_CANNOT_BE_REVIEWED_FROM_STAKEHOLDER)
        
        # Review A2v1
        doReview(self, 'a', aUid2)
        
        # All should be active now
        openItemDetailsPage(self, 'activities', aUid1)
        self.assertFalse(checkIsPending(self))
        openItemDetailsPage(self, 'activities', aUid2)
        self.assertFalse(checkIsPending(self))
        openItemDetailsPage(self, 'stakeholders', shUid)
        self.assertFalse(checkIsPending(self))
        