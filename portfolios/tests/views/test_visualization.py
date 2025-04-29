from django.test import TestCase
from django.urls import reverse
from portfolios.tests.factories import PortfolioFactory
from datetime import datetime, timedelta


class VisualizationViewTests(TestCase):
    def setUp(self):
        self.portfolio = PortfolioFactory()
        self.end_date = datetime.now().date()
        self.start_date = self.end_date - timedelta(days=30)

    def test_metrics_plot_view(self):
        url = reverse('portfolio-metrics-plot', args=[self.portfolio.id])
        response = self.client.get(
            url,
            {
                'start_date': self.start_date,
                'end_date': self.end_date
            }
        )
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'portfolio/metrics_plot.html')
        self.assertIn('plot_div', response.context)
        self.assertIn('portfolio_id', response.context)

    def test_metrics_plot_view_without_dates(self):
        url = reverse('portfolio-metrics-plot', args=[self.portfolio.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 400)

    def test_metrics_plot_view_with_invalid_dates(self):
        url = reverse('portfolio-metrics-plot', args=[self.portfolio.id])
        response = self.client.get(
            url,
            {
                'start_date': self.end_date,
                'end_date': self.start_date
            }
        )
        self.assertEqual(response.status_code, 400)
