import pytest
import urllib

from .base import LmkpFunctionalTestCase
from ..base import (
    FILTER_MAP_EXTENT,
    FILTER_PROFILE,
    TITLE_GRID_STAKEHOLDERS,
    TITLE_GRID_ACTIVITIES,
    TITLE_NOTHING_FOUND,
)


@pytest.mark.usefixtures('app_functional')
@pytest.mark.functional
@pytest.mark.form
class ViewTests(LmkpFunctionalTestCase):

    def test_spatial_extent(self):

        bbox_empty = \
            '-8008785.1837498,11534051.373142,-7999612.7403568,11540472.083518'
        bbox_world = \
            '-18785164.06875,-13149614.848125,18785164.06875,13149614.848125'

        # Set the bounding box to the world
        self.login(self.url('/activities/html?bbox=%s' % bbox_world))
        try:
            self.el('tag_name', 'h5')
            # If there is no Activity yet, create one.
            self.create_activity()
            self.driver.get(self.url('/activities/html?bbox=%s' % bbox_world))
        except:
            pass
        filter = self.el('class_name', 'alert-info')
        self.assertIn(FILTER_MAP_EXTENT, filter.text)

        # Set the bounding box to no man's land.
        self.driver.get(self.url('/activities/html?bbox=%s' % bbox_empty))
        filter = self.el('class_name', 'alert-info')
        self.assertIn(FILTER_MAP_EXTENT, filter.text)
        empty = self.el('tag_name', 'h5')
        self.assertIn(TITLE_NOTHING_FOUND.upper(), empty.text)

        # Set the bounding box to the profile
        self.el('xpath', "//a[contains(@href, '?bbox=profile')]").click()
        filter = self.el('class_name', 'alert-info')
        self.assertIn(FILTER_PROFILE, filter.text)
        self.el('tag_name', 'h5', inverse=True)

        # Set the bounding box (in cookie) to no man's land.
        self.driver.add_cookie({
            'name': '_LOCATION_', 'value': urllib.quote(bbox_empty)})
        self.driver.get(self.url('/activities/html'))
        filter = self.el('class_name', 'alert-info')
        self.assertIn(FILTER_MAP_EXTENT, filter.text)
        empty = self.el('tag_name', 'h5')
        self.assertIn(TITLE_NOTHING_FOUND.upper(), empty.text)

    def test_stakeholder_grid(self):

        self.login(self.url('/stakeholders/html'))
        try:
            self.el('tag_name', 'tr')
        except:
            uid = self.create_stakeholder()
            self.review('stakeholders', uid)
        try:
            self.el('xpath', "//tr[contains(@class, 'pending')]")
        except:
            self.create_stakeholder()

        active_grid_tab = self.el(
            'xpath', "//ul[contains(concat(' ', @class, ' '), ' table_tabs ')]"
            "/li[contains(concat(' ', @class, ' '), ' active ')]")
        self.assertEqual(active_grid_tab.text, TITLE_GRID_STAKEHOLDERS)

        count = self.el('xpath', "//div[contains(@class, 'span4')]/strong")
        count_all = int(count.text)

        self.el('class_name', 'moderator-show-pending-right').click()

        count = self.el('xpath', "//div[contains(@class, 'span4')]/strong")
        count_pending = int(count.text)

        self.assertTrue(count_pending < count_all)

        self.el('class_name', 'moderator-show-pending-right').click()

        count = self.el('xpath', "//div[contains(@class, 'span4')]/strong")
        count_all2 = int(count.text)

        self.assertEqual(count_all, count_all2)

        sh_name = self.el('xpath', "//table/tbody/tr[1]/td[3]").text

        self.el('id', 'search').click()
        self.el('id', 'search-query').send_keys(sh_name)
        self.el('id', 'search-button').click()

        count = self.el('xpath', "//div[contains(@class, 'span4')]/strong")
        count_search = int(count.text)

        self.assertTrue(count_search <= count_all)

        self.el('class_name', 'filter-variable1')

    def test_activity_grid(self):

        self.login(self.url('/activities/html'))
        try:
            self.el('tag_name', 'tr')
        except:
            uid = self.create_activity()
            self.review('activities', uid)
        try:
            self.el('xpath', "//tr[contains(@class, 'pending')]")
        except:
            self.create_activity()

        active_grid_tab = self.el(
            'xpath', "//ul[contains(concat(' ', @class, ' '), ' table_tabs ')]"
            "/li[contains(concat(' ', @class, ' '), ' active ')]")
        self.assertEqual(active_grid_tab.text, TITLE_GRID_ACTIVITIES)

        count = self.el('xpath', "//div[contains(@class, 'span4')]/strong")
        count_all = int(count.text)

        self.el('class_name', 'moderator-show-pending-right').click()

        count = self.el('xpath', "//div[contains(@class, 'span4')]/strong")
        count_pending = int(count.text)

        self.assertTrue(count_pending < count_all)

        self.el('class_name', 'moderator-show-pending-right').click()

        count = self.el('xpath', "//div[contains(@class, 'span4')]/strong")
        count_all2 = int(count.text)

        self.assertEqual(count_all, count_all2)

        __, sh_name = self.get_existing_item('stakeholders', grid_present=True)

        self.el('id', 'search').click()
        self.el('id', 'search-query').send_keys(sh_name)
        self.el('id', 'search-button').click()

        count = self.el('xpath', "//div[contains(@class, 'span4')]/strong")
        count_search = int(count.text)

        self.assertTrue(count_search <= count_all)

        self.el('class_name', 'filter-variable1')
