import time
import pytest
import uuid
from selenium.common.exceptions import ElementNotVisibleException

from .base import LmkpFunctionalTestCase
from ..base import (
    LINK_VIEW_STAKEHOLDER,
    TITLE_STAKEHOLDER_DETAILS,
)


@pytest.mark.usefixtures('app_functional')
@pytest.mark.functional
@pytest.mark.stakeholders
class StakeholderTests(LmkpFunctionalTestCase):

    def test_show_pending_stakeholders(self):
        """
        Test that pending Stakeholders are visible to moderators, even if they
        did not create the Stakeholders themselves.
        """

        sh_grid_url = self.url('/stakeholders/html')

        # Create a Stakeholder as user "admin"
        sh_name = str(uuid.uuid4())
        sh_values = {
            'tf1': sh_name
        }
        self.create_stakeholder(values=sh_values)

        # Go to the grid view of Stakeholders. Check that the created
        # Stakeholder is visible, also after clicking the "Show only pending"
        # button.
        self.driver.get(sh_grid_url)
        self.find_text(sh_name, count=1)
        self.el('class_name', 'moderator-show-pending-right').click()
        self.find_text(sh_name, count=1)

        # Log out and make sure the pending Stakeholder is not visible and
        # there is no "Show only pending button
        self.logout()
        self.driver.get(sh_grid_url)
        self.find_text(sh_name, count=0)
        self.el('class_name', 'moderator-show-pending-right', inverse=True)

        # Change user, log in as "user1" and go to the grid view of
        # stakeholders
        self.login(redirect=sh_grid_url, username='user1')

        # Neither the pending Stakeholder nor the "Show only pending" button
        # are visible because user1 is not moderator in the current profile.
        self.find_text(sh_name, count=0)
        self.el('class_name', 'moderator-show-pending-right', inverse=True)

        # Change to the Laos profile
        self.change_profile(gui=True, old_profile='global', new_profile='laos')

        # Go to the grid view of Stakeholders. Check that the created
        # Stakeholder is visible, also after clicking the "Show only pending"
        # button.
        self.driver.get(sh_grid_url)
        self.find_text(sh_name, count=1)
        self.el('class_name', 'moderator-show-pending-right').click()
        self.find_text(sh_name, count=1)

        # In the Activity form when adding an Involvement, the Stakeholder
        # should because visible too
        known_sh = [{
            'name': sh_name
        }]
        self.create_activity(
            create_inv=True, known_inv=known_sh, no_submit=True)

        sh_field = self.el('name', '[SH] Textfield 1')
        self.assertEqual(sh_field.get_attribute('value'), sh_name)

    def test_delete_stakeholder(self):

        # Open the details of an existing Stakeholder
        uid, name = self.get_existing_item('stakeholders')
        self.open_details('stakeholders', uid)

        # Get the buttons
        delete_button = self.el('link_text', 'Delete this Stakeholder')
        confirm_button = self.el('class_name', 'btn-danger')

        # Confirm delete cannot be clicked
        with self.assertRaises(ElementNotVisibleException):
            confirm_button.click()

        # Clicking the button to delete triggers the confirm panel
        delete_button.click()
        time.sleep(0.5)
        delete_button.click()
        time.sleep(0.5)
        with self.assertRaises(ElementNotVisibleException):
            confirm_button.click()

        # Clicking the cancel button triggers the confirm panel
        delete_button.click()
        time.sleep(0.5)
        cancel_button = self.el('class_name', 'delete-confirm-cancel')
        cancel_button.click()
        time.sleep(0.5)
        with self.assertRaises(ElementNotVisibleException):
            confirm_button.click()

        # Delete and check it succeeds
        delete_button.click()
        confirm_button.click()

        self.el('link_text', LINK_VIEW_STAKEHOLDER).click()
        self.assertIn(TITLE_STAKEHOLDER_DETAILS, self.driver.title)

        # The Stakeholder is pending, has no attributes
        self.assertTrue(self.check_status('pending'))
        self.el('class_name', 'empty-details')

        # The delete button cannot be clicked again.
        self.el('link_text', 'Delete this Stakeholder', inverse=True)
