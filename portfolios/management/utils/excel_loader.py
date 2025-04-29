import pandas as pd
from decimal import Decimal, InvalidOperation
from portfolios.selectors.asset_selector import get_asset_by_name
from portfolios.services.asset_service import create_asset
from portfolios.services.portfolio_service import create_portfolio
from portfolios.selectors.portfolio_selector import get_portfolio_by_name
from portfolios.services.weight_service import create_weight
from portfolios.services.price_service import create_price
import logging

logger = logging.getLogger(__name__)

def load_data_from_excel(file_path: str) -> None:
    logger.info(f"Loading data from Excel file: {file_path}")
    df_weights = pd.read_excel(file_path, sheet_name="weights")
    df_weights['date'] = pd.to_datetime(df_weights['date'], dayfirst=True)
    logger.debug(f"Loaded weights data: {len(df_weights)} rows")
    
    df_prices = pd.read_excel(file_path, sheet_name="prices")
    df_prices.set_index('date', inplace=True)
    logger.debug(f"Loaded prices data: {len(df_prices)} rows")
    
    assets = create_assets(df_weights['asset'].unique())
    portfolios = create_portfolios(df_weights.columns[2:])
    
    create_prices(df_prices)
    create_weights(df_weights, portfolios, assets)
    logger.info("Data loading completed successfully")

def create_assets(asset_names: list[str]) -> dict:
    logger.debug(f"Creating assets from names: {asset_names}")
    assets = {}
    for name in asset_names:
        try:
            asset = create_asset(name)
            logger.info(f"Created new asset: {asset}")
        except ValueError as e:
            logger.warning(f"Asset already exists: {str(e)}")
            asset = get_asset_by_name(name)
            logger.info(f"Retrieved existing asset: {asset}")
        assets[name] = asset
    logger.info(f"Processed {len(assets)} assets")
    return assets

def create_portfolios(portfolio_names: list[str]) -> dict:
    logger.debug(f"Creating portfolios from names: {portfolio_names}")
    portfolios = {}
    for name in portfolio_names:
        normalized_name = name.strip().lower()
        logger.debug(f"Processing portfolio: '{normalized_name}'")
        try:
            portfolio = create_portfolio(normalized_name)
            logger.info(f"Created new portfolio: {portfolio}")
        except ValueError as e:
            logger.warning(f"Portfolio already exists: {str(e)}")
            portfolio = get_portfolio_by_name(normalized_name)
            logger.info(f"Retrieved existing portfolio: {portfolio}")
        portfolios[normalized_name] = portfolio
    logger.info(f"Processed {len(portfolios)} portfolios")
    return portfolios

def create_prices(df_prices: pd.DataFrame) -> None:
    logger.debug(f"Creating prices for {len(df_prices)} dates")
    for date, row in df_prices.iterrows():
        for asset_name, price in row.items():
            try:
                price_value = Decimal(str(price))
                asset = get_asset_by_name(asset_name)
                try:
                    create_price(asset, date, price_value)
                    logger.debug(f"Created price for {asset_name} on {date}: {price_value}")
                except ValueError as e:
                    logger.info(f"Skipping existing price: {str(e)}")
            except (ValueError, TypeError, InvalidOperation):
                logger.warning(f"Invalid price value for {asset_name} on {date}: {price}")
    logger.info(f"Price creation completed for {len(df_prices)} dates")

def create_weights(df_weights: pd.DataFrame, portfolios: dict, assets: dict) -> None:
    logger.debug(f"Creating weights for {len(df_weights)} rows")
    portfolio_columns = [col for col in df_weights.columns if col not in ['date', 'asset']]
    
    for _, row in df_weights.iterrows():
        date = row['date']
        asset_name = row['asset']
        asset = assets[asset_name]

        for portfolio_name in portfolio_columns:
            weight_value = row[portfolio_name]
            if pd.notna(weight_value):
                try:
                    weight_decimal = Decimal(str(weight_value))
                    try:
                        create_weight(portfolios[portfolio_name], asset, date, weight_decimal)
                        logger.debug(f"Created weight for {asset_name} in {portfolio_name} on {date}: {weight_decimal}")
                    except ValueError as e:
                        logger.info(f"Skipping existing weight: {str(e)}")
                except (ValueError, TypeError, InvalidOperation):
                    logger.warning(f"Invalid weight value for {asset_name} in {portfolio_name} on {date}: {weight_value}")
    logger.info(f"Weight creation completed for {len(df_weights)} rows")
