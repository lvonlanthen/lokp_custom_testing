import pytest
from selenium.webdriver.support.ui import Select

from .base import (
    doActivitySubmit,
    doCreateActivity,
    findTextOnPage,
    getEl,
    openItemDetailsPage,
    openItemFormPage,
)


@pytest.mark.functional
@pytest.mark.form
def test_integer_dropdown_fields(testcase):
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
    doCreateActivity(testcase, cat4=cat4Values, noSubmit=True)

    # Reload category 4 and make sure the previously selected values of the
    # IntegerDropdown are still there.
    testcase.driver.find_element_by_id('activityformstep_53').click()
    id1El = Select(getEl(testcase, 'xpath', "//select[@name='%s']" % id1))
    id1sel = id1El.first_selected_option.get_attribute('value')
    testcase.assertEqual(id1sel, '1')
    id2El = Select(getEl(testcase, 'xpath', "//select[@name='%s']" % id2))
    id2sel = id2El.first_selected_option.get_attribute('value')
    testcase.assertEqual(id2sel, '2')

    # Submit and make sure the values are stored correctly
    uid = doActivitySubmit(testcase)
    openItemDetailsPage(testcase, 'activities', uid)
    findTextOnPage(testcase, id1)
    findTextOnPage(testcase, id2)
    findTextOnPage(testcase, '[A] Integerdropdown', 2)

    # Edit and check the values are still there
    openItemFormPage(testcase, 'activities', uid)
    testcase.driver.find_element_by_id('activityformstep_53').click()
    id1El = Select(getEl(testcase, 'xpath', "//select[@name='%s']" % id1))
    id1sel = id1El.first_selected_option.get_attribute('value')
    testcase.assertEqual(id1sel, '1')
    id2El = Select(getEl(testcase, 'xpath', "//select[@name='%s']" % id2))
    id2sel = id2El.first_selected_option.get_attribute('value')
    testcase.assertEqual(id2sel, '2')

    # Make some changes, submit and check the changes
    id1El.select_by_value('')
    id2El.select_by_value('3')
    doActivitySubmit(testcase)
    openItemDetailsPage(testcase, 'activities', uid)
    try:
        findTextOnPage(testcase, id1)
    except Exception:
        pass
    findTextOnPage(testcase, id2)
    findTextOnPage(testcase, '[A] Integerdropdown', 1)
        
        