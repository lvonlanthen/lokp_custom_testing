import pytest
import uuid

from .base import LmkpFunctionalTestCase
from ..base import (
    BUTTON_APPROVE,
    BUTTON_DENY,
    FEEDBACK_INVOLVEMENTS_CANNOT_BE_REVIEWED,
    FEEDBACK_INVOLVEMENTS_CANNOT_BE_REVIEWED_FROM_STAKEHOLDER,
    FEEDBACK_NO_VERSION,
    LINK_REVIEW,
    LINK_DEAL_SHOW_INVOLVEMENT,
    LINK_STAKEHOLDER_SHOW_INVOLVEMENT,
    TITLE_DEAL_MODERATION,
    TITLE_STAKEHOLDER_MODERATION,
)


@pytest.mark.usefixtures('app_functional')
@pytest.mark.functional
@pytest.mark.moderation
class ModerationTests(LmkpFunctionalTestCase):

    def test_approve_activity(self):
        """
        Test that a new Activity can be approved.
        """

        uid = self.create_activity()
        link = self.url('/activities/html/%s' % uid)

        # Check that it is pending and there is a moderation link
        self.driver.get(link)
        self.assertTrue(self.check_status('pending'))
        reviewLink = self.el(
            'xpath', "//a[contains(@href, '/activities/review/')]")
        self.assertIn(LINK_REVIEW, reviewLink.text)

        self.driver.get(reviewLink.get_attribute('href'))
        self.assertIn(TITLE_DEAL_MODERATION, self.driver.title)
        btn = self.el(
            'xpath',
            "//button[contains(concat(' ', @class, ' '), ' btn-success ') and "
            "contains(text(), '%s')]" % BUTTON_APPROVE)
        btn.click()

        self.el('class_name', 'alert-success')

        # Make sure the Activity is not pending anymore
        self.driver.get(link)
        self.assertFalse(self.check_status('pending'))

    def test_reject_first_activity(self):
        uid = self.create_activity()
        self.driver.get(self.url('/activities/review/%s' % uid))

        self.assertIn(TITLE_DEAL_MODERATION, self.driver.title)
        btn = self.el(
            'xpath',
            "//button[contains(concat(' ', @class, ' '), ' btn-warning ') and "
            "contains(text(), '%s')]" % BUTTON_DENY)
        btn.click()

        self.el('class_name', 'alert-success')
        self.find_text(FEEDBACK_NO_VERSION)

    def test_reject_first_stakeholder(self):
        uid = self.create_stakeholder()
        self.driver.get(self.url('/stakeholders/review/%s' % uid))

        self.assertIn(TITLE_STAKEHOLDER_MODERATION, self.driver.title)
        btn = self.el(
            'xpath',
            "//button[contains(concat(' ', @class, ' '), ' btn-warning ') and "
            "contains(text(), '%s')]" % BUTTON_DENY)
        btn.click()

        self.el('class_name', 'alert-success')
        self.find_text(FEEDBACK_NO_VERSION)

    def test_approve_activity_with_new_involvement(self):
        """
        Test that a new Activity with a new involvement can be approved.
        """

        a_uid = self.create_activity(create_inv=True)

        # Check that the Activity cannot be reviewed because of the pending SH
        self.driver.get(self.url('/activities/review/%s' % a_uid))
        self.el(
            'xpath',
            "//button[contains(concat(' ', @class, ' '), ' disabled ') and "
            "contains(text(), '%s')]" % BUTTON_APPROVE)
        self.el('class_name', 'alert-missing-mandatory-keys')

        # Make sure the Stakeholder can be reviewed and do this
        self.el(
            'xpath', "//a[contains(@href, '/stakeholders/review/')]").click()
        self.assertIn(TITLE_STAKEHOLDER_MODERATION, self.driver.title)
        self.el(
            'xpath',
            "//button[contains(concat(' ', @class, ' '), ' btn-success ') and "
            "contains(text(), '%s')]" % BUTTON_APPROVE).click()

        # Make sure there is a Success message and a notice that the Activity
        # can now be reviewed.
        self.el('class_name', 'alert-success')
        self.assertIn('You had to review this', self.driver.page_source)
        self.el(
            'link_text',
            'Click here to return to the Activity and review it.').click()

        # Make sure the Activity can now be reviewed.
        self.assertIn(TITLE_DEAL_MODERATION, self.driver.title)
        self.el(
            'xpath',
            "//button[contains(concat(' ', @class, ' '), ' btn-success ') and "
            "contains(text(), '%s')]" % BUTTON_APPROVE).click()
        self.driver.implicitly_wait(5)

        # Make sure the Activity is not pending anymore
        self.driver.get(self.url('/activities/html/%s' % a_uid))
        self.assertFalse(self.check_status('pending'))

        # Go to Stakeholder and make sure it is not pending anymore
        self.el('link_text', LINK_DEAL_SHOW_INVOLVEMENT).click()
        self.assertFalse(self.check_status('pending'))

    def test_approve_version_with_deleted_involvement(self):
        a_uid = self.create_activity(create_inv=True)
        self.review('activities', a_uid, with_involvement=True)

        self.open_details('activities', a_uid)
        sh_link = self.el(
            'link_text', LINK_DEAL_SHOW_INVOLVEMENT).get_attribute('href')
        sh_uid = sh_link.split('/')[len(sh_link.split('/')) - 1]

        self.open_form('activities', a_uid, reset=True)
        self.el('id', 'activityformstep_3').click()
        self.el(
            'xpath',
            "//a[contains(concat(' ', @class, ' '), ' remove-involvement ')]"
        ).click()
        self.el('id', 'activityformsubmit').click()

        # The Stakeholder cannot be reviewed
        self.driver.get(self.url('/stakeholders/review/%s' % sh_uid))
        self.el(
            'xpath',
            "//button[contains(concat(' ', @class, ' '), ' disabled ') and "
            "contains(text(), '%s')]" % BUTTON_APPROVE)

        # The Activity can be reviewed
        self.review('activities', a_uid)

        self.open_details('activities', a_uid)
        self.el('link_text', LINK_DEAL_SHOW_INVOLVEMENT, inverse=True)

        self.open_details('stakeholders', sh_uid)
        self.el('link_text', LINK_STAKEHOLDER_SHOW_INVOLVEMENT, inverse=True)

    def test_edited_stakeholders_with_involvements_can_be_approved(self):
        """
        Bugfix: Edited Stakeholders with an involvement could not be approved
        from Stakeholder side, thus blocking the review process.
        """

        a_uid = self.create_activity(create_inv=True)

        # Review both Activity (second) and Stakeholder (first)
        self.driver.get(self.url('/activities/review/%s' % a_uid))
        sh_link = self.el(
            'xpath',
            "//a[contains(@href, '/stakeholders/review/')]").get_attribute(
                'href')
        sh_uid = sh_link.split('/')[len(sh_link.split('/')) - 1]
        self.el(
            'xpath', "//a[contains(@href, '/stakeholders/review/')]").click()
        self.el(
            'xpath',
            "//button[contains(concat(' ', @class, ' '), ' btn-success ') and "
            "contains(text(), '%s')]" % BUTTON_APPROVE).click()
        self.el(
            'link_text',
            'Click here to return to the Activity and review it.').click()
        self.driver.implicitly_wait(5)
        self.el(
            'xpath',
            "//button[contains(concat(' ', @class, ' '), ' btn-success ') and "
            "contains(text(), '%s')]" % BUTTON_APPROVE).click()
        # Go to Stakeholder and edit it
        self.driver.get(self.url('/stakeholders/form/%s' % sh_uid))
        self.el(
            'xpath',
            "//textarea[@name='[SH] Textarea 1']").send_keys('Added input')
        self.driver.find_element_by_id('stakeholderformsubmit').click()
        self.driver.implicitly_wait(5)

        # Go to moderation of the Stakeholder, it should be approvable
        self.driver.get(self.url('/stakeholders/review/%s' % sh_uid))
        self.el(
            'xpath',
            "//button[contains(concat(' ', @class, ' '), ' btn-success ') and "
            "contains(text(), '%s')]" % BUTTON_APPROVE).click()

        # Make sure the Stakeholder was approved correctly
        self.el('class_name', 'alert-success')
        self.driver.get(self.url('/stakeholders/html/%s' % sh_uid))
        self.assertFalse(self.check_status('pending'))

    def test_show_warning_prevent_automatic_revision_of_involvements(self):
        """
        Test that the warning that indicates prevention of automatic revision
        is shown where it should be.
        It is shown on Activity side if the involved Stakeholder has no active
        version yet.
        It is shown on Stakeholder side if there is an involvement because
        these always have to be reviewed from Activity side.
        """

        # Create a Stakeholder with a known name.
        sh_name = str(uuid.uuid4())
        sh_values = {
            'tf1': sh_name
        }
        self.create_activity(
            create_inv=True, inv_values=sh_values, no_submit=True)

        # Create an Activity with the Stakeholder
        known_sh = [{
            'name': sh_name
        }]
        a_uid_1 = self.create_activity(create_inv=True, known_inv=known_sh)

        # Create another Activity with the same Stakeholder
        a_uid_2 = self.create_activity(create_inv=True, known_inv=known_sh)

        # A1v1 cannot be reviewed because of SH
        self.driver.get(self.url('/activities/review/%s' % a_uid_1))
        sh_link = self.el(
            'xpath',
            "//a[contains(@href, '/stakeholders/review/')]").get_attribute(
                'href')
        sh_uid = sh_link.split('/')[len(sh_link.split('/')) - 1]
        sh_uid = sh_uid.split('?')[0]

        self.el(
            'xpath',
            "//button[contains(concat(' ', @class, ' '), ' disabled ') and "
            "contains(text(), '%s')]" % BUTTON_APPROVE)
        self.find_text(FEEDBACK_INVOLVEMENTS_CANNOT_BE_REVIEWED)

        # A2v1 cannot be reviewed because of SH
        self.driver.get(self.url('/activities/review/%s' % a_uid_2))
        self.el(
            'xpath',
            "//button[contains(concat(' ', @class, ' '), ' disabled ') and "
            "contains(text(), '%s')]" % BUTTON_APPROVE)
        self.find_text(FEEDBACK_INVOLVEMENTS_CANNOT_BE_REVIEWED)

        # SHv3 cannot be reviewed because of A
        self.driver.get(self.url('/stakeholders/review/%s?new=3' % sh_uid))
        self.el(
            'xpath',
            "//button[contains(concat(' ', @class, ' '), ' disabled ') and "
            "contains(text(), '%s')]" % BUTTON_APPROVE)
        self.find_text(
            FEEDBACK_INVOLVEMENTS_CANNOT_BE_REVIEWED_FROM_STAKEHOLDER)

        # SHv1 can now be reviewed
        self.review('stakeholders', sh_uid)

        # SHv3 can still not be reviewed because of A
        self.driver.get(self.url('/stakeholders/review/%s?new=3' % sh_uid))
        self.el(
            'xpath',
            "//button[contains(concat(' ', @class, ' '), ' disabled ') and "
            "contains(text(), '%s')]" % BUTTON_APPROVE)
        self.find_text(
            FEEDBACK_INVOLVEMENTS_CANNOT_BE_REVIEWED_FROM_STAKEHOLDER)

        # A1v1 can now be reviewed
        self.review('activities', a_uid_1)

        # SHv3 can still not be reviewed because of A
        self.driver.get(self.url('/stakeholders/review/%s?new=3' % sh_uid))
        self.el(
            'xpath',
            "//button[contains(concat(' ', @class, ' '), ' disabled ') and "
            "contains(text(), '%s')]" % BUTTON_APPROVE)
        self.find_text(
            FEEDBACK_INVOLVEMENTS_CANNOT_BE_REVIEWED_FROM_STAKEHOLDER)

        # Review A2v1
        self.review('activities', a_uid_2)

        # All should be active now
        self.open_details('activities', a_uid_1)
        self.assertFalse(self.check_status('pending'))
        self.open_details('activities', a_uid_2)
        self.assertFalse(self.check_status('pending'))
        self.open_details('stakeholders', sh_uid)
        self.assertFalse(self.check_status('pending'))

    def test_moderate_deleted_activity(self):
        a_uid = self.create_activity()
        self.review('activities', a_uid)
        self.open_form('activities', uid=a_uid, reset=True)
        self.el('class_name', 'formdelete').click()
        self.el('class_name', 'btn-danger').click()

        self.review('activities', a_uid)
        self.open_details('activities', a_uid)
        self.check_status('deleted')
        self.el('class_name', 'empty-details')
