from portfolios.models import Asset
import logging

logger = logging.getLogger(__name__)

def get_asset_by_id(asset_id: int) -> Asset:
    logger.debug(f"Getting asset by id: {asset_id}")
    try:
        asset = Asset.objects.get(id=asset_id)
        logger.debug(f"Found asset: {asset}")
        return asset
    except Asset.DoesNotExist:
        error_msg = f"Asset with id {asset_id} not found"
        logger.error(error_msg)
        raise Asset.DoesNotExist(error_msg)

def get_asset_by_name(name: str) -> Asset:
    logger.debug(f"Getting asset by name: {name}")
    try:
        asset = Asset.objects.get(name=name)
        logger.debug(f"Found asset: {asset}")
        return asset
    except Asset.DoesNotExist:
        error_msg = f"Asset with name '{name}' not found"
        logger.error(error_msg)
        raise Asset.DoesNotExist(error_msg)
