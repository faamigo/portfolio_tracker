from portfolios.models import Holding, Portfolio, Asset
from datetime import date
import logging

logger = logging.getLogger(__name__)

def get_holdings_by_date(portfolio: Portfolio, date: date) -> list[Holding]:
    logger.debug(f"Getting holdings for portfolio '{portfolio.name}' on {date}")
    holdings = Holding.objects.filter(
        portfolio=portfolio,
        date=date,
        quantity__gt=0
    ).select_related('asset')
    logger.debug(f"Found {len(holdings)} holdings")
    return holdings

def get_asset_latest_holding_before_date(portfolio: Portfolio, asset: Asset, date: date) -> Holding:
    logger.debug(f"Getting latest holding for asset '{asset.name}' in portfolio '{portfolio.name}' before {date}")
    try:
        holding = Holding.objects.filter(
            portfolio=portfolio,
            asset=asset,
            date__lte=date
        ).order_by('-date').first()
        logger.debug(f"Found holding: {holding}")
        return holding
    except Holding.DoesNotExist:
        error_msg = f"No holdings found for asset '{asset.name}' in portfolio '{portfolio.name}' before {date}"
        logger.error(error_msg)
        raise Holding.DoesNotExist(error_msg)

def get_latest_portfolio_holdings(portfolio: Portfolio) -> list[Holding]:
    logger.debug(f"Getting latest holdings for portfolio '{portfolio.name}'")
    holdings = Holding.objects.filter(
        portfolio=portfolio
    ).select_related('asset')
    logger.debug(f"Found {len(holdings)} holdings")
    return holdings

def get_first_portfolio_holding(portfolio: Portfolio) -> Holding:
    logger.debug(f"Getting first holding for portfolio '{portfolio.name}'")
    try:
        holding = Holding.objects.filter(
            portfolio=portfolio
        ).order_by('date').first()
        logger.debug(f"Found holding: {holding}")
        return holding
    except Holding.DoesNotExist:
        error_msg = f"No holdings found for portfolio '{portfolio.name}'"
        logger.error(error_msg)
        raise Holding.DoesNotExist(error_msg)
