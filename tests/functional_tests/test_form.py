import pytest
from selenium import webdriver
from selenium.webdriver.support.ui import Select
from unittest import TestCase

from .base import *

@pytest.mark.functional
@pytest.mark.form
class  FormTest(TestCase):
    
    def setUp(self):
        self.driver = webdriver.Firefox()

    def tearDown(self):
        self.driver.quit()

    def test_integer_dropdown_fields(self):
        """
        Test the IntegerDropdown fields of the form. In particular, test that:
        - field values are saved and repopulated after form tab change
        - field values are stored and displayed correctly after submission
        - field values can be edited
        """
        
        # Start the form with some Integerdropdown values
        id1 = '[A] Integerdropdown 1'
        id2 = '[A] Integerdropdown 2'
        cat4Values = {
            id1: 1,
            id2: 2
        }
        doCreateActivity(self, cat4=cat4Values, noSubmit=True)
        
        # Reload category 4 and make sure the previously selected values of the
        # IntegerDropdown are still there.
        self.driver.find_element_by_id('activityformstep_53').click()
        id1El = Select(getEl(self, 'xpath', "//select[@name='%s']" % id1))
        id1sel = id1El.first_selected_option.get_attribute('value')
        self.assertEqual(id1sel, '1')
        id2El = Select(getEl(self, 'xpath', "//select[@name='%s']" % id2))
        id2sel = id2El.first_selected_option.get_attribute('value')
        self.assertEqual(id2sel, '2')
        
        # Submit and make sure the values are stored correctly
        uid = doActivitySubmit(self)
        openItemDetailsPage(self, 'activities', uid)
        findTextOnPage(self, id1)
        findTextOnPage(self, id2)
        findTextOnPage(self, '[A] Integerdropdown', 2)

        # Edit and check the values are still there
        openItemFormPage(self, 'activities', uid)
        self.driver.find_element_by_id('activityformstep_53').click()
        id1El = Select(getEl(self, 'xpath', "//select[@name='%s']" % id1))
        id1sel = id1El.first_selected_option.get_attribute('value')
        self.assertEqual(id1sel, '1')
        id2El = Select(getEl(self, 'xpath', "//select[@name='%s']" % id2))
        id2sel = id2El.first_selected_option.get_attribute('value')
        self.assertEqual(id2sel, '2')
        
        # Make some changes, submit and check the changes
        id1El.select_by_value('')
        id2El.select_by_value('3')
        doActivitySubmit(self)
        openItemDetailsPage(self, 'activities', uid)
        try:
            findTextOnPage(self, id1)
        except Exception:
            pass
        findTextOnPage(self, id2)
        findTextOnPage(self, '[A] Integerdropdown', 1)
        
        
        