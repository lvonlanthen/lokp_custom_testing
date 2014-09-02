import pytest
from pyramid import testing
from mock import patch

from lmkp.models.database_objects import Activity
from lmkp.views import download
from ..base import (
    LmkpTestCase,
)
from ..diffs import (
    get_new_diff,
)
from ...base import get_settings


@pytest.mark.download
@pytest.mark.usefixtures('app')
class ActivityDownloadToTableTest(LmkpTestCase):

    def setUp(self):
        self.request = testing.DummyRequest()
        settings = get_settings()
        self.config = testing.setUp(request=self.request, settings=settings)

    def tearDown(self):
        testing.tearDown()

    @patch('lmkp.views.download.activity_protocol.read_many')
    def test_to_table_calls_activity_protocol_read_many(self, mock_read_many):
        download.to_table(self.request)
        mock_read_many.assert_called_once_with(self.request, public=True)

    @pytest.mark.test
    def test_to_table_preserves_order_inside_taggroup(self):
        header, __ = download.to_table(self.request)
        self.assertEqual(len(header), 17)
        index_mainkey = header.index('[A] Dropdown 1')
        self.assertEqual(header.index('[A] Textarea 1'), index_mainkey + 1)

    def test_to_table_preserves_order_of_form(self):
        header, __ = download.to_table(self.request)
        self.assertEqual(len(header), 17)
        index_dropdown_1 = header.index('[A] Dropdown 1')
        index_checkbox_1 = header.index('[A] Checkbox 1')
        index_intdropdown_2 = header.index('[A] Integerdropdown 1')
        self.assertTrue(index_dropdown_1 < index_checkbox_1)
        self.assertTrue(index_checkbox_1 < index_intdropdown_2)

    def test_to_table_can_handle_empty_result(self):
        header, rows = download.to_table(self.request)
        self.assertEqual(len(header), 17)
        self.assertEqual(len(rows), 0)

    def test_to_table_does_not_contain_keys_not_in_form(self):
        header, __ = download.to_table(self.request)
        self.assertNotIn('[A] Numberfield 3', header)

    def test_to_table_returns_one_row(self):
        self.login()
        uid = self.create('a', get_new_diff(101), return_uid=True)
        self.review('a', uid)
        header, rows = download.to_table(self.request)
        self.assertEqual(len(header), 17)
        self.assertEqual(len(rows), 1)
        self.assertEqual(rows[0][header.index('id')], uid)
        self.assertEqual(
            rows[0][header.index('[A] Dropdown 1')], '[A] Value A1')
        self.assertEqual(
            rows[0][header.index('[A] Numberfield 1')], '123.45')

    def test_to_table_returns_multiple_rows(self):
        self.login()
        for i in range(3):
            uid = self.create('a', get_new_diff(101), return_uid=True)
            self.review('a', uid)
        header, rows = download.to_table(self.request)
        self.assertEqual(len(header), 17)
        self.assertEqual(len(rows), 3)
        for r in rows:
            self.assertEqual(len(r), 17)
            self.assertEqual(
                r[header.index('[A] Dropdown 1')], '[A] Value A1')
            self.assertEqual(
                r[header.index('[A] Numberfield 1')], '123.45')

    def test_to_table_with_checkboxes(self):
        self.login()
        self.create('a', get_new_diff(102))
        # The Activity cannot be reviewed because it is not complete. We
        # can however set it "active" directly in the database
        self.db_session.query(Activity).update({'fk_status': 2})
        header, rows = download.to_table(self.request)
        self.assertEqual(len(header), 18)
        self.assertEqual(len(rows), 1)
        row = rows[0]
        self.assertEqual(len(header), len(row))
        self.assertEqual(row[header.index('[A] Checkbox 1_1')], '[A] Value D2')
        self.assertEqual(row[header.index('[A] Checkbox 1_2')], '[A] Value D3')

    def test_to_table_with_repeating_taggroup(self):
        self.login()
        uid = self.create('a', get_new_diff(107), return_uid=True)
        self.review('a', uid)
        header, rows = download.to_table(self.request)
        self.assertEqual(len(header), 19)
        self.assertEqual(len(rows), 1)
        row = rows[0]
        self.assertEqual(len(header), len(row))
        self.assertEqual(row[header.index('[A] Numberfield 2_1')], '1.23')
        self.assertEqual(row[header.index('[A] Integerfield 1_1')], '159')
        self.assertEqual(row[header.index('[A] Numberfield 2_2')], '2.34')
        self.assertEqual(row[header.index('[A] Integerfield 1_2')], '123')

    def test_to_table_different_activities(self):
        self.login()
        uid = self.create('a', get_new_diff(101), return_uid=True)
        self.review('a', uid)
        uid = self.create('a', get_new_diff(104), return_uid=True)
        self.review('a', uid)
        uid = self.create('a', get_new_diff(106), return_uid=True)
        self.review('a', uid)
        header, rows = download.to_table(self.request)
        self.assertEqual(len(header), 20)
        self.assertEqual(len(rows), 3)
        for r in rows:
            self.assertEqual(len(header), len(r))

    def test_to_table_with_involvements(self):
        self.login()
        sh_uid = self.create('sh', get_new_diff(201), return_uid=True)
        self.review('sh', sh_uid)
        inv = [{
            'id': sh_uid,
            'version': 1,
            'role': 6
        }]
        a_uid = self.create('a', get_new_diff(103, data=inv), return_uid=True)
        self.review('a', a_uid)
        header, rows = download.to_table(self.request)
        self.assertEqual(len(header), 20)
        self.assertEqual(len(rows), 1)
        row = rows[0]
        self.assertEqual(len(row), len(header))
        self.assertTrue(header.index(
            '[A] Integerdropdown 1') < header.index('inv_role_1'))
        self.assertEqual(row[header.index('[SH] Textfield 1_1')], 'asdf')
        self.assertEqual(row[header.index('inv_role_1')], 'Stakeholder Role 6')
        self.assertEqual(row[header.index('inv_id_1')], sh_uid)

    def test_to_table_with_mixed_involvements(self):
        self.login()
        sh_uid_1 = self.create('sh', get_new_diff(201), return_uid=True)
        self.review('sh', sh_uid_1)
        sh_uid_2 = self.create('sh', get_new_diff(201), return_uid=True)
        self.review('sh', sh_uid_2)
        sh_uid_3 = self.create('sh', get_new_diff(203), return_uid=True)
        self.review('sh', sh_uid_3)
        inv_1 = [{
            'id': sh_uid_2,
            'version': 1,
            'role': 3
        }]
        inv_2 = [{
            'id': sh_uid_1,
            'version': 1,
            'role': 6
        }, {
            'id': sh_uid_3,
            'version': 1,
            'role': 4
        }]
        a_uid_1 = self.create(
            'a', get_new_diff(103, data=inv_1), return_uid=True)
        self.review('a', a_uid_1)
        a_uid_2 = self.create(
            'a', get_new_diff(101), return_uid=True)
        self.review('a', a_uid_2)
        a_uid_3 = self.create(
            'a', get_new_diff(103, data=inv_2), return_uid=True)
        self.review('a', a_uid_3)
        header, rows = download.to_table(self.request)
        self.assertEqual(len(header), 23)
        self.assertEqual(len(rows), 3)
        for row in rows:
            self.assertEqual(len(row), len(header))

    def test_to_table_translation(self):
        self.login()
        sh_uid = self.create('sh', get_new_diff(201), return_uid=True)
        self.review('sh', sh_uid)
        inv = [{
            'id': sh_uid,
            'version': 1,
            'role': 6
        }]
        a_uid = self.create('a', get_new_diff(103, data=inv), return_uid=True)
        self.review('a', a_uid)
        self.request.params = {'_LOCALE_': 'es'}
        header, rows = download.to_table(self.request)
        self.assertEqual(len(header), 20)
        self.assertEqual(len(rows), 1)
        row = rows[0]
        self.assertEqual(
            row[header.index('[A-T] Dropdown 1')], '[A-T] Value A1')
        self.assertEqual(
            row[header.index('[SH-T] Textfield 1_1')], 'asdf')
