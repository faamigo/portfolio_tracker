from django.core.management.base import BaseCommand
from portfolios.services.holding_service import create_initial_holdings
from portfolios.services.portfolio_service import update_portfolio
from portfolios.selectors.portfolio_selector import get_portfolio_by_name
from datetime import date, datetime
import csv
import os
import sys
from typing import Dict, Any
from django.core.exceptions import ValidationError


class Command(BaseCommand):
    """
    Setup portfolios with initial values and create initial holdings.
    
    This command:
    1. Sets initial values for portfolios
    2. Creates initial holdings for each portfolio
    
    Arguments:
        --csv-file: Path to CSV file containing portfolio names and initial values
        --date: Date in YYYY-MM-DD format (defaults to today)
    """
    help = 'Setup portfolios with initial values and create initial holdings'

    def add_arguments(self, parser):
        parser.add_argument(
            '--csv-file',
            type=str,
            required=True,
            help='Path to CSV file containing portfolio names and initial values. CSV should have columns: portfolio_name,initial_value'
        )
        parser.add_argument(
            '--date',
            type=str,
            help='Date in YYYY-MM-DD format. Defaults to today if not provided.'
        )

    def _validate_portfolio_values(self, portfolio_values: Dict[str, Any]) -> None:
        if not isinstance(portfolio_values, dict):
            raise ValidationError("Portfolio values must be a dictionary")
        
        for name, value in portfolio_values.items():
            if not isinstance(name, str):
                raise ValidationError("Portfolio names must be strings")
            if not isinstance(value, (int, float)):
                raise ValidationError("Portfolio values must be numbers")

    def _read_csv_file(self, file_path: str) -> Dict[str, float]:
        if not os.path.exists(file_path):
            raise ValidationError(f"CSV file not found: {file_path}")

        portfolio_values = {}
        try:
            with open(file_path, 'r') as csvfile:
                reader = csv.DictReader(csvfile)
                for row in reader:
                    try:
                        portfolio_name = row['portfolio_name'].strip()
                        initial_value = float(row['initial_value'])
                        portfolio_values[portfolio_name] = initial_value
                    except KeyError:
                        raise ValidationError("CSV file must contain 'portfolio_name' and 'initial_value' columns")
                    except ValueError:
                        raise ValidationError(f"Invalid initial value for portfolio '{portfolio_name}'")
        except csv.Error as e:
            raise ValidationError(f"Error reading CSV file: {str(e)}")

        if not portfolio_values:
            raise ValidationError("No portfolio values found in CSV file")

        return portfolio_values

    def handle(self, **options):
        try:
            portfolio_values = self._read_csv_file(options['csv_file'])
            self._validate_portfolio_values(portfolio_values)
            
            initial_date = (
                datetime.strptime(options['date'], '%Y-%m-%d').date() 
                if options['date'] 
                else date.today()
            )
            
            for portfolio_name, initial_value in portfolio_values.items():
                normalized_name = portfolio_name.strip().lower()
                self.stdout.write(f"Searching portfolio with name: '{normalized_name}'")
                portfolio = get_portfolio_by_name(normalized_name)
                
                if not portfolio:
                    self.stdout.write(
                        self.style.WARNING(f'Portfolio "{portfolio_name}" not found')
                    )
                    continue
                
                self.stdout.write(f"Found portfolio: {portfolio}")
                updated_portfolio = update_portfolio(portfolio.id, {'initial_value': initial_value})
                try:
                    create_initial_holdings(updated_portfolio, initial_date)
                    self.stdout.write(
                        self.style.SUCCESS(f'Initial holdings created for portfolio "{portfolio_name}"')
                    )
                except ValueError as e:
                    error_msg = str(e)
                    if "Price not found" in error_msg or "No weights found" in error_msg:
                        self.stdout.write(
                            self.style.ERROR(f'Error setting up portfolios: {error_msg}')
                        )
                        sys.exit(1)
                    raise
            
            self.stdout.write(self.style.SUCCESS('Portfolios setup completed successfully'))
            
        except ValidationError as e:
            self.stdout.write(
                self.style.ERROR(f'Validation error: {str(e)}')
            )
            sys.exit(1)
        except Exception as e:
            self.stdout.write(
                self.style.ERROR(f'Error setting up portfolios: {str(e)}')
            )
            sys.exit(1)
