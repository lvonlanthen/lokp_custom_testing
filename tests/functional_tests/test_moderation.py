import pytest
import uuid

from .base import (
    checkIsPending,
    createUrl,
    doCreateActivity,
    doReview,
    findTextOnPage,
    getEl,
    openItemDetailsPage,
)
from ..base import (
    BUTTON_APPROVE,
    FEEDBACK_INVOLVEMENTS_CANNOT_BE_REVIEWED,
    FEEDBACK_INVOLVEMENTS_CANNOT_BE_REVIEWED_FROM_STAKEHOLDER,
    LINK_REVIEW,
    LINK_DEAL_SHOW_INVOLVEMENT,
    TITLE_DEAL_MODERATION,
    TITLE_STAKEHOLDER_MODERATION,
)


@pytest.mark.functional
@pytest.mark.moderation
def test_approve_activity(testcase):
    """
    Test that a new Activity can be approved.
    """

    uid = doCreateActivity(testcase)
    link = createUrl('/activities/html/%s' % uid)

    # Check that it is pending and there is a moderation link
    testcase.driver.get(link)
    testcase.assertTrue(checkIsPending(testcase))
    reviewLink = testcase.driver.find_element_by_xpath("//a[contains(@href, '/activities/review/')]")
    testcase.assertIn(LINK_REVIEW, reviewLink.text)

    testcase.driver.get(reviewLink.get_attribute('href'))
    testcase.assertIn(TITLE_DEAL_MODERATION, testcase.driver.title)
    btn = testcase.driver.find_element_by_xpath("//button[contains(concat(' ', @class, ' '), ' btn-success ') and contains(text(), '%s')]" % BUTTON_APPROVE)
    btn.click()

    getEl(testcase, 'class_name', 'alert-success')

    # Make sure the Activity is not pending anymore
    testcase.driver.get(link)
    testcase.assertFalse(checkIsPending(testcase))
    
    
@pytest.mark.functional
@pytest.mark.moderation
def test_approve_activity_with_new_involvement(testcase):
    """
    Test that a new Activity with a new involvement can be approved.
    """

    aUid = doCreateActivity(testcase, createSH=True)

    # Check that the Activity cannot be reviewed because of the pending SH
    testcase.driver.get(createUrl('/activities/review/%s' % aUid))
    testcase.driver.find_element_by_xpath("//button[contains(concat(' ', @class, ' '), ' disabled ') and contains(text(), '%s')]" % BUTTON_APPROVE)
    getEl(testcase, 'class_name', 'alert-missing-mandatory-keys')

    # Make sure the Stakeholder can be reviewed and do this
    testcase.driver.find_element_by_xpath("//a[contains(@href, '/stakeholders/review/')]").click()
    testcase.assertIn(TITLE_STAKEHOLDER_MODERATION, testcase.driver.title)
    testcase.driver.find_element_by_xpath("//button[contains(concat(' ', @class, ' '), ' btn-success ') and contains(text(), '%s')]" % BUTTON_APPROVE).click()

    # Make sure there is a Success message and a notice that the Activity 
    # can now be reviewed.
    getEl(testcase, 'class_name', 'alert-success')
    testcase.assertIn('You had to review this', testcase.driver.page_source)
    testcase.driver.find_element_by_link_text('Click here to return to the Activity and review it.').click()

    # Make sure the Activity can now be reviewed.
    testcase.assertIn(TITLE_DEAL_MODERATION, testcase.driver.title)
    testcase.driver.find_element_by_xpath("//button[contains(concat(' ', @class, ' '), ' btn-success ') and contains(text(), '%s')]" % BUTTON_APPROVE).click()

    # Make sure the Activity is not pending anymore
    testcase.driver.get(createUrl('/activities/html/%s' % aUid))
    testcase.assertFalse(checkIsPending(testcase))

    # Go to Stakeholder and make sure it is not pending anymore
    testcase.driver.find_element_by_link_text(LINK_DEAL_SHOW_INVOLVEMENT).click()
    testcase.assertFalse(checkIsPending(testcase))
    
    
@pytest.mark.functional
@pytest.mark.moderation
def test_edited_stakeholders_with_involvements_can_be_approved(testcase):
    """
    Bugfix: Edited Stakeholders with an involvement could not be approved
    from Stakeholder side, thus blocking the review process.
    """

    aUid = doCreateActivity(testcase, createSH=True)

    # Review both Activity (first) and Stakeholder (second)
    testcase.driver.get(createUrl('/activities/review/%s' % aUid))
    shLink = testcase.driver.find_element_by_xpath("//a[contains(@href, '/stakeholders/review/')]").get_attribute('href')
    shUid = shLink.split('/')[len(shLink.split('/'))-1]
    testcase.driver.find_element_by_xpath("//a[contains(@href, '/stakeholders/review/')]").click()
    testcase.driver.find_element_by_xpath("//button[contains(concat(' ', @class, ' '), ' btn-success ') and contains(text(), '%s')]" % BUTTON_APPROVE).click()
    testcase.driver.find_element_by_link_text('Click here to return to the Activity and review it.').click()
    testcase.driver.implicitly_wait(10)
    testcase.driver.find_element_by_xpath("//button[contains(concat(' ', @class, ' '), ' btn-success ') and contains(text(), '%s')]" % BUTTON_APPROVE).click()

    # Go to Stakeholder and edit it
    testcase.driver.get(createUrl('/stakeholders/form/%s' % shUid))
    testcase.driver.find_element_by_xpath("//textarea[@name='[SH] Textarea 1']").send_keys('Added input')
    testcase.driver.find_element_by_id('stakeholderformsubmit').click()

    # Go to moderation of the Stakeholder, it should be approvable
    testcase.driver.get(createUrl('/stakeholders/review/%s' % shUid))
    testcase.driver.find_element_by_xpath("//button[contains(concat(' ', @class, ' '), ' btn-success ') and contains(text(), '%s')]" % BUTTON_APPROVE).click()

    # Make sure the Stakeholder was approved correctly
    getEl(testcase, 'class_name', 'alert-success')
    testcase.driver.get(createUrl('/stakeholders/html/%s' % shUid))
    testcase.assertFalse(checkIsPending(testcase))


@pytest.mark.functional
@pytest.mark.moderation
def test_show_warning_prevent_automatic_revision_of_involvements(testcase):
    """
    Test that the warning that indicates prevention of automatic revision is
    shown where it should be.
    It is shown on Activity side if the involved Stakeholder has no active
    version yet.
    It is shown on Stakeholder side if there is an involvement because these
    always have to be reviewed from Activity side.
    """

    # Create a Stakeholder with a known name.
    shName = str(uuid.uuid4())
    shValues = {
        'tf1': shName
    }
    doCreateActivity(testcase, createSH=True, shValues=shValues, noSubmit=True)

    # Create an Activity with the Stakeholder
    knownSh = [{
        'name': shName
    }]
    aUid1 = doCreateActivity(testcase, createSH=True, knownSh=knownSh)

    # Create another Activity with the same Stakeholder
    aUid2 = doCreateActivity(testcase, createSH=True, knownSh=knownSh)

    # A1v1 cannot be reviewed because of SH
    testcase.driver.get(createUrl('/activities/review/%s' % aUid1))
    shLink = testcase.driver.find_element_by_xpath("//a[contains(@href, '/stakeholders/review/')]").get_attribute('href')
    shUid = shLink.split('/')[len(shLink.split('/'))-1]
    shUid = shUid.split('?')[0]

    testcase.driver.find_element_by_xpath("//button[contains(concat(' ', @class, ' '), ' disabled ') and contains(text(), '%s')]" % BUTTON_APPROVE)
    findTextOnPage(testcase, FEEDBACK_INVOLVEMENTS_CANNOT_BE_REVIEWED)

    # A2v1 cannot be reviewed because of SH
    testcase.driver.get(createUrl('/activities/review/%s' % aUid2))
    testcase.driver.find_element_by_xpath("//button[contains(concat(' ', @class, ' '), ' disabled ') and contains(text(), '%s')]" % BUTTON_APPROVE)
    findTextOnPage(testcase, FEEDBACK_INVOLVEMENTS_CANNOT_BE_REVIEWED)

    # SHv3 cannot be reviewed because of A
    testcase.driver.get(createUrl('/stakeholders/review/%s?new=3' % shUid))
    testcase.driver.find_element_by_xpath("//button[contains(concat(' ', @class, ' '), ' disabled ') and contains(text(), '%s')]" % BUTTON_APPROVE)
    findTextOnPage(testcase, FEEDBACK_INVOLVEMENTS_CANNOT_BE_REVIEWED_FROM_STAKEHOLDER)

    # SHv1 can now be reviewed
    doReview(testcase, 'sh', shUid)

    # SHv3 can still not be reviewed because of A
    testcase.driver.get(createUrl('/stakeholders/review/%s?new=3' % shUid))
    testcase.driver.find_element_by_xpath("//button[contains(concat(' ', @class, ' '), ' disabled ') and contains(text(), '%s')]" % BUTTON_APPROVE)
    findTextOnPage(testcase, FEEDBACK_INVOLVEMENTS_CANNOT_BE_REVIEWED_FROM_STAKEHOLDER)

    # A1v1 can now be reviewed
    doReview(testcase, 'a', aUid1)

    # SHv3 can still not be reviewed because of A
    testcase.driver.get(createUrl('/stakeholders/review/%s?new=3' % shUid))
    testcase.driver.find_element_by_xpath("//button[contains(concat(' ', @class, ' '), ' disabled ') and contains(text(), '%s')]" % BUTTON_APPROVE)
    findTextOnPage(testcase, FEEDBACK_INVOLVEMENTS_CANNOT_BE_REVIEWED_FROM_STAKEHOLDER)

    # Review A2v1
    doReview(testcase, 'a', aUid2)

    # All should be active now
    openItemDetailsPage(testcase, 'activities', aUid1)
    testcase.assertFalse(checkIsPending(testcase))
    openItemDetailsPage(testcase, 'activities', aUid2)
    testcase.assertFalse(checkIsPending(testcase))
    openItemDetailsPage(testcase, 'stakeholders', shUid)
    testcase.assertFalse(checkIsPending(testcase))
        