import time
import pytest

from .base import (
    checkIsPending,
    createUrl,
    doCreateActivity,
    doCreateStakeholder,
    doLogin,
    getEl,
    openItemFormPage
)
from ..base import (
    LINK_DEAL_SHOW_INVOLVEMENT,
    LINK_STAKEHOLDER_SHOW_INVOLVEMENT,
    LINK_VIEW_DEAL,
    TEXT_PENDING_VERSION,
    TITLE_DEAL_DETAILS,
    TITLE_DEAL_EDITOR,
    TITLE_STAKEHOLDER_DETAILS,
    TITLE_STAKEHOLDER_EDITOR,
)


@pytest.mark.functional
@pytest.mark.activities
def test_create_activity(testcase):
    """
    Test that a new Activity can be created.
    """

    # Count how many Activities there are already
    doLogin(testcase, createUrl('/activities/html'))

    try:
        getEl(testcase, 'tag_name', 'h5')
        countBefore = 0
    except:
        countBefore = testcase.driver.find_element_by_xpath(
            "//div[contains(@class, 'span4')]/strong")
        countBefore = int(countBefore.text)

    uid = doCreateActivity(testcase)

    # Count how many Activities there are now
    testcase.driver.get(createUrl('/activities/html'))
    countAfter = testcase.driver.find_element_by_xpath(
        "//div[contains(@class, 'span4')]/strong")
    countAfter = int(countAfter.text)
    testcase.assertEqual(countBefore + 1, countAfter)

    # Check that a detail page is available
    testcase.driver.get(createUrl('/activities/html/%s' % uid))
    testcase.assertIn(TITLE_DEAL_DETAILS, testcase.driver.title)
    testcase.assertTrue(checkIsPending(testcase))


@pytest.mark.functional
@pytest.mark.activities
def test_create_activity_with_new_involvement(testcase):
    """
    Test that a new Activity can be created with a new Involvement.
    """

    # Define some values
    aType = '[A] Value A1'
    shName = 'Specific SH'

    # Start the Activity form
    doCreateActivity(testcase, dd1=aType, noSubmit=True)

    # Add an involvement
    testcase.driver.find_element_by_id('activityformstep_3').click()
    testcase.assertIn(TITLE_DEAL_EDITOR, testcase.driver.title)
    shbtn = testcase.driver.find_elements_by_xpath(
        '//a[contains(@class, "accordion-toggle collapsed")]')
    for el in shbtn:
        try:
            el.click()
        except:
            pass
    time.sleep(1)
    testcase.driver.find_element_by_name(
        'createinvolvement_primaryinvestor').click()
    testcase.assertIn(TITLE_STAKEHOLDER_EDITOR, testcase.driver.title)

    # Create and submit a Stakeholder
    doCreateStakeholder(testcase, tf1=shName)

    # Make sure we are back in Activity form and submit
    testcase.assertIn(TITLE_DEAL_EDITOR, testcase.driver.title)
    testcase.driver.find_element_by_id('activityformsubmit').click()
    link = testcase.driver.find_element_by_link_text(
        LINK_VIEW_DEAL).get_attribute('href')
    testcase.driver.get(link)
    testcase.assertIn(TITLE_DEAL_DETAILS, testcase.driver.title)
    pending = testcase.driver.find_element_by_tag_name('h4').text
    testcase.assertIn(TEXT_PENDING_VERSION, pending)

    # Make sure the Stakeholder is linked and view it's details
    testcase.assertIn(shName, testcase.driver.page_source)
    testcase.driver.find_element_by_link_text(
        LINK_DEAL_SHOW_INVOLVEMENT).click()
    testcase.assertIn(TITLE_STAKEHOLDER_DETAILS, testcase.driver.title)
    pending = testcase.driver.find_element_by_tag_name('h4').text
    testcase.assertIn(TEXT_PENDING_VERSION, pending)

    # Make sure the Activity is linked
    testcase.assertIn(aType, testcase.driver.page_source)
    getEl(testcase, 'link_text', LINK_STAKEHOLDER_SHOW_INVOLVEMENT)

#    def test_create_activity_with_existing_involvement(self):
#        """
#        Test that a new Activity can be created with an existing Stakeholder
#        """
#
#        aUid = doCreateActivity(self, createSH=True)
#
#        doReview(driver, 'a', aUid, withInv=True)


@pytest.mark.functional
@pytest.mark.activities
def test_edit_activity_with_renamed_key(testcase):
    """
    This is a test for a bugfix when an activity could not be edited if
    it had a key (eg. remark) which was renamed in english.
    """

    # Create a first activity
    doLogin(testcase)
    openItemFormPage(testcase, 'activities', reset=True)
    testcase.driver.find_element_by_class_name('olMapViewport').click()
    testcase.driver.find_element_by_xpath(
        "//select[@name='[A] Dropdown 1']/option[@value='[A] Value A1']").\
        click()
    testcase.driver.find_element_by_xpath(
        "//input[@name='[A] Textfield 1']").send_keys('foo')
    testcase.driver.find_element_by_id('activityformsubmit').click()

    link = testcase.driver.find_element_by_link_text(
        LINK_VIEW_DEAL).get_attribute('href')
    uid = link.split('/')[len(link.split('/'))-1]

    # Edit it
    testcase.driver.get(createUrl('/activities/form/%s' % uid))
    field = testcase.driver.find_element_by_xpath(
        "//input[@name='[A] Textfield 1']")
    field.clear()
    field.send_keys('bar, not foo')
    testcase.driver.find_element_by_id('activityformsubmit').click()

    testcase.driver.find_element_by_link_text(LINK_VIEW_DEAL).click()
    testcase.assertIn('bar, not foo', testcase.driver.page_source)
