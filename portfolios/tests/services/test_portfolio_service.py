from django.test import TestCase
from django.core.exceptions import ValidationError
from django.utils import timezone
from decimal import Decimal
from portfolios.services.portfolio_service import (
    create_portfolio,
    update_portfolio,
    execute_buy_transaction,
    execute_sell_transaction,
    rebalance_portfolio
)
from portfolios.tests.factories import (
    PortfolioFactory,
    AssetFactory,
    PriceFactory,
    HoldingFactory
)


class PortfolioServiceTests(TestCase):
    def setUp(self):
        self.portfolio = PortfolioFactory(name="Test Portfolio")
        self.asset1 = AssetFactory(name="Test Asset 1")
        self.asset2 = AssetFactory(name="Test Asset 2")
        self.date = timezone.now().date()
        self.price = PriceFactory(
            asset=self.asset1,
            date=self.date,
            price=100.00
        )
        self.price2 = PriceFactory(
            asset=self.asset2,
            date=self.date,
            price=50.00
        )

    def test_create_portfolio(self):
        portfolio = create_portfolio(
            name="New Portfolio",
            initial_value=2000.00
        )
        self.assertEqual(portfolio.name, "New Portfolio")
        self.assertEqual(float(portfolio.initial_value), 2000.00)

    def test_create_portfolio_duplicate_name(self):
        with self.assertRaises(ValueError):
            create_portfolio(name="Test Portfolio")

    def test_update_portfolio(self):
        updated_data = {
            "name": "Updated Portfolio",
            "initial_value": 1500.00
        }
        portfolio = update_portfolio(self.portfolio.id, updated_data)
        self.assertEqual(portfolio.name, "Updated Portfolio")
        self.assertEqual(float(portfolio.initial_value), 1500.00)

    def test_update_portfolio_not_found(self):
        with self.assertRaises(ValidationError):
            update_portfolio(999, {"name": "Not Found"})

    def test_execute_buy_transaction(self):
        result = execute_buy_transaction(
            portfolio_id=self.portfolio.id,
            asset_id=self.asset1.id,
            amount=Decimal("1000.00"),
            date=self.date
        )
        self.assertEqual(result["portfolio_id"], self.portfolio.id)
        self.assertEqual(result["asset_id"], self.asset1.id)
        self.assertEqual(float(result["quantity"]), 10.00)
        self.assertEqual(float(result["price"]), 100.00)
        self.assertEqual(float(result["total"]), 1000.00)

    def test_execute_buy_transaction_no_price(self):
        asset = AssetFactory(name="No Price Asset")
        with self.assertRaises(ValidationError):
            execute_buy_transaction(
                portfolio_id=self.portfolio.id,
                asset_id=asset.id,
                amount=Decimal("1000.00"),
                date=self.date
            )

    def test_execute_sell_transaction(self):
        holding = HoldingFactory(
            portfolio=self.portfolio,
            asset=self.asset1,
            date=self.date,
            quantity=20.00
        )

        result = execute_sell_transaction(
            portfolio_id=self.portfolio.id,
            asset_id=self.asset1.id,
            amount=Decimal("1000.00"),
            date=self.date
        )
        self.assertEqual(result["portfolio_id"], self.portfolio.id)
        self.assertEqual(result["asset_id"], self.asset1.id)
        self.assertEqual(float(result["quantity"]), 10.00)
        self.assertEqual(float(result["price"]), 100.00)
        self.assertEqual(float(result["total"]), 1000.00)

    def test_execute_sell_transaction_insufficient_quantity(self):
        holding = HoldingFactory(
            portfolio=self.portfolio,
            asset=self.asset1,
            date=self.date,
            quantity=5.00
        )
        with self.assertRaises(ValueError):
            execute_sell_transaction(
                portfolio_id=self.portfolio.id,
                asset_id=self.asset1.id,
                amount=Decimal("1000.00"),
                date=self.date
            )

    def test_rebalance_portfolio(self):
        holding = HoldingFactory(
            portfolio=self.portfolio,
            asset=self.asset1,
            date=self.date,
            quantity=20.00
        )

        result = rebalance_portfolio(
            portfolio_id=self.portfolio.id,
            sell_asset_id=self.asset1.id,
            buy_asset_id=self.asset2.id,
            sell_amount=Decimal("1000.00"),
            buy_amount=Decimal("1000.00"),
            start_date=self.date
        )
        
        self.assertIn("sell_transaction", result)
        self.assertIn("buy_transaction", result)
        self.assertIn("metrics", result)

    def test_rebalance_portfolio_invalid_amounts(self):
        with self.assertRaises(ValueError):
            rebalance_portfolio(
                portfolio_id=self.portfolio.id,
                sell_asset_id=self.asset1.id,
                buy_asset_id=self.asset2.id,
                sell_amount=Decimal("-1000.00"),
                buy_amount=Decimal("1000.00"),
                start_date=self.date
            )
