import pytest
from pyramid import testing
from mock import patch, Mock

from lmkp.models.database_objects import Stakeholder
from lmkp.views import download
from lmkp.protocols.stakeholder_protocol import StakeholderProtocol
from ..base import (
    LmkpTestCase,
)
from ..diffs import (
    get_new_diff,
)
from ...base import get_settings


@pytest.mark.download
@pytest.mark.usefixtures('app')
class StakeholderDownloadToTableTest(LmkpTestCase):
    """
    The download function of Stakeholders uses the protocol's
    read_many_by_activities function. In order to not having to create
    Activities for each test as well, many of these tests are based on
    the return value of read_many instead.
    """

    def setUp(self):
        self.request = testing.DummyRequest()
        settings = get_settings()
        self.config = testing.setUp(request=self.request, settings=settings)
        self.header_length = 16
        self.sh_protocol = StakeholderProtocol(self.request)

    def tearDown(self):
        testing.tearDown()

    @patch.object(StakeholderProtocol, 'read_many')
    def test_to_table_calls_stakeholder_protocol_read_many(
            self, mock_read_many):
        download.to_flat_table(self.request, 'stakeholders')
        mock_read_many.assert_called_once_with(
            public_query=True, translate=False, other_identifiers=[])

    def test_to_flat_table_preserves_order_inside_taggroup(self):
        header, __ = download.to_flat_table(self.request, 'stakeholders')
        self.assertEqual(len(header), self.header_length)
        index_mainkey = header.index('[SH] Textfield 1_[SH] Textfield 1')
        self.assertEqual(
            header.index('[SH] Textfield 1_[SH] Textarea 1'),
            index_mainkey + 1)

    def test_to_flat_table_preserves_order_of_form(self):
        header, __ = download.to_flat_table(self.request, 'stakeholders')
        self.assertEqual(len(header), self.header_length)
        index_dropdown_1 = header.index('[SH] Textfield 1_[SH] Textfield 1')
        index_checkbox_1 = header.index('[SH] Checkbox 1_1')
        index_intdropdown_2 = header.index('[SH] Integerdropdown 1')
        self.assertTrue(index_dropdown_1 < index_checkbox_1)
        self.assertTrue(index_checkbox_1 < index_intdropdown_2)

    def test_to_flat_table_has_no_geometry_column(self):
        header, __ = download.to_flat_table(self.request, 'stakeholders')
        self.assertNotIn('geometry', header)

    def test_to_flat_table_does_not_contain_keys_not_in_form(self):
        header, __ = download.to_flat_table(self.request, 'stakeholders')
        self.assertNotIn('[SH] Numberfield 3', header)

    def test_to_flat_table_can_handle_empty_result(self):
        header, rows = download.to_flat_table(self.request, 'stakeholders')
        self.assertEqual(len(header), self.header_length)
        self.assertEqual(len(rows), 0)

    def test_to_flat_table_returns_one_row(self):
        self.login()
        uid = self.create('sh', get_new_diff(201), return_uid=True)
        self.review('sh', uid)
        inv_data = [{
            'id': uid,
            'version': 1,
            'role': 6
        }]
        a_uid = self.create(
            'a', get_new_diff(103, data=inv_data), return_uid=True)
        self.review('a', a_uid)
        header, rows = download.to_flat_table(
            self.request, 'sh', involvements='none')
        self.assertEqual(len(header), self.header_length)
        self.assertEqual(len(rows), 1)
        self.assertEqual(rows[0][header.index('id')], uid)
        self.assertEqual(
            rows[0][header.index('[SH] Textfield 1_[SH] Textfield 1')],
            'asdf')
        self.assertEqual(
            rows[0][header.index('[SH] Numberfield 1')], '123.0')

    def test_to_flat_table_returns_multiple_rows(self):
        self.login()
        for i in range(3):
            uid = self.create('sh', get_new_diff(201), return_uid=True)
            self.review('sh', uid)
            inv_data = [{
                'id': uid,
                'version': 1,
                'role': 6
            }]
            a_uid = self.create(
                'a', get_new_diff(103, data=inv_data), return_uid=True)
            self.review('a', a_uid)
        header, rows = download.to_flat_table(
            self.request, 'sh', involvements='none')
        self.assertEqual(len(header), self.header_length)
        self.assertEqual(len(rows), 3)
        for r in rows:
            self.assertEqual(len(r), self.header_length)
            self.assertEqual(
                r[header.index('[SH] Textfield 1_[SH] Textfield 1')], 'asdf')
            self.assertEqual(
                r[header.index('[SH] Numberfield 1')], '123.0')

    def test_to_flat_table_with_checkboxes(self):
        self.login()
        uid = self.create('sh', get_new_diff(202), return_uid=True)
        # The Stakeholder cannot be reviewed because it is not complete. We
        # can however set it "active" directly in the database
        self.db_session.query(Stakeholder).update({'fk_status': 2})
        inv_data = [{
            'id': uid,
            'version': 1,
            'role': 6
        }]
        a_uid = self.create(
            'a', get_new_diff(103, data=inv_data), return_uid=True)
        self.review('a', a_uid)
        header, rows = download.to_flat_table(
            self.request, 'sh', involvements='none')
        self.assertEqual(len(header), self.header_length + 1)
        self.assertEqual(len(rows), 1)
        row = rows[0]
        self.assertEqual(len(header), len(row))
        self.assertEqual(
            row[header.index('[SH] Checkbox 1_1')], '[SH] Value D2')
        self.assertEqual(
            row[header.index('[SH] Checkbox 1_2')], '[SH] Value D5')

    def test_to_flat_table_with_repeating_taggroup(self):
        self.login()
        uid = self.create('sh', get_new_diff(206), return_uid=True)
        self.review('sh', uid)
        inv_data = [{
            'id': uid,
            'version': 1,
            'role': 6
        }]
        a_uid = self.create(
            'a', get_new_diff(103, data=inv_data), return_uid=True)
        self.review('a', a_uid)
        header, rows = download.to_flat_table(
            self.request, 'sh', involvements='none')
        self.assertEqual(len(header), self.header_length + 2)
        self.assertEqual(len(rows), 1)
        row = rows[0]
        self.assertEqual(len(header), len(row))
        self.assertEqual(
            row[header.index('[SH] Numberfield 2_[SH] Numberfield 2_1')],
            '1.23')
        self.assertEqual(
            row[header.index('[SH] Numberfield 2_[SH] Integerfield 1_1')],
            '159')
        self.assertEqual(
            row[header.index('[SH] Numberfield 2_[SH] Numberfield 2_2')],
            '2.34')
        self.assertEqual(
            row[header.index('[SH] Numberfield 2_[SH] Integerfield 1_2')],
            '123')

    def test_to_flat_table_files(self):
        self.login()
        uid = self.create('stakeholders', get_new_diff(207), return_uid=True)
        self.review('stakeholders', uid)
        self.review('sh', uid)
        inv_data = [{
            'id': uid,
            'version': 1,
            'role': 6
        }]
        a_uid = self.create(
            'a', get_new_diff(103, data=inv_data), return_uid=True)
        self.review('a', a_uid)
        request = self.request
        request.route_url = Mock()
        request.route_url.return_value = 'file_url'
        header, rows = download.to_flat_table(
            self.request, 'stakeholders', involvements='none')
        self.assertEqual(len(header), self.header_length)
        self.assertEqual(len(rows), 1)
        row = rows[0]
        self.assertEqual(
            row[header.index('[SH] Dropdown 2_[SH] Filefield 1_1')],
            'filename1.jpg (file_url)|filename2.pdf (file_url)')

    def test_to_flat_table_different_stakeholders(self):
        self.login()
        uid = self.create('sh', get_new_diff(201), return_uid=True)
        self.review('sh', uid)
        inv_data = [{
            'id': uid,
            'version': 1,
            'role': 6
        }]
        uid = self.create(
            'a', get_new_diff(103, data=inv_data), return_uid=True)
        self.review('a', uid)
        uid = self.create('sh', get_new_diff(204), return_uid=True)
        self.review('sh', uid)
        inv_data = [{
            'id': uid,
            'version': 1,
            'role': 6
        }]
        uid = self.create(
            'a', get_new_diff(103, data=inv_data), return_uid=True)
        self.review('a', uid)
        uid = self.create('sh', get_new_diff(206), return_uid=True)
        self.review('sh', uid)
        inv_data = [{
            'id': uid,
            'version': 1,
            'role': 6
        }]
        uid = self.create(
            'a', get_new_diff(103, data=inv_data), return_uid=True)
        self.review('a', uid)
        header, rows = download.to_flat_table(
            self.request, 'sh', involvements='none')
        self.assertEqual(len(header), self.header_length + 2)
        self.assertEqual(len(rows), 3)
        for r in rows:
            self.assertEqual(len(header), len(r))

    def test_to_flat_table_filters_columns(self):
        self.login()
        uid_1 = self.create('sh', get_new_diff(201), return_uid=True)
        self.review('sh', uid_1)
        inv_data = [{
            'id': uid_1,
            'version': 1,
            'role': 6
        }]
        uid = self.create(
            'a', get_new_diff(103, data=inv_data), return_uid=True)
        self.review('a', uid)
        uid_2 = self.create('sh', get_new_diff(206), return_uid=True)
        self.review('sh', uid_2)
        inv_data = [{
            'id': uid_2,
            'version': 1,
            'role': 6
        }]
        uid = self.create(
            'a', get_new_diff(103, data=inv_data), return_uid=True)
        self.review('a', uid)
        columns = ['[SH] Textfield 1', '[SH] Integerfield 1']
        header, rows = download.to_flat_table(
            self.request, 'stakeholders', columns=columns, involvements='none')
        self.assertEqual(len(header), 6)
        self.assertIn('[SH] Textfield 1_[SH] Textfield 1', header)
        self.assertIn('[SH] Numberfield 2_[SH] Integerfield 1_1', header)
        self.assertIn('[SH] Numberfield 2_[SH] Integerfield 1_2', header)
        self.assertNotIn('[SH] Numberfield 2', header)
        self.assertEqual(len(rows), 2)
        row_uid_1 = rows[1]
        self.assertEqual(len(row_uid_1), len(header))
        self.assertEqual(row_uid_1[header.index('id')], uid_1)
        self.assertEqual(
            row_uid_1[header.index('[SH] Textfield 1_[SH] Textfield 1')],
            'asdf')
        self.assertIsNone(
            row_uid_1[header.index(
                '[SH] Numberfield 2_[SH] Integerfield 1_1')])
        self.assertIsNone(
            row_uid_1[header.index(
                '[SH] Numberfield 2_[SH] Integerfield 1_2')])
        row_uid_2 = rows[0]
        self.assertEqual(len(row_uid_2), len(header))
        self.assertEqual(row_uid_2[header.index('id')], uid_2)
        self.assertIn(
            'Foo',
            row_uid_2[header.index('[SH] Textfield 1_[SH] Textfield 1')])
        self.assertEqual(
            row_uid_2[header.index(
                '[SH] Numberfield 2_[SH] Integerfield 1_1')],
            '159')
        self.assertEqual(
            row_uid_2[header.index(
                '[SH] Numberfield 2_[SH] Integerfield 1_2')],
            '123')

    def test_to_flat_table_filter_no_columns_shows_all_columns(self):
        self.login()
        uid = self.create('sh', get_new_diff(201), return_uid=True)
        self.review('sh', uid)
        columns = []
        header_filtered, rows_filtered = download.to_flat_table(
            self.request, 'stakeholders', columns=columns)
        header, rows = download.to_flat_table(
            self.request, 'stakeholders')
        self.assertEqual(header_filtered, header)
        self.assertEqual(rows_filtered, rows)

    def test_to_flat_table_filter_non_existing_columns(self):
        self.login()
        uid = self.create('sh', get_new_diff(201), return_uid=True)
        self.review('sh', uid)
        inv_data = [{
            'id': uid,
            'version': 1,
            'role': 6
        }]
        a_uid = self.create(
            'a', get_new_diff(103, data=inv_data), return_uid=True)
        self.review('a', a_uid)
        columns = ['foo', 'bar']
        header, rows = download.to_flat_table(
            self.request, 'stakeholders', columns=columns, involvements='none')
        self.assertEqual(len(header), 3)
        self.assertNotIn('[SH] Textfield 1_[SH] Textfield 1', header)
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
        header, rows = download.to_flat_table(self.request, 'stakeholders')
        self.assertEqual(len(header), self.header_length + 3)
        self.assertEqual(len(rows), 1)
        row = rows[0]
        self.assertEqual(len(row), len(header))
        self.assertTrue(header.index(
            '[SH] Integerdropdown 1') < header.index('inv_role_1'))
        self.assertEqual(
            row[header.index('[A] Dropdown 1_1')], '[A] Value A1')
        self.assertEqual(row[header.index('inv_role_1')], 'Stakeholder Role 6')
        self.assertEqual(row[header.index('inv_id_1')], a_uid)

    def test_to_flat_table_only_returns_stakeholders_involved_in_activities(
            self):
        self.login()
        sh_uid_1 = self.create('sh', get_new_diff(201), return_uid=True)
        self.review('sh', sh_uid_1)
        inv = [{
            'id': sh_uid_1,
            'version': 1,
            'role': 6
        }]
        a_uid = self.create('a', get_new_diff(103, data=inv), return_uid=True)
        self.review('a', a_uid)
        sh_uid_2 = self.create('sh', get_new_diff(201), return_uid=True)
        self.review('sh', sh_uid_2)
        header, rows = download.to_flat_table(self.request, 'stakeholders')
        self.assertEqual(len(header), self.header_length + 3)
        self.assertEqual(len(rows), 1)

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
            self.request, 'stakeholders', involvements='none')
        self.assertEqual(len(header), self.header_length)
        self.assertEqual(len(rows), 1)
        row = rows[0]
        self.assertEqual(len(row), len(header))
        self.assertNotIn('[A] Dropdown 1_1', row)
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
            ['[A] Dropdown 1', 0], ['[A] Numberfield 1', 1]]
        header, rows = download.to_flat_table(self.request, 'stakeholders')
        self.assertEqual(len(header), self.header_length + 4)
        row = rows[0]
        self.assertTrue(header.index(
            '[SH] Integerdropdown 1') < header.index('inv_role_1'))
        self.assertEqual(row[header.index('[A] Dropdown 1_1')], '[A] Value A1')
        self.assertEqual(row[header.index('[A] Numberfield 1_1')], '123.45')
        self.assertEqual(row[header.index('inv_role_1')], 'Stakeholder Role 6')
        self.assertEqual(row[header.index('inv_id_1')], a_uid)

    def test_to_flat_table_with_mixed_involvements(self):
        self.login()
        sh_uid_1 = self.create('sh', get_new_diff(201), return_uid=True)
        self.review('sh', sh_uid_1)
        sh_uid_2 = self.create('sh', get_new_diff(201), return_uid=True)
        self.review('sh', sh_uid_2)
        sh_uid_3 = self.create('sh', get_new_diff(203), return_uid=True)
        self.review('sh', sh_uid_3)
        inv_1 = [{
            'id': sh_uid_3,
            'version': 1,
            'role': 3
        }]
        inv_2 = [{
            'id': sh_uid_3,
            'version': 2,
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
        header, rows = download.to_flat_table(self.request, 'stakeholders')
        self.assertEqual(len(header), self.header_length + 6)
        self.assertEqual(len(rows), 2)
        row_sh_3 = rows[0]
        self.assertEqual(len(row_sh_3), len(header))
        self.assertEqual(row_sh_3[header.index('id')], sh_uid_3)
        self.assertEqual(
            row_sh_3[header.index('inv_role_1')], 'Stakeholder Role 3')
        self.assertEqual(row_sh_3[header.index('inv_id_1')], a_uid_1)
        self.assertEqual(
            row_sh_3[header.index('inv_role_2')], 'Stakeholder Role 4')
        self.assertEqual(row_sh_3[header.index('inv_id_2')], a_uid_3)
        row_sh_1 = rows[1]
        self.assertEqual(len(row_sh_1), len(header))
        self.assertEqual(row_sh_1[header.index('id')], sh_uid_1)
        self.assertEqual(
            row_sh_1[header.index('inv_role_1')], 'Stakeholder Role 6')
        self.assertEqual(row_sh_1[header.index('inv_id_1')], a_uid_3)
        self.assertIsNone(row_sh_1[header.index('inv_role_2')])
        self.assertIsNone(row_sh_1[header.index('inv_id_2')])

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
        header, rows = download.to_flat_table(self.request, 'stakeholders')
        self.assertEqual(len(header), self.header_length + 3)
        self.assertEqual(len(rows), 1)
        row = rows[0]
        self.assertEqual(
            row[header.index('[A-T] Dropdown 1_1')],
            '[A-T] Value A1')
        self.assertEqual(
            row[header.index(
                '[SH-T] Identical Translation_[SH-T] Identical Translation')],
            'asdf')

    def test_to_flat_table_translation_same_translation(self):
        self.login()
        uid = self.create('sh', get_new_diff(208), return_uid=True)
        self.review('sh', uid)
        inv = [{
            'id': uid,
            'version': 1,
            'role': 6
        }]
        a_uid = self.create('a', get_new_diff(103, data=inv), return_uid=True)
        self.review('a', a_uid)
        self.request.params = {'_LOCALE_': 'es'}
        header, rows = download.to_flat_table(
            self.request, 'sh', involvements='none')
        self.assertEqual(len(header), self.header_length)
        row = rows[0]
        self.assertEqual(len(rows), 1)
        self.assertEqual(
            row[header.index(
                '[SH-T] Identical Translation_[SH-T] Identical Translation')],
            'First Remark')
        self.assertEqual(
            row[header.index('[SH-T] Identical Translation')],
            'Second Remark')
