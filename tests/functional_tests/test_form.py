import pytest
import time
from selenium.webdriver.support.ui import Select

from .base import LmkpFunctionalTestCase
from ..base import (
    LINK_VIEW_DEAL,
    LINK_DEAL_SHOW_INVOLVEMENT,
)


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

    def test_multiple_select_stakeholders(self):

        def get_sh_names():
            """
            Helper function to extract 3 different Stakeholder names
            from the grid view.
            Creates the Stakeholders if necessary.
            """
            self.login(self.url('/stakeholders/html'))
            try:
                self.el('tag_name', 'tr')
                count = self.el(
                    'xpath', "//div[contains(@class, 'span4')]/strong")
                if int(count.text) < 3:
                    create_sh()
            except:
                create_sh()

            sh_names = []
            els = self.els('xpath', "//table/tbody/tr/td[3]")
            for el in els:
                if el.text not in sh_names and el.text != 'Unknown':
                    sh_names.append(el.text)

            if len(sh_names) < 3:
                create_sh()
                sh_names = []
                els = self.els('xpath', "//table/tbody/tr/td[3]")
                for el in els:
                    if el.text not in sh_names:
                        sh_names.append(el.text)

            return sh_names[:3]

        def create_sh():
            """
            Helper function to create 3 Stakeholders with different names.
            """
            sh_names = ['SH 1', 'SH 2', 'SH 3']
            for sh_name in sh_names:
                self.create_stakeholder(values={'tf1': sh_name})
                self.driver.get(self.url('/stakeholders/html'))

        # Collect 3 different Stakeholder names
        sh_names = get_sh_names()

        # Open the Activity form and go to the page to add Involvements
        self.create_activity(no_submit=True)
        self.el('id', 'activityformstep_3').click()

        # Open 3 more secondary involvement fields and open all
        # involvement fields to show the search field
        add_more_involvements_btn = self.el(
            'xpath',
            "//div[contains(@class, 'form-add-more-icon')]/span[contains("
            "@class, 'green pointer')]")
        for i in range(3):
            add_more_involvements_btn.click()
        select_stakeholder_btns = self.els('class_name', 'accordion-toggle')
        for select_sh_btn in select_stakeholder_btns:
            select_sh_btn.click()
            time.sleep(0.5)

        # Count the fields, panels and buttons
        primary_field = self.els('name', 'createinvolvement_primaryinvestor')
        self.assertEqual(len(primary_field), 1)
        secondary_fields = self.els(
            'name', 'createinvolvement_secondaryinvestor')
        self.assertEqual(len(secondary_fields), 4)
        sh_selection_panels = self.els(
            'xpath',
            "//div[contains(@class, 'accordion-body in collapse')]")
        self.assertEqual(len(sh_selection_panels), 5)
        close_buttons = self.els(
            'xpath', "//span[contains(@class, 'sequence-close close')]")
        self.assertEqual(len(close_buttons), 4)

        # Close two secondary involvement fields
        close_buttons[2].click()
        close_buttons[0].click()

        # Count the panels and fields again
        sh_selection_panels = self.els(
            'xpath',
            "//div[contains(@class, 'accordion-body in collapse')]")
        self.assertEqual(len(sh_selection_panels), 3)
        search_fields = self.els('class_name', "ui-autocomplete-input")
        self.assertEqual(len(search_fields), 3)

        # Type a stakeholder name in each of the remaining fields
        search_fields[0].send_keys(sh_names[0])
        self.el('xpath', "//a[contains(text(), '%s')]" % sh_names[0]).click()
        search_fields[1].send_keys(sh_names[1])
        self.el('xpath', "//a[contains(text(), '%s')]" % sh_names[1]).click()
        search_fields[2].send_keys(sh_names[2])
        self.el('xpath', "//a[contains(text(), '%s')]" % sh_names[2]).click()

        # Make sure the Stakeholder name was filled in the textfield
        sh_name_fields = self.els('name', '[SH] Textfield 1')
        self.assertEqual(sh_name_fields[0].get_attribute('value'), sh_names[0])
        self.assertEqual(sh_name_fields[1].get_attribute('value'), sh_names[1])
        self.assertEqual(sh_name_fields[2].get_attribute('value'), sh_names[2])

        # Remove the first secondary involvement
        close_buttons = self.els(
            'xpath', "//span[contains(@class, 'sequence-close close')]")
        close_buttons[0].click()

        # Make sure the correct one was removed
        sh_name_fields = self.els('name', '[SH] Textfield 1')
        self.assertEqual(len(sh_name_fields), 2)
        self.assertEqual(sh_name_fields[0].get_attribute('value'), sh_names[0])
        self.assertEqual(sh_name_fields[1].get_attribute('value'), sh_names[2])

        # Submit the Activity
        self.el('id', 'activityformsubmit').click()
        self.el('link_text', LINK_VIEW_DEAL).click()

        # Make sure the involvements where added correctly.
        self.find_text(sh_names[0])
        self.find_text(sh_names[2])
        inv_links = self.els('link_text', LINK_DEAL_SHOW_INVOLVEMENT)
        self.assertEqual(len(inv_links), 2)
