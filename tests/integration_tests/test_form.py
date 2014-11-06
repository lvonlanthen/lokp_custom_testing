import pytest

from .base import (
    LmkpTestCase,
)
from .diffs import get_new_diff


@pytest.mark.usefixtures('app')
@pytest.mark.integration
@pytest.mark.form
class FormConfigTests(LmkpTestCase):

    def test_activities_thmg_show_in_details(self):
        """
        Test that the YAML configuration "showindetails" for Thematic Groups
        works for Activities.
        """
        self.login()
        uid = self.create('a', get_new_diff(104), return_uid=True)
        res = self.read_one('a', uid, 'html')
        res.mustcontain('[A] Subcategory 8')

    def test_stakeholders_thmg_show_in_details(self):
        """
        Test that the YAML configuration "showindetails" for Thematic Groups
        works for Stakeholders.
        """
        self.login()
        uid = self.create('sh', get_new_diff(203), return_uid=True)
        res = self.read_one('sh', uid, 'html')
        res.mustcontain('[SH] Subcategory 6')
