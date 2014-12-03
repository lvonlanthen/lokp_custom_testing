import pytest
from pyramid import testing
from mock import patch, Mock

from ...integration_tests.base import (
    LmkpTestCase,
)
from ...base import get_settings
from lmkp.protocols.activity_features import (
    ActivityFeature,
    ActivityTaggroup,
)
from lmkp.protocols.features import ItemTag


@pytest.mark.unittest
@pytest.mark.protocol
@pytest.mark.features
class FeaturesActivityFeatureTests(LmkpTestCase):

    def setUp(self):
        self.request = testing.DummyRequest()
        settings = get_settings()
        self.config = testing.setUp(request=self.request, settings=settings)
        self.feature = ActivityFeature(
            'id', 'identifier', 'order_value', 1, 2, 'geometry')
        self.taggroup1 = ActivityTaggroup(1, 2, 3, 'geom1')
        self.taggroup2 = ActivityTaggroup(2, 3, 4, 'geom2')

    def tearDown(self):
        testing.tearDown()

    def test_create_activity_feature(self):
        feature = ActivityFeature('id', 'id', 'order', 2, 3, 'geom')
        self.assertIsInstance(feature, ActivityFeature)

    def test_activity_feature_geometry(self):
        self.assertEqual(self.feature.geometry, 'geometry')

    def test_activity_feature_geojson_properties(self):
        self.assertEqual(self.feature.geojson_properties, {})

    def test_activity_feature_set_geojson_properties(self):
        self.feature.set_geojson_property('foo', 'bar')
        self.assertEqual(self.feature.geojson_properties, {'foo': 'bar'})

    def test_activity_feature_set_geojson_properties_duplicates(self):
        self.feature.set_geojson_property('foo', 'bar1')
        self.feature.set_geojson_property('foo', 'bar2')
        self.feature.set_geojson_property('foo', 'bar3')
        self.assertEqual(
            self.feature.geojson_properties, {'foo': ['bar1', 'bar2', 'bar3']})

    def test_activity_feature_add_taggroups(self):
        self.feature.add_taggroup(self.taggroup1)
        self.feature.add_taggroup(self.taggroup2)
        taggroups = self.feature.taggroups
        self.assertEqual(len(taggroups), 2)
        self.assertIn(self.taggroup1, taggroups)
        self.assertIn(self.taggroup2, taggroups)

    @patch('lmkp.protocols.activity_features.geometry')
    @patch('lmkp.protocols.activity_features.wkb')
    def test_activity_feature_to_json_contains_geometry(
            self, mock_wkb, mock_geometry):
        mock_wkb.loads.return_value = 'foo'
        mock_geometry.mapping.return_value = 'geom'
        self.feature.geometry = Mock()
        self.feature.geometry.geom_wkb = 'foo'
        self.taggroup1.add_tag(ItemTag(3, 'key1', 'value1'))
        self.feature.add_taggroup(self.taggroup1)
        self.taggroup2.add_tag(ItemTag(4, 'key2', 'value2'))
        self.feature.add_taggroup(self.taggroup2)
        json = self.feature.to_json(self.request)
        self.assertIn('geometry', json)
        self.assertEqual(json.get('geometry'), 'geom')

    def test_activity_feature_to_geojson_returns_none_if_no_geometry(self):
        self.feature.geometry = None
        geojson = self.feature.to_geojson(self.request)
        self.assertIsNone(geojson)

    def test_activity_feature_to_geojson_returns_none_if_invalid_geometry(
            self):
        geojson = self.feature.to_geojson(self.request)
        self.assertIsNone(geojson)

    @patch('lmkp.protocols.activity_features.geometry')
    @patch('lmkp.protocols.activity_features.wkb')
    def test_activity_feature_to_geojson_contains_geometry_and_properties(
            self, mock_wkb, mock_geometry):
        mock_wkb.loads.return_value = 'foo'
        mock_geometry.mapping.return_value = 'geom'
        self.feature.geometry = Mock()
        self.feature.geometry.geom_wkb = 'foo'
        geojson = self.feature.to_geojson(self.request)
        self.assertIn('geometry', geojson)
        self.assertIn('properties', geojson)

    @patch('lmkp.protocols.activity_features.geometry')
    @patch('lmkp.protocols.activity_features.wkb')
    def test_activity_feature_to_geojson_contains_properties(
            self, mock_wkb, mock_geometry):
        mock_wkb.loads.return_value = 'foo'
        mock_geometry.mapping.return_value = 'geom'
        self.feature.geometry = Mock()
        self.feature.geometry.geom_wkb = 'foo'
        self.feature.set_geojson_property('foo', 'bar')
        geojson = self.feature.to_geojson(self.request)
        self.assertIn('foo', geojson.get('properties'))
        self.assertEqual(geojson.get('properties').get('foo'), 'bar')


@pytest.mark.unittest
@pytest.mark.protocol
@pytest.mark.features
class FeaturesActivityTaggroupTests(LmkpTestCase):

    def setUp(self):
        self.request = testing.DummyRequest()
        settings = get_settings()
        self.config = testing.setUp(request=self.request, settings=settings)
        self.taggroup = ActivityTaggroup(1, 2, 1, 'geometry')
        self.tag = ItemTag(1, 'key', 'value')

    def tearDown(self):
        testing.tearDown()

    def test_create_activity_taggroup(self):
        taggroup = ActivityTaggroup(1, 2, 3, 'geom')
        self.assertIsInstance(taggroup, ActivityTaggroup)

    def test_activity_taggroup_geometry(self):
        self.assertEqual(self.taggroup.geometry, 'geometry')

    @patch('lmkp.protocols.activity_features.geometry')
    @patch('lmkp.protocols.activity_features.wkb')
    def test_activity_taggroup_to_json_contains_geometry(
            self, mock_wkb, mock_geometry):
        mock_wkb.loads.return_value = 'foo'
        mock_geometry.mapping.return_value = 'geom'
        self.taggroup.geometry = Mock()
        self.taggroup.geometry.geom_wkb = 'foo'
        self.taggroup.add_tag(self.tag)
        json = self.taggroup.to_json()
        self.assertIn('geometry', json)
        self.assertEqual(json.get('geometry'), 'geom')
