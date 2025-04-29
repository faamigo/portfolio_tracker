from django.test import TestCase
from django.core.exceptions import ValidationError
from django.utils import timezone
from datetime import timedelta
from portfolios.models import Portfolio, Asset, Weight

class WeightTests(TestCase):
    def setUp(self):
        self.portfolio = Portfolio.objects.create(name="Test Portfolio")
        self.asset = Asset.objects.create(name="Test Asset")

    def test_weight_must_be_between_0_and_1(self):
        weight = Weight(
            portfolio=self.portfolio,
            asset=self.asset,
            date=timezone.now().date(),
            weight=1.5
        )
        with self.assertRaises(ValidationError) as context:
            weight.full_clean()
        self.assertIn("Weight must be between 0 and 1", str(context.exception))

        weight.weight = 0
        with self.assertRaises(ValidationError) as context:
            weight.full_clean()
        self.assertIn("Weight must be between 0 and 1", str(context.exception))

    def test_weight_date_cannot_be_in_future(self):
        future_date = timezone.now().date() + timedelta(days=1)
        weight = Weight(
            portfolio=self.portfolio,
            asset=self.asset,
            date=future_date,
            weight=0.5
        )
        with self.assertRaises(ValidationError) as context:
            weight.full_clean()
        self.assertIn("Weight date cannot be in the future", str(context.exception))

    def test_valid_weight(self):
        weight = Weight(
            portfolio=self.portfolio,
            asset=self.asset,
            date=timezone.now().date(),
            weight=0.5
        )
        weight.full_clean()
        weight.save()
        self.assertEqual(Weight.objects.count(), 1)

    def test_unique_together_constraint(self):
        date = timezone.now().date()
        Weight.objects.create(
            portfolio=self.portfolio,
            asset=self.asset,
            date=date,
            weight=0.5
        )
        
        weight = Weight(
            portfolio=self.portfolio,
            asset=self.asset,
            date=date,
            weight=0.7
        )
        with self.assertRaises(ValidationError):
            weight.full_clean()
