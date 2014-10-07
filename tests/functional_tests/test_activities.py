import time
import pytest
from selenium.common.exceptions import ElementNotVisibleException

from .base import LmkpFunctionalTestCase
from ..base import (
    LINK_DEAL_SHOW_INVOLVEMENT,
    LINK_STAKEHOLDER_SHOW_INVOLVEMENT,
    LINK_VIEW_DEAL,
    TITLE_DEAL_DETAILS,
    TITLE_DEAL_EDITOR,
    TITLE_STAKEHOLDER_DETAILS,
    TITLE_STAKEHOLDER_EDITOR,
)


@pytest.mark.usefixtures('app_functional')
@pytest.mark.functional
@pytest.mark.activities
class CreateActivityTests(LmkpFunctionalTestCase):

    def test_create_activities(self):
        self.login(self.url('/activities/html'))

        # Count how many Activities there are already
        try:
            self.el('tag_name', 'h5')
            count_before = 0
        except:
            count = self.el('xpath', "//div[contains(@class, 'span4')]/strong")
            count_before = int(count.text)

        uid = self.create_activity()

        # Count how many Activities there are now
        self.driver.get(self.url('/activities/html'))
        count_after = self.el(
            'xpath', "//div[contains(@class, 'span4')]/strong")
        self.assertEqual(count_before + 1, int(count_after.text))

        # Check that a detail page is available
        self.driver.get(self.url('/activities/html/%s' % uid))
        self.assertIn(TITLE_DEAL_DETAILS, self.driver.title)
        self.assertTrue(self.check_status('pending'))

    def test_create_activity_with_new_involvement(self):
        """
        Test that a new Activity can be created with a new Involvement.
        """

        # Define some values
        a_values = {'dd1': '[A] Value A1'}
        sh_values = {'tf1': 'Specific SH'}

        # Start the Activity form
        self.create_activity(values=a_values, no_submit=True)

        # Add an involvement
        self.el('id', 'activityformstep_3').click()
        self.assertIn(TITLE_DEAL_EDITOR, self.driver.title)
        inv_button = self.els(
            'xpath', '//a[contains(@class, "accordion-toggle collapsed")]')
        for el in inv_button:
            try:
                el.click()
            except:
                pass
        time.sleep(1)
        self.el('name', 'createinvolvement_primaryinvestor').click()
        self.assertIn(TITLE_STAKEHOLDER_EDITOR, self.driver.title)

        # Create and submit a Stakeholder
        self.create_stakeholder(
            values=sh_values, form_present=True, return_uid=False)

        # Make sure we are back in Activity form and submit
        self.assertIn(TITLE_DEAL_EDITOR, self.driver.title)
        self.el('id', 'activityformsubmit').click()
        link = self.el('link_text', LINK_VIEW_DEAL).get_attribute('href')
        self.driver.get(link)
        self.assertIn(TITLE_DEAL_DETAILS, self.driver.title)
        self.check_status('pending')

        # Make sure the Stakeholder is linked and view it's details
        self.assertIn(sh_values['tf1'], self.driver.page_source)
        self.el('link_text', LINK_DEAL_SHOW_INVOLVEMENT).click()
        self.assertIn(TITLE_STAKEHOLDER_DETAILS, self.driver.title)
        self.check_status('pending')

        # Make sure the Activity is linked
        self.assertIn(a_values['dd1'], self.driver.page_source)
        self.el('link_text', LINK_STAKEHOLDER_SHOW_INVOLVEMENT)

    def test_edit_activity_with_renamed_key(self):
        """
        This is a test for a bugfix when an activity could not be edited if
        it had a key (eg. remark) which was renamed in english.
        """

        # Create a first activity
        self.login()
        self.open_form('activities', reset=True)
        self.el('class_name', 'olMapViewport').click()
        self.el(
            'xpath',
            "//select[@name='[A] Dropdown 1']/option[@value='[A] Value A1']").\
            click()
        self.el('xpath', "//input[@name='[A] Textfield 1']").send_keys('foo')
        self.el('id', 'activityformsubmit').click()

        link = self.el('link_text', LINK_VIEW_DEAL).get_attribute('href')
        uid = link.split('/')[len(link.split('/')) - 1]

        # Edit it
        self.driver.get(self.url('/activities/form/%s' % uid))
        field = self.el('xpath', "//input[@name='[A] Textfield 1']")
        field.clear()
        field.send_keys('bar, not foo')
        self.el('id', 'activityformsubmit').click()

        self.el('link_text', LINK_VIEW_DEAL).click()
        self.assertIn('bar, not foo', self.driver.page_source)

    def test_edit_activity_add_involvement(self):
        a_uid = self.create_activity()
        self.review('activities', a_uid)

        self.open_form('activities', a_uid, reset=True)
        self.el(
            'xpath', "//select[@name='[A] Dropdown 1']/option[@value='[A] "
            "Value A3']").click()
        self.el('id', 'activityformstep_3').click()
        inv_button = self.els('class_name', 'accordion-toggle')
        btn = inv_button[0]
        btn.click()
        time.sleep(1)
        self.el('name', 'createinvolvement_primaryinvestor').click()
        self.create_stakeholder(
            values={'tf1': 'New Stakeholder'}, form_present=True,
            return_uid=False)

        # Make sure the Stakeholder was created and added as involvement
        self.el('class_name', 'alert-success')
        invs = self.els('name', '[SH] Textfield 1')
        self.assertEqual(invs[0].get_attribute('value'), 'New Stakeholder')

        # Make sure the other values of the Activity are still there
        self.el('id', 'activityformstep_1').click()
        self.assertEqual(
            self.el('name', '[A] Dropdown 1').get_attribute('value'),
            '[A] Value A3')

        self.el('id', 'activityformsubmit').click()
        self.el('link_text', LINK_VIEW_DEAL).click()

        self.find_text('[A] Value A3')
        inv_links = self.els('link_text', LINK_DEAL_SHOW_INVOLVEMENT)
        self.assertEqual(len(inv_links), 1)
        self.find_text('New Stakeholder')

    def test_delete_activity(self):
        self.open_form('activities', reset=True)
        self.el('class_name', 'formdelete', inverse=True)
        a_uid = self.create_activity()
        self.review('activities', a_uid)

        self.open_form('activities', uid=a_uid, reset=True)

        # Deselect Dropdown value to make sure the item can be deleted
        # without mandatory key
        self.el(
            'xpath',
            "//select[@name='[A] Dropdown 1']/option[@value='']").click()

        delete_button = self.el('class_name', 'formdelete')

        confirm_button = self.el('class_name', 'btn-danger')
        with self.assertRaises(ElementNotVisibleException):
            confirm_button.click()

        delete_button.click()
        with self.assertRaises(ElementNotVisibleException):
            delete_button.click()

        cancel_button = self.el('id', 'delete-confirm-cancel')
        cancel_button.click()

        with self.assertRaises(ElementNotVisibleException):
            confirm_button.click()

        delete_button.click()
        confirm_button.click()

        self.el('link_text', LINK_VIEW_DEAL).click()
        self.assertIn(TITLE_DEAL_DETAILS, self.driver.title)
        self.assertTrue(self.check_status('pending'))

        self.el('class_name', 'empty-details')
        self.el('class_name', 'map-form-controls', inverse=True)


    # def test_involvement_role_handling(self):
    #     a_uid = self.create_activity(create_inv=True)
    #     self.review('activities', a_uid, with_involvement=True)

    #     self.open_form('activities', a_uid, reset=True)
    #     self.el(
    #         'xpath', "//select[@name='[A] Dropdown 1']/option[@value='[A] "
    #         "Value A3']").click()
    #     self.el('id', 'activityformstep_3').click()
    #     self.el('id', 'activityformsubmit').click()

    #     self.el('link_text', LINK_VIEW_DEAL).click()

    #     self.assertIn(TITLE_DEAL_DETAILS, self.driver.title)
    #     self.assertTrue(self.check_status('pending'))
    #     inv_links = self.els('link_text', LINK_DEAL_SHOW_INVOLVEMENT)
    #     self.assertEqual(len(inv_links), 1)
    #     inv_links[0].click()

    #     self.assertIn(TITLE_STAKEHOLDER_DETAILS, self.driver.title)
    #     inv_links = self.els('link_text', LINK_STAKEHOLDER_SHOW_INVOLVEMENT)
    #     self.assertEqual(len(inv_links), 1)
