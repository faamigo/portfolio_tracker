from portfolios.models import Price, Asset
from datetime import date
import logging

logger = logging.getLogger(__name__)

def get_prices_by_date_range(asset_ids: list[int], start_date: date, end_date: date) -> list[Price]:
    logger.debug(f"Getting prices for assets {asset_ids} from {start_date} to {end_date}")
    prices = Price.objects.filter(
        asset_id__in=asset_ids,
        date__range=(start_date, end_date)
    ).order_by('date')
    logger.debug(f"Found {prices.count()} prices")
    return prices

def get_latest_price(asset: Asset) -> Price:
    logger.debug(f"Getting latest price for asset '{asset.name}'")
    price = Price.objects.filter(
        asset=asset
    ).order_by('-date').first()
    logger.debug(f"Found price: {price}")
    if not price:
        error_msg = f"Price not found for asset '{asset.name}'"
        logger.error(error_msg)
        raise Price.DoesNotExist(error_msg)
    return price

def get_price_by_date(asset: Asset, date: date) -> Price:
    logger.debug(f"Getting price for asset '{asset.name}' on {date}")
    try:
        price = Price.objects.get(asset=asset, date=date)
        logger.debug(f"Found price: {price}")
        return price
    except Price.DoesNotExist:
        error_msg = f"Price not found for asset '{asset.name}' on {date}"
        logger.error(error_msg)
        raise Price.DoesNotExist(error_msg)
