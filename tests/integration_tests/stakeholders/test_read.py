import pytest

from ..base import (
    LmkpTestCase,
    get_base_url_by_item_type,
    find_key_value_in_taggroups_json,
)
from ..diffs import (
    get_new_diff,
    get_edit_diff,
)
from ...base import (
    TITLE_HISTORY_VIEW,
)


@pytest.mark.abc
@pytest.mark.read
@pytest.mark.usefixtures('app')
@pytest.mark.integration
@pytest.mark.stakeholders
class StakeholderReadManyTests(LmkpTestCase):

    def test_stakeholders_appear_in_read_many_json(self):
        self.login()

        json = self.read_many('sh', 'json')
        self.assertEqual(json['data'], [])
        self.assertEqual(json['total'], 0)

        self.create('sh', get_new_diff(201))

        json = self.read_many('sh', 'json')
        self.assertEqual(json['total'], 1)
