from datetime import datetime
from decimal import Decimal
from django.db import transaction
from portfolios.models import Portfolio
from portfolios.selectors.portfolio_selector import get_portfolio_by_id
from portfolios.selectors.asset_selector import get_asset_by_id
from portfolios.selectors.holding_selector import get_asset_latest_holding_before_date
from portfolios.selectors.price_selector import get_price_by_date
from portfolios.services.holding_service import create_holding, update_holding
from portfolios.services.metrics_service import get_portfolio_metrics
import logging

logger = logging.getLogger(__name__)

def create_portfolio(name: str, initial_value: float = 0) -> Portfolio:
    logger.debug(f"Creating portfolio with name '{name}', initial_value {initial_value}")
    if Portfolio.objects.filter(name=name).exists():
        error_msg = f"Portfolio with name '{name}' already exists"
        logger.warning(error_msg)
        raise ValueError(error_msg)
    
    portfolio = Portfolio.objects.create(name=name, initial_value=initial_value)
    logger.info(f"Created portfolio: {portfolio}")
    return portfolio

def update_portfolio(portfolio_id: int, new_data: dict) -> Portfolio:
    logger.debug(f"Updating portfolio with id {portfolio_id} with data: {new_data}")
    try:
        portfolio = get_portfolio_by_id(portfolio_id)
        for key, value in new_data.items():
            setattr(portfolio, key, value)
        portfolio.save()
        logger.info(f"Updated portfolio: {portfolio}")
        return portfolio
    except Portfolio.DoesNotExist:
        error_msg = f"Portfolio with id '{portfolio_id}' not found"
        logger.error(error_msg)
        raise Portfolio.DoesNotExist(error_msg)

def execute_buy_transaction(
    portfolio_id: int,
    asset_id: int,
    amount: Decimal,
    date: datetime
) -> dict:
    logger.debug(f"Executing buy transaction for portfolio {portfolio_id}, asset {asset_id}, amount {amount} on {date}")
    portfolio = get_portfolio_by_id(portfolio_id)
    asset = get_asset_by_id(asset_id)
    
    price = get_price_by_date(asset, date).price
    quantity = amount / price

    with transaction.atomic():
        latest_holding = get_asset_latest_holding_before_date(portfolio, asset, date)
        if not latest_holding:
            holding = create_holding(portfolio, asset, date, quantity)
            logger.info(f"Created new holding for buy transaction: {holding}")
        else:
            current_quantity = latest_holding.quantity
            new_quantity = current_quantity + quantity
            update_holding(latest_holding, {'quantity': new_quantity})
            logger.info(f"Updated holding for buy transaction: {latest_holding}")

    result = {
        "message": "Purchase successful",
        "portfolio_id": portfolio_id,
        "asset_id": asset_id,
        "quantity": quantity,
        "price": price,
        "total": amount
    }
    logger.info(f"Buy transaction completed: {result}")
    return result

def execute_sell_transaction(
    portfolio_id: int,
    asset_id: int,
    amount: Decimal,
    date: datetime
) -> dict:
    logger.debug(f"Executing sell transaction for portfolio {portfolio_id}, asset {asset_id}, amount {amount} on {date}")
    portfolio = get_portfolio_by_id(portfolio_id)
    asset = get_asset_by_id(asset_id)
    
    price = get_price_by_date(asset, date).price
    quantity = amount / price

    with transaction.atomic():
        latest_holding = get_asset_latest_holding_before_date(portfolio, asset, date)
        current_quantity = latest_holding.quantity

        if current_quantity < quantity or not latest_holding:
            error_msg = f"Insufficient quantity. Available: {current_quantity}, Requested: {quantity}"
            logger.error(error_msg)
            raise ValueError(error_msg)

        new_quantity = current_quantity - quantity
        update_holding(latest_holding, {'quantity': new_quantity})
        logger.info(f"Updated holding for sell transaction: {latest_holding}")

    result = {
        "message": "Sale successful",
        "portfolio_id": portfolio_id,
        "asset_id": asset_id,
        "quantity": quantity,
        "price": price,
        "total": amount
    }
    logger.info(f"Sell transaction completed: {result}")
    return result

def rebalance_portfolio(
    portfolio_id: int,
    sell_asset_id: int,
    buy_asset_id: int,
    sell_amount: Decimal,
    buy_amount: Decimal,
    start_date: datetime,
    end_date: datetime = None
) -> dict:
    logger.debug(f"Rebalancing portfolio {portfolio_id}: selling {sell_amount} of asset {sell_asset_id}, buying {buy_amount} of asset {buy_asset_id}")
    sell_asset = get_asset_by_id(sell_asset_id)
    buy_asset = get_asset_by_id(buy_asset_id)
    
    if sell_amount <= 0 or buy_amount <= 0:
        error_msg = "Amounts must be positive"
        logger.error(error_msg)
        raise ValueError(error_msg)
    
    sell_price = get_price_by_date(sell_asset, start_date).price
    sell_quantity = sell_amount / sell_price
    sell_response = execute_sell_transaction(portfolio_id, sell_asset.id, sell_quantity, start_date)
    
    buy_price = get_price_by_date(buy_asset, start_date).price
    buy_quantity = buy_amount / buy_price
    buy_response = execute_buy_transaction(portfolio_id, buy_asset.id, buy_quantity, start_date)
    
    metrics = get_portfolio_metrics(portfolio_id, start_date, end_date)
    
    result = {
        "sell_transaction": sell_response,
        "buy_transaction": buy_response,
        "metrics": metrics
    }
    logger.info(f"Rebalancing completed: {result['buy_transaction'], result['sell_transaction'], len(result['metrics'])}")
    return result
