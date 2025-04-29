from django.test import TestCase
from datetime import date
from portfolios.services.metrics_service import get_portfolio_metrics
from portfolios.tests.factories import (
    PortfolioFactory,
    AssetFactory,
    PriceFactory,
    HoldingFactory
)


class MetricsServiceTests(TestCase):
    def setUp(self):
        self.portfolio = PortfolioFactory(name="Test Portfolio")
        self.asset = AssetFactory(name="Test Asset")
        self.reference_date = date(2022, 2, 15)
        self.start_date = date(2022, 2, 15)
        self.end_date = date(2022, 2, 17)

        self.holding = HoldingFactory(
            portfolio=self.portfolio,
            asset=self.asset,
            date=self.reference_date,
            quantity=100.00
        )

        self.price1 = PriceFactory(
            asset=self.asset,
            date=self.start_date,
            price=10.00
        )
        self.price2 = PriceFactory(
            asset=self.asset,
            date=date(2022, 2, 16),
            price=11.00
        )
        self.price3 = PriceFactory(
            asset=self.asset,
            date=self.end_date,
            price=12.00
        )

    def test_get_portfolio_metrics(self):
        metrics = get_portfolio_metrics(
            portfolio_id=self.portfolio.id,
            start_date=self.start_date,
            end_date=self.end_date
        )
        self.assertEqual(len(metrics), 3)
        
        self.assertEqual(metrics[0]["date"], self.start_date)
        self.assertEqual(float(metrics[0]["total_value"]), 1000.00)
        self.assertEqual(metrics[0]["weights"][self.asset.name], 1.0)
        
        self.assertEqual(metrics[2]["date"], self.end_date)
        self.assertEqual(float(metrics[2]["total_value"]), 1200.00)
        self.assertEqual(metrics[2]["weights"][self.asset.name], 1.0)

    def test_get_portfolio_metrics_invalid_date(self):
        with self.assertRaises(ValueError):
            get_portfolio_metrics(
                portfolio_id=self.portfolio.id,
                start_date=date(2022, 2, 14),
                end_date=self.end_date
            )

    def test_get_portfolio_metrics_no_holdings(self):
        portfolio = PortfolioFactory(name="Empty Portfolio")
        metrics = get_portfolio_metrics(
            portfolio_id=portfolio.id,
            start_date=self.start_date,
            end_date=self.end_date
        )
        self.assertEqual(len(metrics), 0)

    def test_get_portfolio_metrics_no_prices(self):
        portfolio = PortfolioFactory(name="Portfolio No Prices")
        asset = AssetFactory(name="Asset No Prices")
        holding = HoldingFactory(
            portfolio=portfolio,
            asset=asset,
            date=self.reference_date,
            quantity=100.00
        )
        metrics = get_portfolio_metrics(
            portfolio_id=portfolio.id,
            start_date=self.start_date,
            end_date=self.end_date
        )
        self.assertEqual(len(metrics), 0)
