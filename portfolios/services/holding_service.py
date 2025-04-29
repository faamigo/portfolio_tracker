from portfolios.models import Holding, Portfolio, Asset
from datetime import date
from portfolios.models import Price
from portfolios.selectors.weight_selector import get_portfolio_weights_by_date
from portfolios.selectors.price_selector import get_price_by_date
import logging

logger = logging.getLogger(__name__)

def create_holding(portfolio: Portfolio, asset: Asset, date: date, quantity: float) -> Holding:
    logger.debug(f"Creating holding for portfolio '{portfolio.name}', asset '{asset.name}' on {date}")
    if Holding.objects.filter(portfolio=portfolio, asset=asset, date=date).exists():
        error_msg = f"Holding for portfolio '{portfolio.name}' and asset '{asset.name}' on {date} already exists"
        logger.warning(error_msg)
        raise ValueError(error_msg)
    
    holding = Holding.objects.create(
        portfolio=portfolio,
        asset=asset,
        date=date,
        quantity=quantity
    )
    logger.info(f"Created holding: {holding}")
    return holding

def update_holding(holding: Holding, new_data: dict) -> Holding:
    logger.debug(f"Updating holding {holding} with data: {new_data}")
    for key, value in new_data.items():
        setattr(holding, key, value)
    holding.save()
    logger.info(f"Updated holding: {holding}")
    return holding

def create_initial_holdings(portfolio: Portfolio, date: date) -> list[dict]:
    logger.info(f"Creating initial holdings for portfolio '{portfolio.name}' on {date}")
    holdings_created = []
    
    weights = get_portfolio_weights_by_date(portfolio, date)
    if not weights:
        error_msg = f"No weights found for portfolio '{portfolio.name}' on {date}"
        logger.error(error_msg)
        raise ValueError(error_msg)

    for weight in weights:
        asset = weight.asset
        try:
            price = get_price_by_date(asset, date).price
            logger.debug(f"Found price {price} for asset '{asset.name}' on {date}")
        except Price.DoesNotExist:
            error_msg = f"Price not found for asset '{asset.name}' on {date}"
            logger.error(error_msg)
            raise ValueError(error_msg)

        weight_float = float(weight.weight)
        initial_value_float = float(portfolio.initial_value)
        price_float = float(price)
        
        quantity = (weight_float * initial_value_float) / price_float
        logger.debug(f"Calculated quantity {quantity} for asset '{asset.name}'")
        
        try: 
            holding = create_holding(portfolio, asset, date, quantity)
            holdings_created.append(holding)
            logger.info(f"Created holding: {holding}")
        except ValueError as e:
            logger.warning(f"Skipping holding for asset '{asset.name}' on {date}: {e}")
            continue

    logger.info(f"Created {len(holdings_created)} holdings for portfolio '{portfolio.name}' on {date} using initial value ${portfolio.initial_value:,.0f}")
    return holdings_created 
