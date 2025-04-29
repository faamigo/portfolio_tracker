from portfolios.models import Weight, Portfolio
from datetime import date
import logging

logger = logging.getLogger(__name__)

def get_portfolio_weights_by_date(portfolio: Portfolio, date: date) -> list[Weight]:
    logger.debug(f"Getting weights for portfolio '{portfolio.name}' on {date}")
    weights = list(Weight.objects.filter(portfolio=portfolio, date=date))
    logger.debug(f"Found {len(weights)} weights")
    return weights

def get_latest_portfolio_weights(portfolio: Portfolio) -> list[Weight]:
    logger.debug(f"Getting latest weights for portfolio '{portfolio.name}'")
    weights = list(Weight.objects.filter(portfolio=portfolio).order_by('-date'))
    logger.debug(f"Found {len(weights)} weights")
    return weights
