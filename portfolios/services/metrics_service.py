from datetime import date
from collections import defaultdict
from portfolios.selectors.holding_selector import get_holdings_by_date, get_first_portfolio_holding
from portfolios.selectors.price_selector import get_prices_by_date_range
from portfolios.selectors.portfolio_selector import get_portfolio_by_id
from portfolios.selectors.asset_selector import get_asset_by_id
import logging

logger = logging.getLogger(__name__)

def get_portfolio_metrics(portfolio_id: int, start_date: date, end_date: date) -> list[dict]:
    logger.debug(f"Getting portfolio metrics for portfolio {portfolio_id} from {start_date} to {end_date}")
    portfolio = get_portfolio_by_id(portfolio_id)
    first_holding = get_first_portfolio_holding(portfolio)
    reference_date = first_holding.date

    if start_date < reference_date:
        error_msg = "Start date must be greater than or equal to reference date"
        logger.error(error_msg)
        raise ValueError(error_msg)

    holdings = get_holdings_by_date(portfolio, reference_date)
    quantities = {h.asset.id: h.quantity for h in holdings}

    asset_ids = list(quantities.keys())
    prices = get_prices_by_date_range(asset_ids, start_date, end_date)

    prices_by_date = defaultdict(dict)
    for price in prices:
        prices_by_date[price.date][price.asset.id] = price.price

    results = []

    for date, prices_on_date in sorted(prices_by_date.items()):
        assets_value = {}
        portfolio_value = 0

        for asset_id, price in prices_on_date.items():
            quantity = quantities.get(asset_id)
            if quantity is None:
                continue
            asset_value = quantity * price
            assets_value[asset_id] = asset_value
            portfolio_value += asset_value

        weights = {}
        for asset_id, asset_value in assets_value.items():
            asset = get_asset_by_id(asset_id)
            weights[asset.name] = float(asset_value / portfolio_value)

        result = {
            "date": date,
            "total_value": float(portfolio_value),
            "weights": weights
        }
        results.append(result)
        logger.debug(f"Calculated metrics for date {date}, total value {portfolio_value}, weights length {len(weights)}")

    logger.info(f"Completed metrics calculation for portfolio {portfolio_id}: {len(results)} dates processed")
    return results
