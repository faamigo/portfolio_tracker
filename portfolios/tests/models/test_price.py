from django.test import TestCase
from django.core.exceptions import ValidationError
from django.utils import timezone
from datetime import timedelta
from portfolios.models import Asset, Price

class PriceTests(TestCase):
    def setUp(self):
        self.asset = Asset.objects.create(name="Test Asset")

    def test_price_must_be_positive(self):
        price = Price(
            asset=self.asset,
            date=timezone.now().date(),
            price=0
        )
        with self.assertRaises(ValidationError) as context:
            price.full_clean()
        self.assertIn("Price must be positive", str(context.exception))

    def test_price_date_cannot_be_in_future(self):
        future_date = timezone.now().date() + timedelta(days=1)
        price = Price(
            asset=self.asset,
            date=future_date,
            price=100.50
        )
        with self.assertRaises(ValidationError) as context:
            price.full_clean()
        self.assertIn("Price date cannot be in the future", str(context.exception))

    def test_valid_price(self):
        price = Price(
            asset=self.asset,
            date=timezone.now().date(),
            price=100.50
        )
        price.full_clean()
        price.save()
        self.assertEqual(Price.objects.count(), 1)

    def test_unique_together_constraint(self):
        date = timezone.now().date()
        Price.objects.create(
            asset=self.asset,
            date=date,
            price=100.50
        )
        
        price = Price(
            asset=self.asset,
            date=date,
            price=150.75
        )
        with self.assertRaises(ValidationError):
            price.full_clean()
