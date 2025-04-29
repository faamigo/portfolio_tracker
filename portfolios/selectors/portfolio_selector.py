from portfolios.models import Portfolio
from portfolios.selectors.holding_selector import get_latest_portfolio_holdings
from portfolios.selectors.price_selector import get_latest_price
from datetime import datetime
from portfolios.models import Price
import logging

logger = logging.getLogger(__name__)


def get_portfolio_by_id(portfolio_id: int) -> Portfolio:
    logger.debug(f"Getting portfolio by id: {portfolio_id}")
    try:
        portfolio = Portfolio.objects.get(id=portfolio_id)
        logger.debug(f"Found portfolio: {portfolio}")
        return portfolio
    except Portfolio.DoesNotExist:
        error_msg = f"Portfolio with id '{portfolio_id}' not found"
        logger.error(error_msg)
        raise Portfolio.DoesNotExist(error_msg)

def get_portfolio_by_name(name: str) -> Portfolio:
    logger.debug(f"Getting portfolio by name: {name}")
    try:
        portfolio = Portfolio.objects.get(name=name)
        logger.debug(f"Found portfolio: {portfolio}")
        return portfolio
    except Portfolio.DoesNotExist:
        error_msg = f"Portfolio with name '{name}' not found"
        logger.error(error_msg)
        raise Portfolio.DoesNotExist(error_msg)
    
def get_portfolio_assets(portfolio_id: int) -> tuple[list, datetime]:
    logger.debug(f"Getting portfolio assets for portfolio: {portfolio_id}")
    portfolio = get_portfolio_by_id(portfolio_id)
    holdings = get_latest_portfolio_holdings(portfolio)
    
    if not holdings:
        logger.warning(f"No holdings found for portfolio: {portfolio_id}")
        return [], None

    assets_data = []
    for holding in holdings:
        try:
            latest_price = get_latest_price(holding.asset)
            
            if latest_price:
                assets_data.append({
                    "asset_id": holding.asset.id,
                    "asset_name": holding.asset.name,
                    "quantity": holding.quantity,
                    "price": latest_price.price,
                    "value": holding.quantity * latest_price.price,
                    "date": latest_price.date
                })
        except Price.DoesNotExist:
            continue
    
    logger.debug(f"Found {len(assets_data)} assets for portfolio: {portfolio_id}")

    return assets_data, latest_price.date if latest_price else None
