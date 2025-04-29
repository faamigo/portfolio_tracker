from django.test import TestCase
from django.utils import timezone
from portfolios.selectors.weight_selector import (
    get_portfolio_weights_by_date,
    get_latest_portfolio_weights
)
from portfolios.tests.factories import (
    PortfolioFactory,
    AssetFactory,
    WeightFactory
)


class WeightSelectorTests(TestCase):
    def setUp(self):
        self.portfolio = PortfolioFactory(name="Test Portfolio")
        self.asset = AssetFactory(name="Test Asset")
        self.date1 = timezone.now().date()
        self.date2 = self.date1 + timezone.timedelta(days=1)
        self.date3 = self.date2 + timezone.timedelta(days=1)

        self.weight1 = WeightFactory(
            portfolio=self.portfolio,
            asset=self.asset,
            date=self.date1,
            weight=0.5
        )
        self.weight2 = WeightFactory(
            portfolio=self.portfolio,
            asset=self.asset,
            date=self.date2,
            weight=0.6
        )
        self.weight3 = WeightFactory(
            portfolio=self.portfolio,
            asset=self.asset,
            date=self.date3,
            weight=0.7
        )

    def test_get_portfolio_weights_by_date(self):
        weights = get_portfolio_weights_by_date(self.portfolio, self.date1)
        self.assertEqual(len(weights), 1)
        self.assertEqual(weights[0], self.weight1)

    def test_get_portfolio_weights_by_date_not_found(self):
        weights = get_portfolio_weights_by_date(
            self.portfolio,
            self.date1 + timezone.timedelta(days=10)
        )
        self.assertEqual(len(weights), 0)

    def test_get_latest_portfolio_weights(self):
        weights = get_latest_portfolio_weights(self.portfolio)
        self.assertEqual(len(weights), 3)
        self.assertIn(self.weight1, weights)
        self.assertIn(self.weight2, weights)
        self.assertIn(self.weight3, weights)
