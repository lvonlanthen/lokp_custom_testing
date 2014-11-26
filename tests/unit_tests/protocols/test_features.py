import pytest
from pyramid import testing

from ...integration_tests.base import (
    LmkpTestCase,
)
from ...base import get_settings
from lmkp.protocols.features import (
    ItemFeature,
    ItemTaggroup,
    ItemTag,
)


@pytest.mark.unittest
@pytest.mark.protocol
@pytest.mark.features
class FeaturesItemFeatureTests(LmkpTestCase):

    def setUp(self):
        self.request = testing.DummyRequest()
        settings = get_settings()
        self.config = testing.setUp(request=self.request, settings=settings)
        self.feature = ItemFeature('identifier', 'order_value', 1, 2)
        self.taggroup1 = ItemTaggroup(1, 2, 3)
        self.taggroup2 = ItemTaggroup(2, 3, 4)

    def tearDown(self):
        testing.tearDown()

    def test_create_item_feature(self):
        feature = ItemFeature('id', 'order', 2, 3)
        self.assertIsInstance(feature, ItemFeature)

    def test_item_feature_identifier(self):
        self.assertEqual(self.feature.identifier, 'identifier')

    def test_item_feature_version(self):
        self.assertEqual(self.feature.version, 1)

    def test_item_feature_order_value(self):
        self.assertEqual(self.feature.order_value, 'order_value')

    def test_item_feature_status_id(self):
        self.assertEqual(self.feature.status_id, 2)

    def test_item_feature_timestamp(self):
        feature = ItemFeature('identifier', 'order_value', 1, 2)
        feature.timestamp = 'foo'
        self.assertEqual(feature.timestamp, 'foo')

    def test_item_feature_previous_version(self):
        feature = ItemFeature('identifier', 'order_value', 1, 2)
        feature.previous_version = 1
        self.assertEqual(feature.previous_version, 1)

    def test_item_feature_userid(self):
        feature = ItemFeature('identifier', 'order_value', 1, 2)
        feature.userid = 1
        self.assertEqual(feature.userid, 1)

    def test_item_feature_username(self):
        feature = ItemFeature('identifier', 'order_value', 1, 2)
        feature.username = 'foo'
        self.assertEqual(feature.username, 'foo')

    def test_item_feature_user_privacy(self):
        feature = ItemFeature('identifier', 'order_value', 1, 2)
        feature.user_privacy = 1
        self.assertEqual(feature.user_privacy, 1)

    def test_item_feature_user_firstname(self):
        feature = ItemFeature('identifier', 'order_value', 1, 2)
        feature.user_firstname = 'foo'
        self.assertEqual(feature.user_firstname, 'foo')

    def test_item_feature_user_lastname(self):
        feature = ItemFeature('identifier', 'order_value', 1, 2)
        feature.user_lastname = 'foo'
        self.assertEqual(feature.user_lastname, 'foo')

    def test_item_feature_institution_id(self):
        feature = ItemFeature('identifier', 'order_value', 1, 2)
        feature.institution_id = 1
        self.assertEqual(feature.institution_id, 1)

    def test_item_feature_institution_name(self):
        feature = ItemFeature('identifier', 'order_value', 1, 2)
        feature.institution_name = 'foo'
        self.assertEqual(feature.institution_name, 'foo')

    def test_item_feature_institution_url(self):
        feature = ItemFeature('identifier', 'order_value', 1, 2)
        feature.institution_url = 'foo'
        self.assertEqual(feature.institution_url, 'foo')

    def test_item_feature_institution_logo(self):
        feature = ItemFeature('identifier', 'order_value', 1, 2)
        feature.institution_logo = 'foo'
        self.assertEqual(feature.institution_logo, 'foo')

    def test_item_feature_taggroups(self):
        taggroups = self.feature.taggroups
        self.assertIsInstance(taggroups, list)
        self.assertEqual(len(taggroups), 0)

    def test_item_feature_add_taggroups(self):
        self.feature.add_taggroup(self.taggroup1)
        self.feature.add_taggroup(self.taggroup2)
        taggroups = self.feature.taggroups
        self.assertEqual(len(taggroups), 2)
        self.assertIn(self.taggroup1, taggroups)
        self.assertIn(self.taggroup2, taggroups)

    def test_item_feature_add_taggroups_only_add_taggroups(self):
        self.feature.add_taggroup('foo')
        self.feature.add_taggroup(0)
        self.assertEqual(len(self.feature.taggroups), 0)

    def test_item_feature_get_taggroup_by_id_returns_taggroup(self):
        self.feature.add_taggroup(self.taggroup1)
        self.feature.add_taggroup(self.taggroup2)
        taggroup = self.feature.get_taggroup_by_id(2)
        self.assertEqual(taggroup, self.taggroup2)

    def test_item_feature_get_taggroup_by_id_returns_none(self):
        self.feature.add_taggroup(self.taggroup1)
        self.feature.add_taggroup(self.taggroup2)
        self.assertIsNone(self.feature.get_taggroup_by_id(0))

    def test_item_feature_to_json(self):
        self.taggroup1.add_tag(ItemTag(3, 'key1', 'value1'))
        self.feature.add_taggroup(self.taggroup1)
        self.taggroup2.add_tag(ItemTag(4, 'key2', 'value2'))
        self.feature.add_taggroup(self.taggroup2)
        json = self.feature.to_json(self.request)
        self.assertIsInstance(json, dict)
        self.assertEqual(json.get('id'), 'identifier')
        self.assertEqual(
            json.get('taggroups'),
            [self.taggroup1.to_json(), self.taggroup2.to_json()])
        self.assertEqual(json.get('status_id'), 2)
        self.assertEqual(json.get('version'), 1)
        self.assertNotIn('geometry', json)

    def test_item_feature_to_json_contains_timestamp(self):
        json = self.feature.to_json(self.request)
        self.assertIsNone(json['timestamp'])
        self.feature.timestamp = 'foo'
        json = self.feature.to_json(self.request)
        self.assertEqual(json.get('timestamp'), 'foo')

    def test_item_feature_to_json_contains_status(self):
        json = self.feature.to_json(self.request)
        self.assertEqual(json.get('status'), 'active')

    def test_item_feature_to_json_contains_involvements_if_available(self):
        json = self.feature.to_json(self.request)
        self.assertNotIn('involvements', json)
        inv = ItemFeature('id', 'order', 2, 3)
        self.feature.add_involvement(inv)
        json = self.feature.to_json(self.request)
        self.assertEqual(json.get('involvements'), [inv.to_json(self.request)])

    def test_item_feature_to_json_contains_previous_version(self):
        json = self.feature.to_json(self.request)
        self.assertIsNone(json['previous_version'])
        self.feature.previous_version = 'foo'
        json = self.feature.to_json(self.request)
        self.assertEqual(json.get('previous_version'), 'foo')

    def test_item_feature_to_json_contains_user_details_if_available(self):
        json = self.feature.to_json(self.request)
        self.assertNotIn('user', json)
        self.feature.userid = 'user_id'
        self.feature.username = 'user_name'
        json = self.feature.to_json(self.request)
        self.assertIn('user', json)
        self.assertEqual(json.get('user').get('id'), 'user_id')
        self.assertEqual(json.get('user').get('username'), 'user_name')

    def test_item_feature_to_json_contains_user_details_privacy(self):
        self.feature.userid = 'user_id'
        self.feature.username = 'user_name'
        self.feature.user_firstname = 'foo'
        self.feature.user_lastname = 'bar'
        json = self.feature.to_json(self.request)
        self.assertNotIn('firstname', json.get('user'))
        self.assertNotIn('lastname', json.get('user'))
        self.feature.user_privacy = 0
        json = self.feature.to_json(self.request)
        self.assertNotIn('firstname', json.get('user'))
        self.assertNotIn('lastname', json.get('user'))
        self.feature.user_privacy = 1
        json = self.feature.to_json(self.request)
        self.assertEqual(json.get('user').get('firstname'), 'foo')
        self.assertEqual(json.get('user').get('lastname'), 'bar')

    def test_item_feature_to_json_contains_institution_if_available(self):
        json = self.feature.to_json(self.request)
        self.assertNotIn('institution', json)
        self.feature.institution_id = 'inst_id'
        self.feature.institution_name = 'inst_name'
        json = self.feature.to_json(self.request)
        self.assertIn('institution', json)
        self.assertEqual(json.get('institution').get('id'), 'inst_id')
        self.assertEqual(json.get('institution').get('name'), 'inst_name')


@pytest.mark.unittest
@pytest.mark.protocol
@pytest.mark.features
class FeaturesItemTaggroupTests(LmkpTestCase):

    def setUp(self):
        self.request = testing.DummyRequest()
        settings = get_settings()
        self.config = testing.setUp(request=self.request, settings=settings)
        self.taggroup = ItemTaggroup(1, 2, 2)
        self.tag1 = ItemTag(1, 'key1', 'value1')
        self.tag2 = ItemTag(2, 'key2', 'value2')

    def tearDown(self):
        testing.tearDown()

    def test_create_item_taggroup(self):
        taggroup = ItemTaggroup(1, 2, 3)
        self.assertIsInstance(taggroup, ItemTaggroup)

    def test_item_taggroup_id(self):
        self.assertEqual(self.taggroup.id, 1)

    def test_item_taggroup_taggroup_id(self):
        self.assertEqual(self.taggroup.taggroup_id, 2)

    def test_item_taggroup_main_tag_id(self):
        self.assertEqual(self.taggroup.main_tag_id, 2)

    def test_item_taggroup_add_tags(self):
        self.taggroup.add_tag(self.tag1)
        self.taggroup.add_tag(self.tag2)
        tags = self.taggroup.tags
        self.assertEqual(len(tags), 2)
        self.assertIn(self.tag1, tags)
        self.assertIn(self.tag2, tags)

    def test_item_taggroup_add_tags_only_add_tags(self):
        self.taggroup.add_tag('foo')
        self.taggroup.add_tag(0)
        self.assertEqual(len(self.taggroup.tags), 0)

    def test_item_taggroup_add_tags_also_sets_main_tag(self):
        self.assertIsNone(self.taggroup.main_tag)
        self.taggroup.add_tag(self.tag1)
        self.assertIsNone(self.taggroup.main_tag)
        self.taggroup.add_tag(self.tag2)
        self.assertEqual(self.taggroup.main_tag, self.tag2)

    def test_item_taggroup_get_tag_by_id_returns_tag(self):
        self.taggroup.add_tag(self.tag1)
        self.taggroup.add_tag(self.tag2)
        tag = self.taggroup.get_tag_by_id(2)
        self.assertEqual(tag, self.tag2)

    def test_item_taggroup_get_tag_by_id_returns_none(self):
        self.taggroup.add_tag(self.tag1)
        self.taggroup.add_tag(self.tag2)
        self.assertIsNone(self.taggroup.get_tag_by_id(0))

    def test_item_taggroup_main_tag(self):
        self.taggroup.main_tag = self.tag1
        self.assertEqual(self.taggroup.main_tag, self.tag1)

    def test_item_taggroup_main_tag_needs_to_be_tag(self):
        self.taggroup.main_tag = 'foo'
        self.assertIsNone(self.taggroup.main_tag)

    def test_item_taggroup_to_json(self):
        self.taggroup.add_tag(self.tag1)
        self.taggroup.add_tag(self.tag2)
        json = self.taggroup.to_json()
        self.assertIsInstance(json, dict)
        self.assertEqual(json.get('id'), 1)
        self.assertEqual(json.get('tg_id'), 2)
        self.assertEqual(json.get('main_tag'), self.tag2.to_json())
        self.assertEqual(
            json.get('tags'), [self.tag1.to_json(), self.tag2.to_json()])
        self.assertNotIn('geometry', json)


@pytest.mark.unittest
@pytest.mark.protocol
@pytest.mark.features
class FeaturesItemTagTests(LmkpTestCase):

    def setUp(self):
        self.request = testing.DummyRequest()
        settings = get_settings()
        self.config = testing.setUp(request=self.request, settings=settings)
        self.tag = ItemTag(1, 'key', 'value')

    def tearDown(self):
        testing.tearDown()

    def test_create_item_tag(self):
        tag = ItemTag(1, 'k', 'v')
        self.assertIsInstance(tag, ItemTag)

    def test_item_tag_id(self):
        self.assertEqual(self.tag.id, 1)

    def test_item_tag_key(self):
        self.assertEqual(self.tag.key, 'key')

    def test_item_tag_value(self):
        self.assertEqual(self.tag.value, 'value')

    def test_item_tag_to_json(self):
        json = self.tag.to_json()
        self.assertIsInstance(json, dict)
        self.assertEqual(json.get('id'), 1)
        self.assertEqual(json.get('key'), 'key')
        self.assertEqual(json.get('value'), 'value')
