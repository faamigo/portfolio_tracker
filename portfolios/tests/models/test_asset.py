from django.test import TestCase
from django.core.exceptions import ValidationError
from portfolios.models import Asset

class AssetTests(TestCase):
    def test_asset_name_cannot_be_empty(self):
        asset = Asset(name="")
        with self.assertRaises(ValidationError) as context:
            asset.full_clean()
        self.assertIn("Asset name cannot be empty", str(context.exception))

    def test_asset_name_must_be_at_least_2_characters(self):
        asset = Asset(name="a")
        with self.assertRaises(ValidationError) as context:
            asset.full_clean()
        self.assertIn("Asset name must be at least 2 characters long", str(context.exception))

    def test_asset_name_cannot_be_just_whitespace(self):
        asset = Asset(name="   ")
        with self.assertRaises(ValidationError) as context:
            asset.full_clean()
        self.assertIn("Asset name cannot be empty", str(context.exception))

    def test_valid_asset(self):
        asset = Asset(name="Test Asset")
        asset.full_clean()
        asset.save()
        self.assertEqual(Asset.objects.count(), 1)
