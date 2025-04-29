from django.test import TestCase
from django.utils import timezone
from decimal import Decimal
from portfolios.services.price_service import create_price
from portfolios.tests.factories import AssetFactory, PriceFactory

class PriceServiceTests(TestCase):
    def setUp(self):
        self.asset = AssetFactory(name="Test Asset")
        self.date = timezone.now().date()

    def test_create_price(self):
        price = create_price(self.asset, self.date, Decimal("100.00"))
        self.assertEqual(price.asset, self.asset)
        self.assertEqual(price.date, self.date)
        self.assertEqual(float(price.price), 100.00)

    def test_create_price_duplicate(self):
        PriceFactory(asset=self.asset, date=self.date, price=100.00)
        with self.assertRaises(ValueError):
            create_price(self.asset, self.date, Decimal("200.00"))

    def test_create_price_invalid_value(self):
        with self.assertRaises(ValueError):
            create_price(self.asset, self.date, Decimal("-100.00"))
