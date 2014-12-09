import pytest
import uuid

from ..diffs import (
    get_new_diff,
)
from ..base import (
    LmkpTestCase,
    get_status_from_item_json,
)
from ...base import (
    FEEDBACK_NOT_VALID_FORMAT,
    STATUS_PENDING,
    TITLE_HISTORY_VIEW,
    TITLE_STAKEHOLDER_EDITOR,
)


@pytest.mark.usefixtures('app')
@pytest.mark.integration
@pytest.mark.stakeholders
class StakeholderCreateTests(LmkpTestCase):

    def test_stakeholder_cannot_be_created_without_login(self):
        """
        New Stakeholders cannot be created if the user is not logged in.
        """
        res = self.create('sh', {})

        self.assertEqual(res.status_int, 200)
        self.assertIn(b'Please login', res.body)

    def test_cannot_create_empty_stakeholder(self):
        """
        When trying to create a Stakeholder with an empty JSON, a 400
        (Bad Response) code is returned with an error message in the
        body.
        """
        self.login()
        res = self.create('sh', {}, expect_errors=True)
        self.assertEqual(res.status_int, 400)
        res.mustcontain(FEEDBACK_NOT_VALID_FORMAT)

    def test_stakeholder_can_be_created_with_all_mandatory_fields(self):
        """
        New Stakeholders can be created with all mandatory fields.
        """
        self.login()
        res = self.create('sh', get_new_diff(201))
        self.assertEqual(res.status_int, 201)
        json = res.json
        self.assertEqual(json['total'], 1)
        self.assertTrue(json['created'])
        self.assertEqual(len(json['data']), 1)
        self.assertIn('id', json['data'][0])

    def test_stakeholder_can_be_created_without_mandatory_fields(self):
        """
        New Stakeholders can be created even without mandatory fields.
        """
        self.login()
        res = self.create('sh', get_new_diff(202))
        self.assertEqual(res.status_int, 201)
        json = res.json
        self.assertEqual(json['total'], 1)
        self.assertTrue(json['created'])
        self.assertEqual(len(json['data']), 1)
        self.assertIn('id', json['data'][0])

    def test_stakeholder_cannot_be_created_with_invalid_key(self):
        self.login()
        diff = get_new_diff(201)
        diff['stakeholders'][0]['taggroups'][0]['main_tag']['key'] = 'Foo'
        diff['stakeholders'][0]['taggroups'][0]['tags'][0]['key'] = 'Foo'
        res = self.create('sh', diff, expect_errors=True)
        self.assertEqual(res.status_int, 400)
        res.mustcontain("Key: Foo or Value: 123.0 is not valid.")

    def test_stakeholder_cannot_be_created_with_invalid_value(self):
        self.login()
        diff = get_new_diff(202)
        diff['stakeholders'][0]['taggroups'][0]['main_tag']['value'] = 'Foo'
        diff['stakeholders'][0]['taggroups'][0]['tags'][0]['value'] = 'Foo'
        res = self.create('sh', diff, expect_errors=True)
        self.assertEqual(res.status_int, 400)
        res.mustcontain("Key: [SH] Checkbox 1 or Value: Foo is not valid.")

    def test_stakeholder_can_be_created_with_special_chars(self):
        self.login()
        res = self.create('sh', get_new_diff(204))
        self.assertEqual(res.status_int, 201)
        json = res.json
        self.assertEqual(json['total'], 1)
        self.assertTrue(json['created'])
        self.assertEqual(len(json['data']), 1)
        self.assertIn('id', json['data'][0])

    # def test_stakeholders_cannot_be_created_with_involvements(self):
    #     self.login()
    #     diff = get_new_diff(201)
    #     a_uid = self.create('a', get_new_diff(101), return_uid=True)
    #     diff['stakeholders'][0]['activities'] = [{
    #         'id': a_uid,
    #         'version': 1,
    #         'role': 1,
    #         'op': 'add'
    #     }]
    #     res = self.create('sh', diff, expect_errors=True)
    #     self.assertEqual(res.status_int, 400)
    #     res.mustcontain('Invalid')

    def test_new_stakeholders_have_status_pending(self):
        """
        Test that new Stakeholders are created with status "pending".
        """
        self.login()
        uid = self.create('sh', get_new_diff(201), return_uid=True)
        json = self.read_one_history('sh', uid, 'json')
        self.assertEqual(json['total'], 1)
        status = get_status_from_item_json(json)
        self.assertEqual(STATUS_PENDING, status)

    def test_new_stakeholders_appear_in_read_many_json_service(self):
        """
        Newly created Stakeholders appear in the JSON service "read many".
        """
        self.login()

        json = self.read_many('sh', 'json')
        self.assertEqual(json['data'], [])
        self.assertEqual(json['total'], 0)

        self.create('sh', get_new_diff(201))

        json = self.read_many('sh', 'json')
        self.assertEqual(json['total'], 1)

    def test_history_view(self):
        """
        Test that a history view is available for newly created
        Stakeholders.
        """
        self.login()
        uid = self.create('sh', get_new_diff(201), return_uid=True)

        res = self.app.get('/stakeholders/history/html/%s' % uid)
        self.assertEqual(res.status_int, 200)
        self.assertIn(TITLE_HISTORY_VIEW, res.body)

    def test_stakeholder_form_returns_404_if_no_item(self):
        self.login()
        res = self.app.get(
            '/stakeholders/form/%s?v=1' % str(uuid.uuid4()), status=404)
        self.assertEqual(res.status_int, 404)

    def test_stakeholder_form_is_available(self):
        self.login()
        uid = self.create('sh', get_new_diff(201), return_uid=True)
        res = self.app.get('/stakeholders/form/%s?v=1' % uid)
        self.assertIn(TITLE_STAKEHOLDER_EDITOR, res)
        self.assertIn(uid, res)
