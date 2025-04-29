from django.views.generic import TemplateView
from rest_framework import serializers
from portfolios.services.visualization_service import get_portfolio_metrics_plot
from portfolios.selectors.portfolio_selector import get_portfolio_by_id

class PortfolioMetricsPlotView(TemplateView):
    template_name = 'portfolio/metrics_plot.html'

    class QueryParamsSerializer(serializers.Serializer):
        start_date = serializers.DateField(required=True)
        end_date = serializers.DateField(required=True)

    def get_context_data(self, **kwargs):
        portfolio_id = kwargs['portfolio_id']
        portfolio = get_portfolio_by_id(portfolio_id)
        
        serializer = self.QueryParamsSerializer(data=self.request.GET)
        serializer.is_valid(raise_exception=True)
        
        start_date = serializer.validated_data.get('start_date')
        end_date = serializer.validated_data.get('end_date')
        
        plot_div = get_portfolio_metrics_plot(portfolio_id, start_date, end_date)
        
        return {
            'plot_div': plot_div,
            'portfolio_name': portfolio.name
        }
