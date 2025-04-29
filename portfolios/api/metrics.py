from rest_framework.views import APIView
from rest_framework import serializers, status
from rest_framework.response import Response
from rest_framework.request import Request
from portfolios.api.pagination import StandardResultsSetPagination
from portfolios.services.metrics_service import get_portfolio_metrics


class PortfolioMetricsApi(APIView):
    class InputSerializer(serializers.Serializer):
        start_date = serializers.DateField()
        end_date = serializers.DateField()

    class OutputSerializer(serializers.Serializer):
        date = serializers.DateField()
        total_value = serializers.DecimalField(max_digits=20, decimal_places=2)
        weights = serializers.DictField()
    
    pagination_class = StandardResultsSetPagination
    
    def get(self, request: Request, portfolio_id: int) -> Response:
        input_serializer = self.InputSerializer(data=request.query_params)
        input_serializer.is_valid(raise_exception=True)

        start_date = input_serializer.validated_data['start_date']
        end_date = input_serializer.validated_data['end_date']

        try:
            metrics = get_portfolio_metrics(portfolio_id, start_date, end_date)
            output_serializer = self.OutputSerializer(metrics, many=True)
            
            paginator = self.pagination_class()
            paginated_data = paginator.paginate_queryset(output_serializer.data, request)
            return paginator.get_paginated_response(paginated_data)
            
        except ValueError as e:
            return Response(
                {"error": str(e)}, 
                status=status.HTTP_400_BAD_REQUEST
            ) 
