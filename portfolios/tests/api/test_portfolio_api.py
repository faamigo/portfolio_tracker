from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse
from portfolios.tests.factories import PortfolioFactory, AssetFactory, HoldingFactory
from datetime import datetime


class PortfolioAPITests(APITestCase):
    def setUp(self):
        self.portfolio = PortfolioFactory()
        self.asset = AssetFactory()
        self.holding = HoldingFactory(portfolio=self.portfolio, asset=self.asset)
        self.list_url = reverse('portfolio-list')
        self.detail_url = reverse('portfolio-detail', args=[self.portfolio.id])
        self.holdings_url = reverse('portfolio-holdings', args=[self.portfolio.id])
        self.weights_url = reverse('portfolio-weights', args=[self.portfolio.id])
        self.rebalance_url = reverse('portfolio-rebalance', args=[self.portfolio.id])

    def test_list_portfolios(self):
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('results', response.data)
        self.assertIn('count', response.data)

    def test_create_portfolio(self):
        data = {
            'name': 'Test Portfolio',
            'initial_cash': 10000.00
        }
        response = self.client.post(self.list_url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['name'], 'Test Portfolio')

    def test_retrieve_portfolio(self):
        response = self.client.get(self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['id'], self.portfolio.id)

    def test_get_portfolio_holdings(self):
        response = self.client.get(self.holdings_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('results', response.data)
        self.assertIn('count', response.data)

    def test_get_portfolio_weights(self):
        response = self.client.get(self.weights_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('results', response.data)
        self.assertIn('count', response.data)

    def test_rebalance_portfolio(self):
        data = {
            'sell_asset_id': self.asset.id,
            'buy_asset_id': self.asset.id,
            'sell_amount': 500.00,
            'buy_amount': 500.00,
            'start_date': datetime.now().date(),
            'end_date': datetime.now().date()
        }
        response = self.client.post(self.rebalance_url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('sell_transaction', response.data)
        self.assertIn('buy_transaction', response.data)
        self.assertIn('metrics', response.data)

    def test_rebalance_portfolio_without_dates(self):
        data = {
            'sell_asset_id': self.asset.id,
            'buy_asset_id': self.asset.id,
            'sell_amount': 500.00,
            'buy_amount': 500.00
        }
        response = self.client.post(self.rebalance_url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
