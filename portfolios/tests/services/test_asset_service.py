from django.test import TestCase
from django.core.exceptions import ValidationError
from portfolios.services.asset_service import create_asset
from portfolios.tests.factories import AssetFactory


class AssetServiceTests(TestCase):
    def test_create_asset(self):
        asset = create_asset("Test Asset")
        self.assertEqual(asset.name, "Test Asset")

    def test_create_asset_duplicate_name(self):
        AssetFactory(name="Test Asset")
        with self.assertRaises(ValueError):
            create_asset("Test Asset") 
