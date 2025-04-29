from django.test import TestCase
from django.utils import timezone
from decimal import Decimal
from portfolios.services.weight_service import create_weight
from portfolios.tests.factories import (
    PortfolioFactory,
    AssetFactory,
    WeightFactory
)


class WeightServiceTests(TestCase):
    def setUp(self):
        self.portfolio = PortfolioFactory(name="Test Portfolio")
        self.asset = AssetFactory(name="Test Asset")
        self.date = timezone.now().date()

    def test_create_weight(self):
        weight = create_weight(
            portfolio=self.portfolio,
            asset=self.asset,
            date=self.date,
            weight=Decimal("0.5")
        )
        self.assertEqual(weight.portfolio, self.portfolio)
        self.assertEqual(weight.asset, self.asset)
        self.assertEqual(float(weight.weight), 0.5)

    def test_create_weight_invalid_value(self):
        with self.assertRaises(ValueError):
            create_weight(
                portfolio=self.portfolio,
                asset=self.asset,
                date=self.date,
                weight=Decimal("1.5")
            )

    def test_create_weight_duplicate(self):
        WeightFactory(portfolio=self.portfolio, asset=self.asset, date=self.date, weight=0.5)
        with self.assertRaises(ValueError):
            create_weight(
                portfolio=self.portfolio,
                asset=self.asset,
                date=self.date,
                weight=Decimal("0.6")
            )
