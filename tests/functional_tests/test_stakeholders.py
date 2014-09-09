import pytest
import uuid

from .base import LmkpFunctionalTestCase
from ..base import (
    BUTTON_SHOW_ONLY_PENDING,
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
        self.el('link_text', BUTTON_SHOW_ONLY_PENDING).click()
        self.find_text(sh_name, count=1)

        # Log out and make sure the pending Stakeholder is not visible and
        # there is no "Show only pending button
        self.logout()
        self.driver.get(sh_grid_url)
        self.find_text(sh_name, count=0)
        self.el('link_text', BUTTON_SHOW_ONLY_PENDING, inverse=True)

        # Change user, log in as "user1" and go to the grid view of
        # stakeholders
        self.login(redirect=sh_grid_url, username='user1')

        # Neither the pending Stakeholder nor the "Show only pending" button
        # are visible because user1 is not moderator in the current profile.
        self.find_text(sh_name, count=0)
        self.el('link_text', BUTTON_SHOW_ONLY_PENDING, inverse=True)

        # Change to the Laos profile
        self.change_profile(gui=True, old_profile='global', new_profile='laos')

        # Go to the grid view of Stakeholders. Check that the created
        # Stakeholder is visible, also after clicking the "Show only pending"
        # button.
        self.driver.get(sh_grid_url)
        self.find_text(sh_name, count=1)
        self.el('link_text', BUTTON_SHOW_ONLY_PENDING).click()
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
