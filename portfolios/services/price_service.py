from datetime import datetime, date
from decimal import Decimal
from portfolios.models import Price, Asset
import logging

logger = logging.getLogger(__name__)

def create_price(asset: Asset, date: datetime, price: Decimal) -> Price:
    logger.debug(f"Creating price for asset '{asset.name}' on {date}")
    if price <= 0:
        error_msg = "Price must be positive"
        logger.error(error_msg)
        raise ValueError(error_msg)
    
    if Price.objects.filter(asset=asset, date=date).exists():
        error_msg = f"Price already exists for asset {asset.name} on {date}"
        logger.warning(error_msg)
        raise ValueError(error_msg)
    
    price_obj = Price.objects.create(asset=asset, date=date, price=price)
    logger.info(f"Created price: {price_obj}")
    return price_obj
