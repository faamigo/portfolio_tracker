from decimal import Decimal
from django.db import transaction
from django.db.models import Q
from portfolios.models import Weight, Portfolio, Asset
from datetime import datetime, date
import logging

logger = logging.getLogger(__name__)

def create_weight(portfolio: Portfolio, asset: Asset, date: date, weight: float) -> Weight:
    logger.debug(f"Creating weight for portfolio '{portfolio.name}', asset '{asset.name}' on {date}")
    if not 0 <= weight <= 1:
        error_msg = "Weight must be between 0 and 1"
        logger.error(error_msg)
        raise ValueError(error_msg)
    
    if Weight.objects.filter(portfolio=portfolio, asset=asset, date=date).exists():
        error_msg = f"Weight already exists for asset {asset.name} in portfolio {portfolio.name} on {date}"
        logger.warning(error_msg)
        raise ValueError(error_msg)
    
    weight_obj = Weight.objects.create(portfolio=portfolio, asset=asset, date=date, weight=weight)
    logger.info(f"Created weight: {weight_obj}")
    return weight_obj
