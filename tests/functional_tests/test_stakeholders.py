import pytest
import uuid

from .base import (
    createUrl,
    doChangeProfile,
    doCreateActivity,
    doLogin,
    findTextOnPage,
    getEl,
)
from ..base import (
    BUTTON_SHOW_ONLY_PENDING,
)


@pytest.mark.functional
@pytest.mark.stakeholders
def test_show_pending_stakeholders(testcase):
    """
    Test that pending Stakeholders are visible to moderators, even if they did
    not create the Stakeholders themselves.
    """

    shGridUrl = createUrl('/stakeholders/html')

    # Create a Stakeholder as user "admin"
    shName = str(uuid.uuid4())
    shValues = {
        'tf1': shName
    }
    doCreateActivity(testcase, createSH=True, shValues=shValues, noSubmit=True)

    # Go to the grid view of Stakeholders. Check that the created Stakeholder
    # is visible, also after clicking the "Show only pending" button.
    testcase.driver.get(shGridUrl)
    findTextOnPage(testcase, shName, count=1)
    getEl(testcase, 'link_text', BUTTON_SHOW_ONLY_PENDING).click()
    findTextOnPage(testcase, shName, count=1)

    # Log out and make sure the pending Stakeholder is not visible and there is
    # no "Show only pending button
    testcase.driver.get(createUrl('/logout'))
    testcase.driver.get(shGridUrl)
    findTextOnPage(testcase, shName, count=0)
    getEl(testcase, 'link_text', BUTTON_SHOW_ONLY_PENDING, inverse=True)

    # Change user, log in as "user1" and go to the grid view of stakeholders
    doLogin(testcase, redirect=shGridUrl, username='user1')

    # Neither the pending Stakeholder nor the "Show only pending" button are
    # visible because user1 is not moderator in the current profile.
    findTextOnPage(testcase, shName, count=0)
    getEl(testcase, 'link_text', BUTTON_SHOW_ONLY_PENDING, inverse=True)

    # Change to the Laos profile
    doChangeProfile(testcase, gui=True, old='global', new='laos')

    # Go to the grid view of Stakeholders. Check that the created Stakeholder
    # is visible, also after clicking the "Show only pending" button.
    testcase.driver.get(shGridUrl)
    findTextOnPage(testcase, shName, count=1)
    getEl(testcase, 'link_text', BUTTON_SHOW_ONLY_PENDING).click()
    findTextOnPage(testcase, shName, count=1)

    # In the Activity form when adding an Involvement, the Stakeholder should
    # because visible too
    knownSh = [{
        'name': shName
    }]
    doCreateActivity(testcase, createSH=True, knownSh=knownSh, noSubmit=True)

    shField = getEl(testcase, 'name', '[SH] Textfield 1')
    testcase.assertEqual(shField.get_attribute('value'), shName)
