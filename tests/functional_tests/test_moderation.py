import pytest
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
        
        doLogin(self.driver)
        
        uid = doCreateActivity(self.driver)
        link = createUrl('/activities/html/%s' % uid)

        # Check that it is pending and there is a moderation link
        self.driver.get(link)
        self.assertTrue(checkIsPending(self.driver))
        reviewLink = self.driver.find_element_by_xpath("//a[contains(@href, '/activities/review/')]")
        self.assertIn(LINK_REVIEW, reviewLink.text)
        
        self.driver.get(reviewLink.get_attribute('href'))
        self.assertIn(TITLE_DEAL_MODERATION, self.driver.title)
        btn = self.driver.find_element_by_xpath("//button[contains(concat(' ', @class, ' '), ' btn-success ') and contains(text(), '%s')]" % BUTTON_APPROVE)
        btn.click()
        
        self.assertTrue(checkElExists(self.driver, 'class_name', 'alert-success'))
        
        # Make sure the Activity is not pending anymore
        self.driver.get(link)
        self.assertFalse(checkIsPending(self.driver))
    
    def test_approve_activity_with_new_involvement(self):
        """
        Test that a new Activity with a new involvement can be approved.
        """
        
        doLogin(self.driver)
        
        aUid = doCreateActivity(self.driver, createSH=True)
        
        # Check that the Activity cannot be reviewed because of the pending SH
        self.driver.get(createUrl('/activities/review/%s' % aUid))
        self.driver.find_element_by_xpath("//button[contains(concat(' ', @class, ' '), ' disabled ') and contains(text(), '%s')]" % BUTTON_APPROVE)
        self.assertTrue(checkElExists(self.driver, 'class_name', 'alert-missing-mandatory-keys'))
        
        # Make sure the Stakeholder can be reviewed and do this
        self.driver.find_element_by_xpath("//a[contains(@href, '/stakeholders/review/')]").click()
        self.assertIn(TITLE_STAKEHOLDER_MODERATION, self.driver.title)
        self.driver.find_element_by_xpath("//button[contains(concat(' ', @class, ' '), ' btn-success ') and contains(text(), '%s')]" % BUTTON_APPROVE).click()
        
        # Make sure there is a Success message and a notice that the Activity 
        # can now be reviewed.
        self.assertTrue(checkElExists(self.driver, 'class_name', 'alert-success'))
        self.assertIn('You had to review this', self.driver.page_source)
        self.driver.find_element_by_link_text('Click here to return to the Activity and review it.').click()
        
        # Make sure the Activity can now be reviewed.
        self.assertIn(TITLE_DEAL_MODERATION, self.driver.title)
        self.driver.find_element_by_xpath("//button[contains(concat(' ', @class, ' '), ' btn-success ') and contains(text(), '%s')]" % BUTTON_APPROVE).click()
        
        # Make sure the Activity is not pending anymore
        self.driver.get(createUrl('/activities/html/%s' % aUid))
        self.assertFalse(checkIsPending(self.driver))
        
        # Go to Stakeholder and make sure it is not pending anymore
        self.driver.find_element_by_link_text(LINK_DEAL_SHOW_INVOLVEMENT).click()
        self.assertFalse(checkIsPending(self.driver))
    
    def test_edited_stakeholders_with_involvements_can_be_approved(self):
        """
        Bugfix: Edited Stakeholders with an involvement could not be approved
        from Stakeholder side, thus blocking the review process.
        """
        
        doLogin(self.driver)
        
        aUid = doCreateActivity(self.driver, createSH=True)
        
        # Review both Activity (first) and Stakeholder (second)
        self.driver.get(createUrl('/activities/review/%s' % aUid))
        shLink = self.driver.find_element_by_xpath("//a[contains(@href, '/stakeholders/review/')]").get_attribute('href')
        shUid = shLink.split('/')[len(shLink.split('/'))-1]
        self.driver.find_element_by_xpath("//a[contains(@href, '/stakeholders/review/')]").click()
        self.driver.find_element_by_xpath("//button[contains(concat(' ', @class, ' '), ' btn-success ') and contains(text(), '%s')]" % BUTTON_APPROVE).click()
        self.driver.find_element_by_link_text('Click here to return to the Activity and review it.').click()
        self.driver.find_element_by_xpath("//button[contains(concat(' ', @class, ' '), ' btn-success ') and contains(text(), '%s')]" % BUTTON_APPROVE).click()
        
        # Go to Stakeholder and edit it
        self.driver.get(createUrl('/stakeholders/form/%s' % shUid))
        self.driver.find_element_by_xpath("//textarea[@name='[SH] Textarea 1']").send_keys('Added input')
        self.driver.find_element_by_id('stakeholderformsubmit').click()
        
        # Go to moderation of the Stakeholder, it should be approvable
        self.driver.get(createUrl('/stakeholders/review/%s' % shUid))
        self.driver.find_element_by_xpath("//button[contains(concat(' ', @class, ' '), ' btn-success ') and contains(text(), '%s')]" % BUTTON_APPROVE).click()

        # Make sure the Stakeholderw as approved correctly
        self.assertTrue(checkElExists(self.driver, 'class_name', 'alert-success'))
        self.driver.get(createUrl('/stakeholders/html/%s' % shUid))
        self.assertFalse(checkIsPending(self.driver))