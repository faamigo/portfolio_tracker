from django.core.management.base import BaseCommand
from portfolios.management.utils.excel_loader import load_data_from_excel
import os


class Command(BaseCommand):
    """
    Load data from Excel file.
    Arguments:
        --excel-file: Path to Excel file containing the data to load
    """
    help = 'Load data from Excel file'

    def add_arguments(self, parser):
        parser.add_argument(
            '--excel-file',
            type=str,
            required=True,
            help='Path to Excel file containing the data to load'
        )

    def handle(self, **options):
        excel_path = options['excel_file']
        
        if not os.path.exists(excel_path):
            self.stdout.write(self.style.WARNING(f'Excel file not found: {excel_path}'))
            return

        try:
            load_data_from_excel(excel_path)
            self.stdout.write(self.style.SUCCESS('Data loaded successfully from Excel'))
        except Exception as e:
            self.stdout.write(
                self.style.ERROR(f'Error loading data from Excel: {str(e)}')
            )
