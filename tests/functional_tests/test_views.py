import pytest
import urllib

from .base import LmkpFunctionalTestCase
from ..base import (
    FILTER_MAP_EXTENT,
    FILTER_PROFILE,
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
