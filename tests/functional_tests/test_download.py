import pytest

from .base import LmkpFunctionalTestCase
from ..base import (
    BUTTON_DOWNLOAD,
    TITLE_DEAL_DOWNLOAD,
    TITLE_STAKEHOLDER_DOWNLOAD,
)


@pytest.mark.usefixtures('app_functional')
@pytest.mark.functional
@pytest.mark.download
class DownloadTests(LmkpFunctionalTestCase):

    def test_download(self):

        # Make sure there is a link on the grids
        self.driver.get(self.url('/activities/html'))
        self.el('xpath', "//a[contains(@href, '/activities/download')]")
        self.driver.get(self.url('/stakeholders/html'))
        self.el('xpath', "//a[contains(@href, '/stakeholders/download')]")

        # Make sure the download overview page exists
        self.driver.get(self.url('/download'))
        self.el('xpath', "//a[contains(@href, '/activities/download')]")
        self.el('xpath', "//a[contains(@href, '/stakeholders/download')]")

        # Check the functionality of the Activity download page
        self.driver.get(self.url('/activities/download'))
        h3 = self.el('tag_name', 'h3')
        self.assertIn(TITLE_DEAL_DOWNLOAD.upper(), h3.text)
        button = self.el('class_name', 'btn-primary')
        self.assertEqual(button.text, BUTTON_DOWNLOAD)

        format = self.el('id', 'output_format_overview')
        involvements = self.el('id', 'involvements_overview')
        attributes = self.el('id', 'attributes_checkboxes_overview')
        options = self.el('id', 'download_options_customize')
        self.assertEqual(format.text, 'CSV')
        self.assertEqual(involvements.text, 'Yes')
        self.assertEqual(attributes.text, 'All')

        self.assertNotIn('in', options.get_attribute('class'))
        self.el('class_name', 'accordion-toggle').click()
        self.assertIn('in', options.get_attribute('class'))

        self.el(
            'xpath',
            "//select[@name='involvements']/option[@value='none']").click()
        self.assertEqual(involvements.text, 'No')

        self.el('xpath', "//input[@value='[A] Dropdown 1']").click()
        self.el('xpath', "//input[@value='[A] Checkbox 1']").click()
        self.assertIn('[A] Textarea 1', attributes.text)
        self.assertNotIn('[A] Dropdown 1', attributes.text)

        self.el('xpath', "//input[@value='[A] Dropdown 1']").click()
        self.el('xpath', "//input[@value='[A] Checkbox 1']").click()
        self.assertEqual(attributes.text, 'All')

        self.el('class_name', 'accordion-toggle').click()
        self.assertNotIn('in', options.get_attribute('class'))

        # Check the functionality of the Stakeholder download page
        self.driver.get(self.url('/stakeholders/download'))
        h3 = self.el('tag_name', 'h3')
        self.assertIn(TITLE_STAKEHOLDER_DOWNLOAD.upper(), h3.text)
        button = self.el('class_name', 'btn-primary')
        self.assertEqual(button.text, BUTTON_DOWNLOAD)

        format = self.el('id', 'output_format_overview')
        involvements = self.el('id', 'involvements_overview')
        attributes = self.el('id', 'attributes_checkboxes_overview')
        options = self.el('id', 'download_options_customize')
        self.assertEqual(format.text, 'CSV')
        self.assertEqual(involvements.text, 'Yes')
        self.assertEqual(attributes.text, 'All')

        self.assertNotIn('in', options.get_attribute('class'))
        self.el('class_name', 'accordion-toggle').click()
        self.assertIn('in', options.get_attribute('class'))

        self.el(
            'xpath',
            "//select[@name='involvements']/option[@value='none']").click()
        self.assertEqual(involvements.text, 'No')

        self.el('xpath', "//input[@value='[SH] Textfield 1']").click()
        self.el('xpath', "//input[@value='[SH] Checkbox 1']").click()
        self.assertIn('[SH] Textarea 1', attributes.text)
        self.assertNotIn('[SH] Textfield 1', attributes.text)

        self.el('xpath', "//input[@value='[SH] Textfield 1']").click()
        self.el('xpath', "//input[@value='[SH] Checkbox 1']").click()
        self.assertEqual(attributes.text, 'All')

        self.el('class_name', 'accordion-toggle').click()
        self.assertNotIn('in', options.get_attribute('class'))
