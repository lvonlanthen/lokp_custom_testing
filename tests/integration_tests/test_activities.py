# Some of the more complicated test setups and procedures are explained
# schematically in files available in a Google Drive folder:
# https://drive.google.com/folderview?id=0B49ePOKDgdN-
# WFZXVGlCX2ZZR2M&usp=sharing

import pytest

from .base import (
    LmkpTestCase,
    get_status_from_item_json,
    get_involvements_from_item_json,
)
from .diffs import (
    get_new_diff,
    get_edit_diff,
)
from ..base import (
    STATUS_ACTIVE,
    STATUS_EDITED,
    STATUS_INACTIVE,
    STATUS_PENDING,
    TITLE_HISTORY_VIEW,
)


@pytest.mark.usefixtures('app')
@pytest.mark.integration
@pytest.mark.activities
@pytest.mark.moderation
class ActivityTests(LmkpTestCase):

    def test_setup_01(self):
        """
        For the rather complicated setup of this test, have a look at
        "Setup Test 01" in the drive folder.
        """
        self.login()
        # Create a first Stakeholder
        sh_uid1 = self.create('sh', get_new_diff(201), return_uid=True)
        # Create a second Stakeholder
        sh_uid2 = self.create('sh', get_new_diff(201), return_uid=True)
        # Create a first Activity
        a_uid1 = self.create('a', get_new_diff(101), return_uid=True)
        # Edit the Activity and add the first Stakeholder as involvement
        inv_data1 = [{
            'id': sh_uid1,
            'version': 1,
            'role': 6
        }]
        self.create('a', get_edit_diff(102, a_uid1, version=1, data=inv_data1))
        # Create a second Activity and add the second Stakeholder as
        # involvement
        inv_data2 = [{
            'id': sh_uid2,
            'version': 1,
            'role': 6
        }]
        a_uid2 = self.create(
            'a', get_new_diff(103, data=inv_data2), return_uid=True)
        # Create a third Activity and add both Stakeholders as involvement
        inv_data3 = [{
            'id': sh_uid1,
            'version': 2,
            'role': 6
        }, {
            'id': sh_uid2,
            'version': 2,
            'role': 6
        }]
        a_uid3 = self.create(
            'a', get_new_diff(103, data=inv_data3), return_uid=True)

        # Check that everything was added correctly
        res = self.read_one('a', a_uid1, 'json')
        self.assertEqual(res['total'], 2)
        self.assertEqual(STATUS_PENDING, get_status_from_item_json(res, 0))
        self.assertEqual(STATUS_EDITED, get_status_from_item_json(res, 1))
        self.assertEqual(len(get_involvements_from_item_json(res, 0)), 1)
        self.assertEqual(len(get_involvements_from_item_json(res, 1)), 0)
        res = self.read_one('a', a_uid2, 'json')
        self.assertEqual(res['total'], 1)
        self.assertEqual(STATUS_PENDING, get_status_from_item_json(res, 0))
        self.assertEqual(len(get_involvements_from_item_json(res, 0)), 1)
        res = self.read_one('a', a_uid3, 'json')
        self.assertEqual(res['total'], 1)
        self.assertEqual(STATUS_PENDING, get_status_from_item_json(res, 0))
        self.assertEqual(len(get_involvements_from_item_json(res, 0)), 2)
        res = self.read_one('sh', sh_uid1, 'json')
        self.assertEqual(res['total'], 3)
        self.assertEqual(STATUS_PENDING, get_status_from_item_json(res, 0))
        self.assertEqual(STATUS_EDITED, get_status_from_item_json(res, 1))
        self.assertEqual(STATUS_PENDING, get_status_from_item_json(res, 2))
        self.assertEqual(len(get_involvements_from_item_json(res, 0)), 2)
        self.assertEqual(len(get_involvements_from_item_json(res, 1)), 1)
        self.assertEqual(len(get_involvements_from_item_json(res, 2)), 0)
        res = self.read_one('sh', sh_uid2, 'json')
        self.assertEqual(res['total'], 3)
        self.assertEqual(STATUS_PENDING, get_status_from_item_json(res, 0))
        self.assertEqual(STATUS_EDITED, get_status_from_item_json(res, 1))
        self.assertEqual(STATUS_PENDING, get_status_from_item_json(res, 2))
        self.assertEqual(len(get_involvements_from_item_json(res, 0)), 2)
        self.assertEqual(len(get_involvements_from_item_json(res, 1)), 1)
        self.assertEqual(len(get_involvements_from_item_json(res, 2)), 0)

    def test_setup_01_review(self):
        """
        For the rather complicated setup of this test, have a look at
        "Setup Test 01" in the drive folder.
        """
        self.login()
        # Create a first Stakeholder
        sh_uid1 = self.create('sh', get_new_diff(201), return_uid=True)
        # Create a second Stakeholder
        sh_uid2 = self.create('sh', get_new_diff(201), return_uid=True)
        # Create a first Activity
        a_uid1 = self.create('a', get_new_diff(101), return_uid=True)
        # Edit the Activity and add the first Stakeholder as involvement
        inv_data1 = [{
            'id': sh_uid1,
            'version': 1,
            'role': 6
        }]
        self.create('a', get_edit_diff(102, a_uid1, version=1, data=inv_data1))
        # Create a second Activity and add the second Stakeholder as
        # involvement
        inv_data2 = [{
            'id': sh_uid2,
            'version': 1,
            'role': 6
        }]
        a_uid2 = self.create(
            'a', get_new_diff(103, data=inv_data2), return_uid=True)
        # Create a third Activity and add both Stakeholders as involvement
        inv_data3 = [{
            'id': sh_uid1,
            'version': 2,
            'role': 6
        }, {
            'id': sh_uid2,
            'version': 2,
            'role': 6
        }]
        a_uid3 = self.create(
            'a', get_new_diff(103, data=inv_data3), return_uid=True)

        # None of the Activities can be reviewed because of SH
        res = self.review('a', a_uid1, version=2)
        self.review_not_possible('a', 1, res)
        res = self.review('a', a_uid2, version=1)
        self.review_not_possible('a', 1, res)
        res = self.review('a', a_uid3, version=1)
        self.review_not_possible('a', 1, res)

        # SH1v1 can be reviewed
        self.review('sh', sh_uid1, version=1)

        # A1v2 can be reviewed
        self.review('a', a_uid1, version=2)

        # SH1v3 cannot be reviewed because of A3
        res = self.review('sh', sh_uid1, version=3)
        self.review_not_possible('sh', 1, res)

        # A3v1 can not be reviewed because of SH2
        res = self.review('a', a_uid3, version=1)
        self.review_not_possible('a', 1, res)

        # SH2v1 can be reviewed
        self.review('sh', sh_uid2, version=1)

        # A2v1 can now be reviewed
        self.review('a', a_uid2, version=1)

        # A3v1 can now be reviewed
        self.review('a', a_uid3, version=1)

        res = self.read_one('a', a_uid1, 'json')
        self.assertEqual(res['total'], 2)
        self.assertEqual(STATUS_ACTIVE, get_status_from_item_json(res, 0))
        self.assertEqual(STATUS_EDITED, get_status_from_item_json(res, 1))
        self.assertEqual(len(get_involvements_from_item_json(res, 0)), 1)
        self.assertEqual(len(get_involvements_from_item_json(res, 1)), 0)
        res = self.read_one('a', a_uid2, 'json')
        self.assertEqual(res['total'], 1)
        self.assertEqual(STATUS_ACTIVE, get_status_from_item_json(res, 0))
        self.assertEqual(len(get_involvements_from_item_json(res, 0)), 1)
        res = self.read_one('a', a_uid3, 'json')
        self.assertEqual(res['total'], 1)
        self.assertEqual(STATUS_ACTIVE, get_status_from_item_json(res, 0))
        self.assertEqual(len(get_involvements_from_item_json(res, 0)), 2)
        res = self.read_one('sh', sh_uid1, 'json')
        self.assertEqual(res['total'], 3)
        self.assertEqual(STATUS_ACTIVE, get_status_from_item_json(res, 0))
        self.assertEqual(STATUS_INACTIVE, get_status_from_item_json(res, 1))
        self.assertEqual(STATUS_INACTIVE, get_status_from_item_json(res, 2))
        self.assertEqual(len(get_involvements_from_item_json(res, 0)), 2)
        self.assertEqual(len(get_involvements_from_item_json(res, 1)), 1)
        self.assertEqual(len(get_involvements_from_item_json(res, 2)), 0)
        res = self.read_one('sh', sh_uid2, 'json')
        self.assertEqual(res['total'], 3)
        self.assertEqual(STATUS_ACTIVE, get_status_from_item_json(res, 0))
        self.assertEqual(STATUS_INACTIVE, get_status_from_item_json(res, 1))
        self.assertEqual(STATUS_INACTIVE, get_status_from_item_json(res, 2))
        self.assertEqual(len(get_involvements_from_item_json(res, 0)), 2)
        self.assertEqual(len(get_involvements_from_item_json(res, 1)), 1)
        self.assertEqual(len(get_involvements_from_item_json(res, 2)), 0)

    def test_setup_02(self):
        """
        For the rather complicated setup of this test, have a look at
        "Setup Test 02" in the drive folder.
        """
        self.login()
        # Create a first Stakeholder
        sh_uid1 = self.create('sh', get_new_diff(201), return_uid=True)
        # Create a second Stakeholder
        sh_uid2 = self.create('sh', get_new_diff(201), return_uid=True)
        # Create a first Activity
        a_uid1 = self.create('a', get_new_diff(101), return_uid=True)
        # Edit the Activity and add the first Stakeholder as involvement
        inv_data1 = [{
            'id': sh_uid1,
            'version': 1,
            'role': 6
        }]
        self.create('a', get_edit_diff(102, a_uid1, version=1, data=inv_data1))
        # Create a second Activity and add the second Stakeholder as
        # involvement
        inv_data2 = [{
            'id': sh_uid2,
            'version': 1,
            'role': 6
        }]
        a_uid2 = self.create(
            'a', get_new_diff(103, data=inv_data2), return_uid=True)
        # Create a third Activity and add both Stakeholders as involvement
        inv_data3 = [{
            'id': sh_uid1,
            'version': 2,
            'role': 6
        }, {
            'id': sh_uid2,
            'version': 2,
            'role': 6
        }]
        a_uid3 = self.create(
            'a', get_new_diff(103, data=inv_data3), return_uid=True)
        # Edit the third Activity
        self.create('a', get_edit_diff(101, a_uid3))

        # Check that everything was added correctly
        res = self.read_one('a', a_uid1, 'json')
        self.assertEqual(res['total'], 2)
        self.assertEqual(STATUS_PENDING, get_status_from_item_json(res, 0))
        self.assertEqual(STATUS_EDITED, get_status_from_item_json(res, 1))
        self.assertEqual(len(get_involvements_from_item_json(res, 0)), 1)
        self.assertEqual(len(get_involvements_from_item_json(res, 1)), 0)
        res = self.read_one('a', a_uid2, 'json')
        self.assertEqual(res['total'], 1)
        self.assertEqual(STATUS_PENDING, get_status_from_item_json(res, 0))
        self.assertEqual(len(get_involvements_from_item_json(res, 0)), 1)
        res = self.read_one('a', a_uid3, 'json')
        self.assertEqual(res['total'], 2)
        self.assertEqual(STATUS_PENDING, get_status_from_item_json(res, 0))
        self.assertEqual(STATUS_EDITED, get_status_from_item_json(res, 1))
        self.assertEqual(len(get_involvements_from_item_json(res, 0)), 2)
        self.assertEqual(len(get_involvements_from_item_json(res, 1)), 2)
        res = self.read_one('sh', sh_uid1, 'json')
        self.assertEqual(res['total'], 3)
        self.assertEqual(STATUS_PENDING, get_status_from_item_json(res, 0))
        self.assertEqual(STATUS_EDITED, get_status_from_item_json(res, 1))
        self.assertEqual(STATUS_PENDING, get_status_from_item_json(res, 2))
        self.assertEqual(len(get_involvements_from_item_json(res, 0)), 2)
        self.assertEqual(len(get_involvements_from_item_json(res, 1)), 1)
        self.assertEqual(len(get_involvements_from_item_json(res, 2)), 0)
        res = self.read_one('sh', sh_uid2, 'json')
        self.assertEqual(res['total'], 3)
        self.assertEqual(STATUS_PENDING, get_status_from_item_json(res, 0))
        self.assertEqual(STATUS_EDITED, get_status_from_item_json(res, 1))
        self.assertEqual(STATUS_PENDING, get_status_from_item_json(res, 2))
        self.assertEqual(len(get_involvements_from_item_json(res, 0)), 2)
        self.assertEqual(len(get_involvements_from_item_json(res, 1)), 1)
        self.assertEqual(len(get_involvements_from_item_json(res, 2)), 0)

    def test_setup_02_review(self):
        """
        For the rather complicated setup of this test, have a look at
        "Setup Test 02" in the drive folder.
        """
        self.login()
        # Create a first Stakeholder
        sh_uid1 = self.create('sh', get_new_diff(201), return_uid=True)
        # Create a second Stakeholder
        sh_uid2 = self.create('sh', get_new_diff(201), return_uid=True)
        # Create a first Activity
        a_uid1 = self.create('a', get_new_diff(101), return_uid=True)
        # Edit the Activity and add the first Stakeholder as involvement
        inv_data1 = [{
            'id': sh_uid1,
            'version': 1,
            'role': 6
        }]
        self.create('a', get_edit_diff(102, a_uid1, version=1, data=inv_data1))
        # Create a second Activity and add the second Stakeholder as
        # involvement
        inv_data2 = [{
            'id': sh_uid2,
            'version': 1,
            'role': 6
        }]
        a_uid2 = self.create(
            'a', get_new_diff(103, data=inv_data2), return_uid=True)
        # Create a third Activity and add both Stakeholders as involvement
        inv_data3 = [{
            'id': sh_uid1,
            'version': 2,
            'role': 6
        }, {
            'id': sh_uid2,
            'version': 2,
            'role': 6
        }]
        a_uid3 = self.create(
            'a', get_new_diff(103, data=inv_data3), return_uid=True)
        # Edit the third Activity
        self.create('a', get_edit_diff(101, a_uid3))

        # None of the Activities can be reviewed because of SH
        res = self.review('a', a_uid1, version=2)
        self.review_not_possible('a', 1, res)
        res = self.review('a', a_uid2, version=1)
        self.review_not_possible('a', 1, res)
        res = self.review('a', a_uid3, version=2)
        self.review_not_possible('a', 1, res)

        # SH1v1 can be reviewed
        self.review('sh', sh_uid1, version=1)

        # A1v2 can now be reviewed
        self.review('a', a_uid1, version=2)

        # SH2v1 can be reviewd
        self.review('sh', sh_uid2, version=1)

        # A2v1 can now be reviewed.
        self.review('a', a_uid2, version=1)

        # A3v2 can now be reviewed.
        self.review('a', a_uid3, version=2)

        res = self.read_one('a', a_uid1, 'json')
        self.assertEqual(res['total'], 2)
        self.assertEqual(STATUS_ACTIVE, get_status_from_item_json(res, 0))
        self.assertEqual(STATUS_EDITED, get_status_from_item_json(res, 1))
        self.assertEqual(len(get_involvements_from_item_json(res, 0)), 1)
        self.assertEqual(len(get_involvements_from_item_json(res, 1)), 0)
        res = self.read_one('a', a_uid2, 'json')
        self.assertEqual(res['total'], 1)
        self.assertEqual(STATUS_ACTIVE, get_status_from_item_json(res, 0))
        self.assertEqual(len(get_involvements_from_item_json(res, 0)), 1)
        res = self.read_one('a', a_uid3, 'json')
        self.assertEqual(res['total'], 2)
        self.assertEqual(STATUS_ACTIVE, get_status_from_item_json(res, 0))
        self.assertEqual(STATUS_EDITED, get_status_from_item_json(res, 1))
        self.assertEqual(len(get_involvements_from_item_json(res, 0)), 2)
        self.assertEqual(len(get_involvements_from_item_json(res, 1)), 2)
        res = self.read_one('sh', sh_uid1, 'json')
        res = self.read_one('sh', sh_uid2, 'json')
        self.assertEqual(res['total'], 3)
        self.assertEqual(STATUS_ACTIVE, get_status_from_item_json(res, 0))
        self.assertEqual(STATUS_INACTIVE, get_status_from_item_json(res, 1))
        self.assertEqual(STATUS_INACTIVE, get_status_from_item_json(res, 2))
        self.assertEqual(len(get_involvements_from_item_json(res, 0)), 2)
        self.assertEqual(len(get_involvements_from_item_json(res, 1)), 1)
        self.assertEqual(len(get_involvements_from_item_json(res, 2)), 0)
        res = self.read_one('sh', sh_uid2, 'json')
        self.assertEqual(res['total'], 3)
        self.assertEqual(STATUS_ACTIVE, get_status_from_item_json(res, 0))
        self.assertEqual(STATUS_INACTIVE, get_status_from_item_json(res, 1))
        self.assertEqual(STATUS_INACTIVE, get_status_from_item_json(res, 2))
        self.assertEqual(len(get_involvements_from_item_json(res, 0)), 2)
        self.assertEqual(len(get_involvements_from_item_json(res, 1)), 1)
        self.assertEqual(len(get_involvements_from_item_json(res, 2)), 0)


@pytest.mark.usefixtures('app')
@pytest.mark.integration
@pytest.mark.activities
@pytest.mark.moderation
class ActivityHistoryTests(LmkpTestCase):

    def test_history_view(self):
        """
        Test that a history view is available for newly created Activities.
        """
        self.login()
        uid = self.create('a', get_new_diff(101), return_uid=True)

        res = self.app.get('/activities/history/html/%s' % uid)
        self.assertEqual(res.status_int, 200)
        self.assertIn(TITLE_HISTORY_VIEW, res.body)
