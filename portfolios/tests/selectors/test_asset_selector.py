from django.test import TestCase
from django.core.exceptions import ObjectDoesNotExist
from portfolios.selectors.asset_selector import (
    get_asset_by_id,
    get_asset_by_name
)
from portfolios.tests.factories import AssetFactory


class AssetSelectorTests(TestCase):
    def setUp(self):
        self.asset = AssetFactory(name="Test Asset")

    def test_get_asset_by_id(self):
        asset = get_asset_by_id(self.asset.id)
        self.assertEqual(asset, self.asset)

    def test_get_asset_by_id_not_found(self):
        with self.assertRaises(ObjectDoesNotExist):
            get_asset_by_id(999)

    def test_get_asset_by_name(self):
        asset = get_asset_by_name("Test Asset")
        self.assertEqual(asset, self.asset)

    def test_get_asset_by_name_not_found(self):
        with self.assertRaises(ObjectDoesNotExist):
            get_asset_by_name("Non Existent Asset")
