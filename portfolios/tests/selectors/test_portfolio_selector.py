from django.test import TestCase
from django.core.exceptions import ObjectDoesNotExist
from django.utils import timezone
from portfolios.selectors.portfolio_selector import (
    get_portfolio_by_id,
    get_portfolio_by_name,
    get_portfolio_assets
)
from portfolios.tests.factories import (
    PortfolioFactory,
    AssetFactory,
    HoldingFactory,
    PriceFactory
)


class PortfolioSelectorTests(TestCase):
    def setUp(self):
        self.portfolio = PortfolioFactory(name="Test Portfolio")
        self.asset = AssetFactory(name="Test Asset")
        self.date = timezone.now().date()
        
        self.holding = HoldingFactory(
            portfolio=self.portfolio,
            asset=self.asset,
            date=self.date,
            quantity=100.50
        )
        
        self.price = PriceFactory(
            asset=self.asset,
            date=self.date,
            price=10.00
        )

    def test_get_portfolio_by_id(self):
        portfolio = get_portfolio_by_id(self.portfolio.id)
        self.assertEqual(portfolio, self.portfolio)

    def test_get_portfolio_by_id_not_found(self):
        with self.assertRaises(ObjectDoesNotExist):
            get_portfolio_by_id(999)

    def test_get_portfolio_by_name(self):
        portfolio = get_portfolio_by_name("Test Portfolio")
        self.assertEqual(portfolio, self.portfolio)

    def test_get_portfolio_by_name_not_found(self):
        with self.assertRaises(ObjectDoesNotExist):
            get_portfolio_by_name("Non Existent Portfolio")

    def test_get_portfolio_assets(self):
        assets_data, latest_date = get_portfolio_assets(self.portfolio.id)
        self.assertEqual(len(assets_data), 1)
        self.assertEqual(assets_data[0]["asset_id"], self.asset.id)
        self.assertEqual(assets_data[0]["asset_name"], self.asset.name)
        self.assertEqual(assets_data[0]["quantity"], self.holding.quantity)
        self.assertEqual(assets_data[0]["price"], self.price.price)
        self.assertEqual(assets_data[0]["value"], self.holding.quantity * self.price.price)
        self.assertEqual(latest_date, self.date)

    def test_get_portfolio_assets_no_holdings(self):
        portfolio = PortfolioFactory(name="Empty Portfolio")
        assets_data, latest_date = get_portfolio_assets(portfolio.id)
        self.assertEqual(len(assets_data), 0)
        self.assertIsNone(latest_date)

    def test_get_portfolio_assets_no_prices(self):
        portfolio = PortfolioFactory(name="Portfolio No Prices")
        asset = AssetFactory(name="Asset No Price")
        HoldingFactory(
            portfolio=portfolio,
            asset=asset,
            date=self.date,
            quantity=100.50
        )
        assets_data, latest_date = get_portfolio_assets(portfolio.id)
        self.assertEqual(len(assets_data), 0)
        self.assertIsNone(latest_date)
