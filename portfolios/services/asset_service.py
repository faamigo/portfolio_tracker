from portfolios.models import Asset
import logging

logger = logging.getLogger(__name__)

def create_asset(name: str) -> Asset:
    logger.debug(f"Creating asset with name '{name}'")
    if Asset.objects.filter(name=name).exists():
        error_msg = f"Asset with name '{name}' already exists"
        logger.warning(error_msg)
        raise ValueError(error_msg)
    
    asset = Asset.objects.create(name=name)
    logger.info(f"Created asset: {asset}")
    return asset
