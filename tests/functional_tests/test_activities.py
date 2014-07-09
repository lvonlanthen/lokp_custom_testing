import pytest
from selenium import webdriver
from unittest import TestCase

from .base import *

@pytest.mark.functional
@pytest.mark.activities
class ActivitiesTests(TestCase):
    
    def setUp(self):
        self.driver = webdriver.Firefox()
    
    def tearDown(self):
        self.driver.quit()
    
    def test_create_activity(self):
        """
        Test that a new Activity can be created.
        """
        
        doLogin(self.driver)
        
        # Count how many Activities there are already
        self.driver.get(createUrl('/activities/html'))
        if checkElExists(self.driver, 'tag_name', 'h5'):
            countBefore = 0
        else:
            countBefore = self.driver.find_element_by_xpath("//div[contains(@class, 'span4')]/strong")
            countBefore = int(countBefore.text)
            
        uid = doCreateActivity(self.driver)

        # Count how many Activities there are now
        self.driver.get(createUrl('/activities/html'))
        countAfter = self.driver.find_element_by_xpath("//div[contains(@class, 'span4')]/strong")
        countAfter = int(countAfter.text)
        self.assertEqual(countBefore + 1, countAfter)

        # Check that a detail page is available
        self.driver.get(createUrl('/activities/html/%s' % uid))
        self.assertIn(TITLE_DEAL_DETAILS, self.driver.title)
        self.assertTrue(checkIsPending(self.driver))

    def test_create_activity_with_new_involvement(self):
        """
        Test that a new Activity can be created with a new Involvement.
        """
        
        # Define some values
        aType = '[A] Value A1'
        shName = 'Specific SH'
        
        driver = self.driver
        doLogin(driver)
        
        # Start the Activity form
        doCreateActivity(driver, dd1=aType, noSubmit=True)
        
        # Add an involvement
        driver.find_element_by_id('activityformstep_3').click()
        self.assertIn(TITLE_DEAL_EDITOR, driver.title)
        shbtn = driver.find_elements_by_class_name('accordion-toggle')
        for el in shbtn:
            el.click()
        driver.find_element_by_name('createinvolvement_primaryinvestor').click()
        self.assertIn(TITLE_STAKEHOLDER_EDITOR, driver.title)
        
        # Create and submit a Stakeholder
        doCreateStakeholder(self.driver, tf1=shName)
        
        # Make sure we are back in Activity form and submit
        self.assertIn(TITLE_DEAL_EDITOR, driver.title)
        driver.find_element_by_id('activityformsubmit').click()
        link = driver.find_element_by_link_text(LINK_VIEW_DEAL).get_attribute('href')
        driver.get(link)
        self.assertIn(TITLE_DEAL_DETAILS, driver.title)
        pending = driver.find_element_by_tag_name('h4').text
        self.assertIn(TEXT_PENDING_VERSION, pending)
        
        # Make sure the Stakeholder is linked and view it's details
        self.assertIn(shName, driver.page_source)
        driver.find_element_by_link_text(LINK_DEAL_SHOW_INVOLVEMENT).click()
        self.assertIn(TITLE_STAKEHOLDER_DETAILS, driver.title)
        pending = driver.find_element_by_tag_name('h4').text
        self.assertIn(TEXT_PENDING_VERSION, pending)

        # Make sure the Activity is linked
        self.assertIn(aType, driver.page_source)
        checkElExists(driver, 'link_text', LINK_STAKEHOLDER_SHOW_INVOLVEMENT)
        
        def test_create_activity_with_existing_involvement(self):
            """
            Test that a new Activity can be created with an existing Stakeholder
            """
            
            doLogin(self.driver)
            
            aUid = doCreateActivity(self.driver, createSH=True)
            
            doReview(self.driver, 'a', aUid, withInv=True)
            
            