from django.test import TestCase
from django.utils import timezone
from portfolios.selectors.holding_selector import (
    get_holdings_by_date,
    get_asset_latest_holding_before_date,
    get_latest_portfolio_holdings
)
from portfolios.tests.factories import (
    PortfolioFactory,
    AssetFactory,
    HoldingFactory
)


class HoldingSelectorTests(TestCase):
    def setUp(self):
        self.portfolio = PortfolioFactory(name="Test Portfolio")
        self.asset = AssetFactory(name="Test Asset")
        self.date1 = timezone.now().date()
        self.date2 = self.date1 + timezone.timedelta(days=1)
        self.date3 = self.date2 + timezone.timedelta(days=1)

        self.holding1 = HoldingFactory(
            portfolio=self.portfolio,
            asset=self.asset,
            date=self.date1,
            quantity=100.50
        )
        self.holding2 = HoldingFactory(
            portfolio=self.portfolio,
            asset=self.asset,
            date=self.date2,
            quantity=105.50
        )
        self.holding3 = HoldingFactory(
            portfolio=self.portfolio,
            asset=self.asset,
            date=self.date3,
            quantity=110.50
        )

    def test_get_holdings_by_date(self):
        holdings = get_holdings_by_date(self.portfolio, self.date1)
        self.assertEqual(len(holdings), 1)
        self.assertEqual(holdings[0], self.holding1)

    def test_get_holdings_by_date_not_found(self):
        holdings = get_holdings_by_date(
            self.portfolio,
            self.date1 + timezone.timedelta(days=10)
        )
        self.assertEqual(len(holdings), 0)

    def test_get_asset_latest_holding_before_date(self):
        holding = get_asset_latest_holding_before_date(
            self.portfolio,
            self.asset,
            self.date3
        )
        self.assertEqual(holding, self.holding3)

        holding = get_asset_latest_holding_before_date(
            self.portfolio,
            self.asset,
            self.date2
        )
        self.assertEqual(holding, self.holding2)

    def test_get_asset_latest_holding_before_date_not_found(self):
        holding = get_asset_latest_holding_before_date(
            self.portfolio,
            self.asset,
            self.date1 - timezone.timedelta(days=1)
        )
        self.assertIsNone(holding)

    def test_get_latest_portfolio_holdings(self):
        holdings = get_latest_portfolio_holdings(self.portfolio)
        self.assertEqual(len(holdings), 3)
        self.assertIn(self.holding1, holdings)
        self.assertIn(self.holding2, holdings)
        self.assertIn(self.holding3, holdings)
