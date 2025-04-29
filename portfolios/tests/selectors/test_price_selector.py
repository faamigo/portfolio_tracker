from django.test import TestCase
from django.utils import timezone
from django.core.exceptions import ObjectDoesNotExist
from portfolios.selectors.price_selector import (
    get_prices_by_date_range,
    get_latest_price,
    get_price_by_date
)
from portfolios.tests.factories import (
    AssetFactory,
    PriceFactory
)


class PriceSelectorTests(TestCase):
    def setUp(self):
        self.asset = AssetFactory(name="Test Asset")
        self.date1 = timezone.now().date()
        self.date2 = self.date1 + timezone.timedelta(days=1)
        self.date3 = self.date2 + timezone.timedelta(days=1)

        self.price1 = PriceFactory(
            asset=self.asset,
            date=self.date1,
            price=100.50
        )
        self.price2 = PriceFactory(
            asset=self.asset,
            date=self.date2,
            price=105.50
        )
        self.price3 = PriceFactory(
            asset=self.asset,
            date=self.date3,
            price=110.50
        )

    def test_get_price_by_date(self):
        price = get_price_by_date(self.asset.id, self.date1)
        self.assertEqual(price, self.price1)

    def test_get_price_by_date_not_found(self):
        with self.assertRaises(ObjectDoesNotExist):
            get_price_by_date(
                self.asset.id,
                self.date1 + timezone.timedelta(days=10)
            )

    def test_get_latest_price(self):
        price = get_latest_price(self.asset)
        self.assertEqual(price, self.price3)

    def test_get_latest_price_not_found(self):
        asset = AssetFactory(name="Asset No Price")
        with self.assertRaises(ObjectDoesNotExist):
            get_latest_price(asset)

    def test_get_prices_by_date_range(self):
        prices = get_prices_by_date_range(
            [self.asset.id],
            self.date1,
            self.date2
        )
        self.assertEqual(len(prices), 2)
        self.assertIn(self.price1, prices)
        self.assertIn(self.price2, prices)

        prices = get_prices_by_date_range(
            [self.asset.id],
            self.date2
        )
        self.assertEqual(len(prices), 2)
        self.assertIn(self.price2, prices)
        self.assertIn(self.price3, prices)

        prices = get_prices_by_date_range(
            [self.asset.id],
            end_date=self.date2
        )
        self.assertEqual(len(prices), 2)
        self.assertIn(self.price1, prices)
        self.assertIn(self.price2, prices)
