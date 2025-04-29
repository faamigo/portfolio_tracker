from rest_framework.views import APIView
from rest_framework import serializers, status
from rest_framework.response import Response
from datetime import datetime
from rest_framework.request import Request

from portfolios.models import Portfolio, Asset, Holding, Price
from portfolios.selectors.portfolio_selector import get_portfolio_by_id
from portfolios.selectors.holding_selector import get_latest_portfolio_holdings
from portfolios.selectors.weight_selector import get_latest_portfolio_weights
from .pagination import StandardResultsSetPagination
from portfolios.services.portfolio_service import rebalance_portfolio


class PortfolioApi(APIView):    
    class InputSerializer(serializers.Serializer):
        name = serializers.CharField(max_length=100)
        initial_cash = serializers.DecimalField(max_digits=10, decimal_places=2, min_value=0)

    class OutputSerializer(serializers.Serializer):
        id = serializers.IntegerField()
        name = serializers.CharField()
        initial_value = serializers.DecimalField(max_digits=20, decimal_places=2)
        created_at = serializers.DateTimeField()
        updated_at = serializers.DateTimeField()
    
    pagination_class = StandardResultsSetPagination

    def get(self, request: Request) -> Response:
        portfolios = Portfolio.objects.all()
        paginator = self.pagination_class()
        page = paginator.paginate_queryset(portfolios, request)
        serializer = self.OutputSerializer(page, many=True)
        return paginator.get_paginated_response(serializer.data)

class PortfolioDetailApi(APIView):
    class OutputSerializer(serializers.Serializer):
        id = serializers.IntegerField()
        name = serializers.CharField()
        initial_value = serializers.DecimalField(max_digits=20, decimal_places=2)
        created_at = serializers.DateTimeField()
        updated_at = serializers.DateTimeField()

    def get(self, request: Request, pk: int) -> Response:
        try:
            portfolio = get_portfolio_by_id(pk)
            serializer = self.OutputSerializer(portfolio)
            return Response(serializer.data)
        except Portfolio.DoesNotExist:
            return Response(
                {"error": "Portfolio not found"}, 
                status=status.HTTP_404_NOT_FOUND
            )

class PortfolioHoldingsApi(APIView):
    pagination_class = StandardResultsSetPagination

    class OutputSerializer(serializers.Serializer):
        id = serializers.IntegerField()
        portfolio_id = serializers.IntegerField()
        asset_id = serializers.IntegerField()
        quantity = serializers.DecimalField(max_digits=20, decimal_places=4)
        date = serializers.DateField()
        created_at = serializers.DateTimeField()
        updated_at = serializers.DateTimeField()

    def get(self, request: Request, portfolio_id: int) -> Response:
        try:
            portfolio = get_portfolio_by_id(portfolio_id)
            holdings = get_latest_portfolio_holdings(portfolio)
            
            paginator = self.pagination_class()
            page = paginator.paginate_queryset(holdings, request)
            serializer = self.OutputSerializer(page, many=True)
            return paginator.get_paginated_response(serializer.data)
        except Portfolio.DoesNotExist:
            return Response(
                {"error": "Portfolio not found"}, 
                status=status.HTTP_404_NOT_FOUND
            )


class PortfolioWeightsApi(APIView):
    pagination_class = StandardResultsSetPagination

    class OutputSerializer(serializers.Serializer):
        id = serializers.IntegerField()
        portfolio_id = serializers.IntegerField()
        asset_id = serializers.IntegerField()
        weight = serializers.DecimalField(max_digits=5, decimal_places=2)
        date = serializers.DateField()
        created_at = serializers.DateTimeField()
        updated_at = serializers.DateTimeField()

    def get(self, request: Request, portfolio_id: int) -> Response:
        try:
            portfolio = get_portfolio_by_id(portfolio_id)
            weights = get_latest_portfolio_weights(portfolio)
            
            paginator = self.pagination_class()
            page = paginator.paginate_queryset(weights, request)
            serializer = self.OutputSerializer(page, many=True)
            return paginator.get_paginated_response(serializer.data)
        except Portfolio.DoesNotExist:
            return Response(
                {"error": "Portfolio not found"}, 
                status=status.HTTP_404_NOT_FOUND
            )


class TransactionSerializer(serializers.Serializer):
    message = serializers.CharField()
    portfolio_id = serializers.IntegerField()
    asset_id = serializers.IntegerField()
    quantity = serializers.DecimalField(max_digits=20, decimal_places=4)
    price = serializers.DecimalField(max_digits=20, decimal_places=2)
    total = serializers.DecimalField(max_digits=20, decimal_places=2)

class MetricsSerializer(serializers.Serializer):
    date = serializers.DateField()
    total_value = serializers.DecimalField(max_digits=20, decimal_places=2)
    weights = serializers.DictField(child=serializers.DecimalField(max_digits=5, decimal_places=2))

class RebalancePortfolioApi(APIView):
    class InputSerializer(serializers.Serializer):
        start_date = serializers.DateField(required=True)
        end_date = serializers.DateField(required=True)
        sell_amount = serializers.DecimalField(max_digits=20, decimal_places=2)
        buy_amount = serializers.DecimalField(max_digits=20, decimal_places=2)
        sell_asset_id = serializers.IntegerField()
        buy_asset_id = serializers.IntegerField()

    class OutputSerializer(serializers.Serializer):
        sell_transaction = TransactionSerializer()
        buy_transaction = TransactionSerializer()
        metrics = MetricsSerializer(many=True)
    
    def post(self, request: Request, portfolio_id: int) -> Response:
        input_serializer = self.InputSerializer(data=request.data)
        input_serializer.is_valid(raise_exception=True)

        data = input_serializer.validated_data
        start_date = data.get('start_date', datetime.now().date())
        end_date = data.get('end_date', datetime.now().date())
        
        try:
            response_data = rebalance_portfolio(
                portfolio_id=portfolio_id,
                sell_asset_id=data['sell_asset_id'],
                buy_asset_id=data['buy_asset_id'],
                sell_amount=data['sell_amount'],
                buy_amount=data['buy_amount'],
                start_date=start_date,
                end_date=end_date
            )
            
            output_serializer = self.OutputSerializer(response_data)
            return Response(output_serializer.data)
            
        except (Portfolio.DoesNotExist, Asset.DoesNotExist) as e:
            return Response(
                {"error": str(e)}, 
                status=status.HTTP_404_NOT_FOUND
            )
        except (Price.DoesNotExist, Holding.DoesNotExist, ValueError) as e:
            return Response(
                {"error": str(e)}, 
                status=status.HTTP_400_BAD_REQUEST
            )
