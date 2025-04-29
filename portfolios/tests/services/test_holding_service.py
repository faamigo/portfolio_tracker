from django.test import TestCase
from django.utils import timezone
from portfolios.services.holding_service import (
    create_holding,
    update_holding,
    create_initial_holdings
)
from portfolios.tests.factories import (
    PortfolioFactory,
    AssetFactory,
    PriceFactory,
    WeightFactory,
    HoldingFactory
)


class HoldingServiceTests(TestCase):
    def setUp(self):
        self.portfolio = PortfolioFactory(name="Test Portfolio")
        self.asset = AssetFactory(name="Test Asset")
        self.date = timezone.now().date()
        self.price = PriceFactory(
            asset=self.asset,
            date=self.date,
            price=100.00
        )

    def test_create_holding(self):
        holding = create_holding(
            portfolio=self.portfolio,
            asset=self.asset,
            date=self.date,
            quantity=100.50
        )
        self.assertEqual(holding.portfolio, self.portfolio)
        self.assertEqual(holding.asset, self.asset)
        self.assertEqual(holding.quantity, 100.50)

    def test_create_holding_duplicate(self):
        HoldingFactory(
            portfolio=self.portfolio,
            asset=self.asset,
            date=self.date,
            quantity=100.50
        )
        with self.assertRaises(ValueError):
            create_holding(
                portfolio=self.portfolio,
                asset=self.asset,
                date=self.date,
                quantity=200.50
            )

    def test_update_holding(self):
        holding = HoldingFactory(
            portfolio=self.portfolio,
            asset=self.asset,
            date=self.date,
            quantity=100.50
        )
        updated_holding = update_holding(holding, {"quantity": 200.50})
        self.assertEqual(updated_holding.quantity, 200.50)

    def test_create_initial_holdings(self):
        weight = WeightFactory(
            portfolio=self.portfolio,
            asset=self.asset,
            date=self.date,
            weight=0.5
        )
        holdings = create_initial_holdings(self.portfolio, self.date)
        self.assertEqual(len(holdings), 1)
        self.assertEqual(holdings[0].portfolio, self.portfolio)
        self.assertEqual(holdings[0].asset, self.asset)
        self.assertEqual(float(holdings[0].quantity), 5.0)

    def test_create_initial_holdings_no_weights(self):
        with self.assertRaises(ValueError):
            create_initial_holdings(self.portfolio, self.date)

    def test_create_initial_holdings_no_prices(self):
        weight = WeightFactory(
            portfolio=self.portfolio,
            asset=self.asset,
            date=self.date,
            weight=0.5
        )
        self.price.delete()
        with self.assertRaises(ValueError):
            create_initial_holdings(self.portfolio, self.date)
