from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.request import Request
from datetime import datetime
from ..services.portfolio_service import (
    execute_buy_transaction,
    execute_sell_transaction
)
from portfolios.models import Portfolio, Asset, Price, Holding
from rest_framework import serializers, status
from portfolios.selectors.portfolio_selector import get_portfolio_assets
from .pagination import StandardResultsSetPagination


class PortfolioAssetsApi(APIView):
    pagination_class = StandardResultsSetPagination

    class OutputSerializer(serializers.Serializer):
        portfolio_id = serializers.IntegerField()
        date = serializers.DateField()
        assets = serializers.ListField(
            child=serializers.DictField(
                child=serializers.CharField()
            )
        )
    
    def get(self, request: Request, portfolio_id: int) -> Response:
        try:
            assets_data, latest_date = get_portfolio_assets(portfolio_id)
            if latest_date is None:
                return Response({"assets": []})
            
            response_data = {
                "portfolio_id": portfolio_id,
                "date": latest_date.strftime("%Y-%m-%d"),
                "assets": assets_data
            }
            
            paginator = self.pagination_class()
            paginated_data = paginator.paginate_queryset(response_data["assets"], request)
            response_data["assets"] = paginated_data
            
            serializer = self.OutputSerializer(response_data)
            return paginator.get_paginated_response(serializer.data)
        except Portfolio.DoesNotExist:
            return Response({"error": "Portfolio not found"}, status=status.HTTP_404_NOT_FOUND)


class BuyAssetApi(APIView):
    class InputSerializer(serializers.Serializer):
        amount = serializers.DecimalField(max_digits=20, decimal_places=2)
        date = serializers.DateField(required=False)

    class OutputSerializer(serializers.Serializer):
        message = serializers.CharField()
        portfolio_id = serializers.IntegerField()
        asset_id = serializers.IntegerField()
        quantity = serializers.DecimalField(max_digits=20, decimal_places=4)
        price = serializers.DecimalField(max_digits=20, decimal_places=2)
        total = serializers.DecimalField(max_digits=20, decimal_places=2)
    
    def post(self, request: Request, portfolio_id: int, asset_id: int) -> Response:
        input_serializer = self.InputSerializer(data=request.data)
        input_serializer.is_valid(raise_exception=True)

        amount = input_serializer.validated_data['amount']
        date = input_serializer.validated_data.get('date', datetime.now().date())

        try:
            response = execute_buy_transaction(portfolio_id, asset_id, amount, date)
            output_serializer = self.OutputSerializer(response)
            return Response(output_serializer.data)
        except (Portfolio.DoesNotExist, Asset.DoesNotExist):
            return Response(
                {"error": "Portfolio or Asset not found"}, 
                status=status.HTTP_404_NOT_FOUND
            )
        except Price.DoesNotExist:
            return Response(
                {"error": f"No price found for asset on {date}"}, 
                status=status.HTTP_404_NOT_FOUND
            )


class SellAssetApi(APIView):
    class InputSerializer(serializers.Serializer):
        amount = serializers.DecimalField(max_digits=20, decimal_places=2)
        date = serializers.DateField(required=False)

    class OutputSerializer(serializers.Serializer):
        message = serializers.CharField()
        portfolio_id = serializers.IntegerField()
        asset_id = serializers.IntegerField()
        quantity = serializers.DecimalField(max_digits=20, decimal_places=4)
        price = serializers.DecimalField(max_digits=20, decimal_places=2)
        total = serializers.DecimalField(max_digits=20, decimal_places=2)
    
    def post(self, request: Request, portfolio_id: int, asset_id: int) -> Response:
        input_serializer = self.InputSerializer(data=request.data)
        input_serializer.is_valid(raise_exception=True)

        amount = input_serializer.validated_data['amount']
        date = input_serializer.validated_data.get('date', datetime.now().date())

        try:
            response = execute_sell_transaction(portfolio_id, asset_id, amount, date)
            output_serializer = self.OutputSerializer(response)
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
