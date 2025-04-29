from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse
from portfolios.tests.factories import PortfolioFactory
from datetime import datetime, timedelta


class MetricsAPITests(APITestCase):
    def setUp(self):
        self.portfolio = PortfolioFactory()
        self.metrics_url = reverse('portfolio-metrics', args=[self.portfolio.id])
        self.end_date = datetime.now().date()
        self.start_date = self.end_date - timedelta(days=30)

    def test_get_portfolio_metrics(self):
        response = self.client.get(
            self.metrics_url,
            {
                'start_date': self.start_date,
                'end_date': self.end_date
            }
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('results', response.data)
        self.assertIn('count', response.data)
        self.assertIn('next', response.data)
        self.assertIn('previous', response.data)

    def test_get_portfolio_metrics_without_dates(self):
        response = self.client.get(self.metrics_url)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_get_portfolio_metrics_with_invalid_dates(self):
        response = self.client.get(
            self.metrics_url,
            {
                'start_date': self.end_date,
                'end_date': self.start_date
            }
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
