import pytest
from pyramid import testing
from mock import patch, Mock

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
        self.header_length = 18

    def tearDown(self):
        testing.tearDown()

    @patch('lmkp.views.download.activity_protocol.read_many')
    def test_to_table_calls_activity_protocol_read_many(self, mock_read_many):
        download.to_flat_table(self.request, 'activities')
        mock_read_many.assert_called_once_with(
            self.request, public=True, translate=False)

    def test_to_flat_table_preserves_order_inside_taggroup(self):
        header, __ = download.to_flat_table(self.request, 'activities')
        self.assertEqual(len(header), self.header_length)
        index_mainkey = header.index('[A] Dropdown 1_[A] Dropdown 1')
        self.assertEqual(
            header.index('[A] Dropdown 1_[A] Textarea 1'), index_mainkey + 1)

    def test_to_flat_table_preserves_order_of_form(self):
        header, __ = download.to_flat_table(self.request, 'activities')
        self.assertEqual(len(header), self.header_length)
        index_dropdown_1 = header.index('[A] Dropdown 1_[A] Dropdown 1')
        index_checkbox_1 = header.index('[A] Checkbox 1_1')
        index_intdropdown_2 = header.index('[A] Integerdropdown 1')
        self.assertTrue(index_dropdown_1 < index_checkbox_1)
        self.assertTrue(index_checkbox_1 < index_intdropdown_2)

    def test_to_flat_table_does_not_contain_keys_not_in_form(self):
        header, __ = download.to_flat_table(self.request, 'activities')
        self.assertNotIn('[A] Numberfield 3', header)

    def test_to_flat_table_can_handle_empty_result(self):
        header, rows = download.to_flat_table(self.request, 'activities')
        self.assertEqual(len(header), self.header_length)
        self.assertEqual(len(rows), 0)

    def test_to_flat_table_returns_one_row(self):
        self.login()
        uid = self.create('a', get_new_diff(101), return_uid=True)
        self.review('a', uid)
        header, rows = download.to_flat_table(self.request, 'activities')
        self.assertEqual(len(header), self.header_length)
        self.assertEqual(len(rows), 1)
        self.assertEqual(rows[0][header.index('id')], uid)
        self.assertEqual(
            rows[0][header.index('[A] Dropdown 1_[A] Dropdown 1')],
            '[A] Value A1')
        self.assertEqual(
            rows[0][header.index('[A] Numberfield 1')], '123.45')

    def test_to_flat_table_returns_multiple_rows(self):
        self.login()
        for i in range(3):
            uid = self.create('a', get_new_diff(101), return_uid=True)
            self.review('a', uid)
        header, rows = download.to_flat_table(self.request, 'activities')
        self.assertEqual(len(header), self.header_length)
        self.assertEqual(len(rows), 3)
        for r in rows:
            self.assertEqual(len(r), self.header_length)
            self.assertEqual(
                r[header.index('[A] Dropdown 1_[A] Dropdown 1')],
                '[A] Value A1')
            self.assertEqual(
                r[header.index('[A] Numberfield 1')], '123.45')

    def test_to_flat_table_with_checkboxes(self):
        self.login()
        self.create('a', get_new_diff(102))
        # The Activity cannot be reviewed because it is not complete. We
        # can however set it "active" directly in the database
        self.db_session.query(Activity).update({'fk_status': 2})
        header, rows = download.to_flat_table(self.request, 'activities')
        self.assertEqual(len(header), self.header_length + 1)
        self.assertEqual(len(rows), 1)
        row = rows[0]
        self.assertEqual(len(header), len(row))
        self.assertEqual(row[header.index('[A] Checkbox 1_1')], '[A] Value D2')
        self.assertEqual(row[header.index('[A] Checkbox 1_2')], '[A] Value D3')

    def test_to_flat_table_with_repeating_taggroup(self):
        self.login()
        uid = self.create('a', get_new_diff(107), return_uid=True)
        self.review('a', uid)
        header, rows = download.to_flat_table(self.request, 'activities')
        self.assertEqual(len(header), self.header_length + 2)
        self.assertEqual(len(rows), 1)
        row = rows[0]
        self.assertEqual(len(header), len(row))
        self.assertEqual(
            row[header.index('[A] Numberfield 2_[A] Numberfield 2_1')], '1.23')
        self.assertEqual(
            row[header.index('[A] Numberfield 2_[A] Integerfield 1_1')], '159')
        self.assertEqual(
            row[header.index('[A] Numberfield 2_[A] Numberfield 2_2')], '2.34')
        self.assertEqual(
            row[header.index('[A] Numberfield 2_[A] Integerfield 1_2')], '123')

    def test_to_flat_table_files(self):
        self.login()
        uid = self.create('a', get_new_diff(109), return_uid=True)
        self.review('a', uid)
        request = self.request
        request.route_url = Mock()
        request.route_url.return_value = 'file_url'
        header, rows = download.to_flat_table(self.request, 'activities')
        self.assertEqual(len(header), self.header_length)
        self.assertEqual(len(rows), 1)
        row = rows[0]
        self.assertEqual(
            row[header.index('[A] Dropdown 2_[A] Filefield 1_1')],
            'filename1.jpg (file_url)|filename2.pdf (file_url)')

    def test_to_flat_table_different_activities(self):
        self.login()
        uid = self.create('a', get_new_diff(101), return_uid=True)
        self.review('a', uid)
        uid = self.create('a', get_new_diff(104), return_uid=True)
        self.review('a', uid)
        uid = self.create('a', get_new_diff(106), return_uid=True)
        self.review('a', uid)
        header, rows = download.to_flat_table(self.request, 'activities')
        self.assertEqual(len(header), self.header_length + 3)
        self.assertEqual(len(rows), 3)
        for r in rows:
            self.assertEqual(len(header), len(r))

    def test_to_flat_table_filters_columns(self):
        self.login()
        uid_1 = self.create('a', get_new_diff(101), return_uid=True)
        self.review('a', uid_1)
        uid_2 = self.create('a', get_new_diff(107), return_uid=True)
        self.review('a', uid_2)
        columns = ['[A] Dropdown 1', '[A] Integerfield 1']
        header, rows = download.to_flat_table(
            self.request, 'activities', columns=columns)
        self.assertEqual(len(header), 7)
        self.assertIn('[A] Dropdown 1_[A] Dropdown 1', header)
        self.assertIn('[A] Numberfield 2_[A] Integerfield 1_1', header)
        self.assertIn('[A] Numberfield 2_[A] Integerfield 1_2', header)
        self.assertNotIn('[A] Numberfield 2_[A] Numberfield 2', header)
        self.assertEqual(len(rows), 2)
        row_uid_1 = rows[1]
        self.assertEqual(len(row_uid_1), len(header))
        self.assertEqual(row_uid_1[header.index('id')], uid_1)
        self.assertEqual(
            row_uid_1[header.index('[A] Dropdown 1_[A] Dropdown 1')],
            '[A] Value A1')
        self.assertIsNone(
            row_uid_1[header.index('[A] Numberfield 2_[A] Integerfield 1_1')])
        self.assertIsNone(
            row_uid_1[header.index('[A] Numberfield 2_[A] Integerfield 1_2')])
        row_uid_2 = rows[0]
        self.assertEqual(len(row_uid_2), len(header))
        self.assertEqual(row_uid_2[header.index('id')], uid_2)
        self.assertEqual(
            row_uid_2[header.index('[A] Dropdown 1_[A] Dropdown 1')],
            '[A] Value A1')
        self.assertEqual(
            row_uid_2[header.index('[A] Numberfield 2_[A] Integerfield 1_1')],
            '159')
        self.assertEqual(
            row_uid_2[header.index('[A] Numberfield 2_[A] Integerfield 1_2')],
            '123')

    def test_to_flat_table_filter_no_columns_shows_all_columns(self):
        self.login()
        uid = self.create('a', get_new_diff(101), return_uid=True)
        self.review('a', uid)
        columns = []
        header_filtered, rows_filtered = download.to_flat_table(
            self.request, 'activities', columns=columns)
        header, rows = download.to_flat_table(
            self.request, 'activities')
        self.assertEqual(header_filtered, header)
        self.assertEqual(rows_filtered, rows)

    def test_to_flat_table_filter_non_existing_columns(self):
        self.login()
        uid = self.create('a', get_new_diff(101), return_uid=True)
        self.review('a', uid)
        columns = ['foo', 'bar']
        header, rows = download.to_flat_table(
            self.request, 'activities', columns=columns)
        self.assertEqual(len(header), 4)
        self.assertNotIn('[A] Dropdown 1_[A] Dropdown 1', header)
        row = rows[0]
        self.assertEqual(len(row), len(header))
        self.assertEqual(row[header.index('id')], uid)

    def test_to_flat_table_with_involvements(self):
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
        header, rows = download.to_flat_table(self.request, 'activities')
        self.assertEqual(len(header), self.header_length + 3)
        self.assertEqual(len(rows), 1)
        row = rows[0]
        self.assertEqual(len(row), len(header))
        self.assertTrue(header.index(
            '[A] Integerdropdown 1') < header.index('inv_role_1'))
        self.assertEqual(row[header.index('[SH] Textfield 1_1')], 'asdf')
        self.assertEqual(row[header.index('inv_role_1')], 'Stakeholder Role 6')
        self.assertEqual(row[header.index('inv_id_1')], sh_uid)

    def test_to_flat_table_without_involvements(self):
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
        header, rows = download.to_flat_table(
            self.request, 'activities', involvements='none')
        self.assertEqual(len(header), self.header_length)
        self.assertEqual(len(rows), 1)
        row = rows[0]
        self.assertEqual(len(row), len(header))
        self.assertNotIn('[SH] Textfield 1_1', row)
        self.assertNotIn('inv_role_1', row)
        self.assertNotIn('inv_id_1', row)

    @patch(
        'lmkp.views.form_config.ConfigCategoryList.'
        'getInvolvementOverviewKeyNames')
    def test_to_flat_table_with_involvement_many_overview_keys(
            self, mock_get_involvement_overview_key_names):
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
        mock_get_involvement_overview_key_names.return_value = [
            ['[SH] Textfield 1', 0], ['[SH] Numberfield 1', 1]]
        header, rows = download.to_flat_table(self.request, 'activities')
        self.assertEqual(len(header), self.header_length + 4)
        row = rows[0]
        self.assertTrue(header.index(
            '[A] Integerdropdown 1') < header.index('inv_role_1'))
        self.assertEqual(row[header.index('[SH] Textfield 1_1')], 'asdf')
        self.assertEqual(row[header.index('[SH] Numberfield 1_1')], '123.0')
        self.assertEqual(row[header.index('inv_role_1')], 'Stakeholder Role 6')
        self.assertEqual(row[header.index('inv_id_1')], sh_uid)

    def test_to_flat_table_with_mixed_involvements(self):
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
            'id': sh_uid_3,
            'version': 1,
            'role': 4
        }, {
            'id': sh_uid_1,
            'version': 1,
            'role': 6
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
        header, rows = download.to_flat_table(self.request, 'activities')
        self.assertEqual(len(header), self.header_length + 6)
        self.assertEqual(len(rows), 3)
        row_a_3 = rows[0]
        self.assertEqual(len(row_a_3), len(header))
        self.assertEqual(
            row_a_3[header.index('inv_role_1')], 'Stakeholder Role 4')
        self.assertEqual(row_a_3[header.index('inv_id_1')], sh_uid_3)
        self.assertEqual(
            row_a_3[header.index('inv_role_2')], 'Stakeholder Role 6')
        self.assertEqual(row_a_3[header.index('inv_id_2')], sh_uid_1)
        row_a_2 = rows[1]
        self.assertEqual(len(row_a_2), len(header))
        self.assertIsNone(row_a_2[header.index('inv_role_1')])
        self.assertIsNone(row_a_2[header.index('inv_id_1')])
        self.assertIsNone(row_a_2[header.index('inv_role_2')])
        self.assertIsNone(row_a_2[header.index('inv_id_2')])
        row_a_1 = rows[2]
        self.assertEqual(len(row_a_1), len(header))
        self.assertEqual(
            row_a_1[header.index('inv_role_1')], 'Stakeholder Role 3')
        self.assertEqual(row_a_1[header.index('inv_id_1')], sh_uid_2)
        self.assertIsNone(row_a_1[header.index('inv_role_2')])
        self.assertIsNone(row_a_1[header.index('inv_id_2')])

    def test_to_flat_table_translation(self):
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
        header, rows = download.to_flat_table(self.request, 'activities')
        self.assertEqual(len(header), self.header_length + 3)
        self.assertEqual(len(rows), 1)
        row = rows[0]
        self.assertEqual(
            row[header.index('[A-T] Dropdown 1_[A-T] Dropdown 1')],
            '[A-T] Value A1')
        self.assertEqual(
            row[header.index('[SH-T] Identical Translation_1')], 'asdf')

    def test_to_flat_table_translation_same_translation(self):
        self.login()
        uid = self.create('a', get_new_diff(108), return_uid=True)
        self.review('a', uid)
        self.request.params = {'_LOCALE_': 'es'}
        header, rows = download.to_flat_table(self.request, 'activities')
        self.assertEqual(len(header), self.header_length)
        self.assertEqual(header.count('[A-T] Identical Translation'), 2)
        index_mainkey = header.index('[A-T] Dropdown 1_[A-T] Dropdown 1')
        self.assertEqual(
            header.index('[A-T] Dropdown 1_[A-T] Textarea 1'),
            index_mainkey + 1)
        self.assertEqual(len(rows), 1)
        row = rows[0]
        self.assertEqual(len(row), len(header))
        self.assertEqual(
            row[header.index('[A-T] Dropdown 1_[A-T] Dropdown 1')],
            '[A-T] Value A1')
