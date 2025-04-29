from django.test import TestCase
from django.core.exceptions import ValidationError
from portfolios.models import Portfolio

class PortfolioTests(TestCase):
    def test_portfolio_name_cannot_be_empty(self):
        portfolio = Portfolio(name="")
        with self.assertRaises(ValidationError) as context:
            portfolio.full_clean()
        self.assertIn("Portfolio name cannot be empty", str(context.exception))

    def test_portfolio_name_must_be_at_least_2_characters(self):
        portfolio = Portfolio(name="a")
        with self.assertRaises(ValidationError) as context:
            portfolio.full_clean()
        self.assertIn("Portfolio name must be at least 2 characters long", str(context.exception))

    def test_portfolio_name_cannot_be_just_whitespace(self):
        portfolio = Portfolio(name="   ")
        with self.assertRaises(ValidationError) as context:
            portfolio.full_clean()
        self.assertIn("Portfolio name cannot be empty", str(context.exception))

    def test_initial_value_must_be_positive(self):
        portfolio = Portfolio(name="Test Portfolio", initial_value=-100)
        with self.assertRaises(ValidationError) as context:
            portfolio.full_clean()
        self.assertIn("Initial value must be positive", str(context.exception))

    def test_valid_portfolio(self):
        portfolio = Portfolio(name="Test Portfolio", initial_value=1000)
        portfolio.full_clean()
        portfolio.save()
        self.assertEqual(Portfolio.objects.count(), 1)
