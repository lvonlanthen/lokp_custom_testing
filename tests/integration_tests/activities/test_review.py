import pytest
import uuid
from pyramid import testing

from ..base import (
    LmkpTestCase,
    get_status_from_item_json,
    get_involvements_from_item_json,
)
from ..diffs import (
    get_new_diff,
    get_edit_diff,
)
from ...base import (
    FEEDBACK_LOGIN_NEEDED,
    FEEDBACK_NO_GEOMETRY_PROVIDED,
    FEEDBACK_NOT_VALID_FORMAT,
    STATUS_PENDING,
    TITLE_DEAL_EDITOR,
    get_settings,
)


@pytest.mark.usefixtures('app')
@pytest.mark.integration
@pytest.mark.activities
class ActivityReviewTests(LmkpTestCase):

    def setUp(self):
        self.request = testing.DummyRequest()
        settings = get_settings()
        self.config = testing.setUp(request=self.request, settings=settings)
        self.login()

    def tearDown(self):
        testing.tearDown()

    # def test_compare_page_is_available(self):
    #     uid = self.create('a', get_new_diff(101), return_uid=True)
    #     self.create('a', get_edit_diff(101, uid))
    #     self.create('a', get_edit_diff(101, uid, version=2))

    #     res = self.app.get('/activities/compare/%s' % uid)
    #     self.assertEqual(res.status_int, 200)

    #     print res

    #     self.fail()
