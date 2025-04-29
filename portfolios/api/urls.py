from django.urls import path
from .metrics import PortfolioMetricsApi
from .asset import (
    PortfolioAssetsApi,
    BuyAssetApi,
    SellAssetApi,
)
from .portfolio import (
    PortfolioApi,
    PortfolioDetailApi,
    PortfolioHoldingsApi,
    PortfolioWeightsApi,
    RebalancePortfolioApi
)


urlpatterns = [
    path('portfolios/', PortfolioApi.as_view(), name='portfolio-list'),
    path('portfolios/<int:pk>/', PortfolioDetailApi.as_view(), name='portfolio-detail'),
    path('portfolios/<int:portfolio_id>/assets/', PortfolioAssetsApi.as_view(), name='portfolio-assets'),
    path('portfolios/<int:portfolio_id>/holdings/', PortfolioHoldingsApi.as_view(), name='portfolio-holdings'),
    path('portfolios/<int:portfolio_id>/weights/', PortfolioWeightsApi.as_view(), name='portfolio-weights'),
    path('portfolios/<int:portfolio_id>/metrics/', PortfolioMetricsApi.as_view(), name='portfolio-metrics'),
    path('portfolios/<int:portfolio_id>/assets/<int:asset_id>/buy/', BuyAssetApi.as_view(), name='buy-asset'),
    path('portfolios/<int:portfolio_id>/assets/<int:asset_id>/sell/', SellAssetApi.as_view(), name='sell-asset'),
    path('portfolios/<int:portfolio_id>/rebalance/', RebalancePortfolioApi.as_view(), name='execute-sell-buy-and-metrics'),
]
