from django.urls import path, include
from rest_framework.routers import DefaultRouter
from portfolios.views.visualization import PortfolioMetricsPlotView

router = DefaultRouter()

urlpatterns = [
    path('api/', include(router.urls)),
    path('api/', include('portfolios.api.urls')),
    path(
        'portfolios/<int:portfolio_id>/metrics/plot/',
        PortfolioMetricsPlotView.as_view(),
        name='portfolio-metrics-plot'
    ),
] 