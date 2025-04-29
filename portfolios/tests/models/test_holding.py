from django.test import TestCase
from django.core.exceptions import ValidationError
from django.utils import timezone
from datetime import timedelta
from portfolios.models import Portfolio, Asset, Holding

class HoldingTests(TestCase):
    def setUp(self):
        self.portfolio = Portfolio.objects.create(name="Test Portfolio")
        self.asset = Asset.objects.create(name="Test Asset")

    def test_holding_date_cannot_be_in_future(self):
        future_date = timezone.now().date() + timedelta(days=1)
        holding = Holding(
            portfolio=self.portfolio,
            asset=self.asset,
            date=future_date,
            quantity=100.50
        )
        with self.assertRaises(ValidationError) as context:
            holding.full_clean()
        self.assertIn("Holding date cannot be in the future", str(context.exception))

    def test_valid_holding(self):
        holding = Holding(
            portfolio=self.portfolio,
            asset=self.asset,
            date=timezone.now().date(),
            quantity=100.50
        )
        holding.full_clean()
        holding.save()
        self.assertEqual(Holding.objects.count(), 1)

    def test_unique_together_constraint(self):
        date = timezone.now().date()
        Holding.objects.create(
            portfolio=self.portfolio,
            asset=self.asset,
            date=date,
            quantity=100.50
        )
        
        holding = Holding(
            portfolio=self.portfolio,
            asset=self.asset,
            date=date,
            quantity=150.75
        )
        with self.assertRaises(ValidationError):
            holding.full_clean()
