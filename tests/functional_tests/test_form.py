import pytest
from selenium.webdriver.support.ui import Select

from .base import LmkpFunctionalTestCase


@pytest.mark.usefixtures('app_functional')
@pytest.mark.functional
@pytest.mark.form
class FormTests(LmkpFunctionalTestCase):

    def test_integer_dropdown_fields(self):
        """
        Test the IntegerDropdown fields of the form. In particular, test that:
        - field values are saved and repopulated after form tab change
        - field values are stored and displayed correctly after submission
        - field values can be edited
        """

        # Start the form with some Integerdropdown values
        id_1 = '[A] Integerdropdown 1'
        id_2 = '[A] Integerdropdown 2'
        values = {'cat4': {
            id_1: 1,
            id_2: 2
        }}
        self.create_activity(values=values, no_submit=True)

        # Reload category 4 and make sure the previously selected values of the
        # IntegerDropdown are still there.
        self.el('id', 'activityformstep_53').click()
        id_1_el = Select(self.el('xpath', "//select[@name='%s']" % id_1))
        id_1_sel = id_1_el.first_selected_option.get_attribute('value')
        self.assertEqual(id_1_sel, '1')
        id_2_el = Select(self.el('xpath', "//select[@name='%s']" % id_2))
        id_2_sel = id_2_el.first_selected_option.get_attribute('value')
        self.assertEqual(id_2_sel, '2')

        # Submit and make sure the values are stored correctly
        uid = self.submit_activity()
        self.open_details('activities', uid)
        self.find_text(id_1)
        self.find_text(id_2)
        self.find_text('[A] Integerdropdown', 2)

        # Edit and check the values are still there
        self.open_form('activities', uid=uid)
        self.el('id', 'activityformstep_53').click()
        id_1_el = Select(self.el('xpath', "//select[@name='%s']" % id_1))
        id_1_sel = id_1_el.first_selected_option.get_attribute('value')
        self.assertEqual(id_1_sel, '1')
        id_2_el = Select(self.el('xpath', "//select[@name='%s']" % id_2))
        id_2_sel = id_2_el.first_selected_option.get_attribute('value')
        self.assertEqual(id_2_sel, '2')

        # Make some changes, submit and check the changes
        id_1_el.select_by_value('')
        id_2_el.select_by_value('3')
        self.submit_activity()
        self.open_details('activities', uid)
        try:
            self.find_text(id_1)
        except Exception:
            pass
        self.find_text(id_2)
        self.find_text('[A] Integerdropdown', 1)
