from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse
from portfolios.tests.factories import PortfolioFactory, AssetFactory, PriceFactory, HoldingFactory
from datetime import datetime


class AssetsAPITests(APITestCase):
    def setUp(self):
        self.portfolio = PortfolioFactory()
        self.asset = AssetFactory()
        self.price = PriceFactory(asset=self.asset)
        self.holding = HoldingFactory(portfolio=self.portfolio, asset=self.asset)
        self.assets_url = reverse('portfolio-assets', args=[self.portfolio.id])
        self.buy_url = reverse('portfolio-buy-asset', args=[self.portfolio.id, self.asset.id])
        self.sell_url = reverse('portfolio-sell-asset', args=[self.portfolio.id, self.asset.id])

    def test_get_portfolio_assets(self):
        response = self.client.get(self.assets_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('assets', response.data)
        self.assertIn('date', response.data)
        self.assertIn('portfolio_id', response.data)

    def test_buy_asset(self):
        data = {
            'amount': 1000.00,
            'date': datetime.now().date()
        }
        response = self.client.post(self.buy_url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('message', response.data)
        self.assertIn('quantity', response.data)
        self.assertIn('price', response.data)
        self.assertIn('total', response.data)

    def test_buy_asset_without_date(self):
        data = {
            'amount': 1000.00
        }
        response = self.client.post(self.buy_url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_buy_asset_with_invalid_amount(self):
        data = {
            'amount': -1000.00,
            'date': datetime.now().date()
        }
        response = self.client.post(self.buy_url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_sell_asset(self):
        data = {
            'amount': 500.00,
            'date': datetime.now().date()
        }
        response = self.client.post(self.sell_url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('message', response.data)
        self.assertIn('quantity', response.data)
        self.assertIn('price', response.data)
        self.assertIn('total', response.data)

    def test_sell_asset_without_date(self):
        data = {
            'amount': 500.00
        }
        response = self.client.post(self.sell_url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_sell_asset_with_invalid_amount(self):
        data = {
            'amount': -500.00,
            'date': datetime.now().date()
        }
        response = self.client.post(self.sell_url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
