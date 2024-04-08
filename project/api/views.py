import json
import pandas as pd

from django.shortcuts import get_object_or_404

from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.exceptions import NotFound, NotAcceptable

from .serializers import StockSerializer, TradeSerializer, StockInventorySerializer

from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView

from . models import Stock, Trade, StockInventory

class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        # Add custom claims
        token['username'] = user.username

        return token
    
class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer


class RoutesView(APIView):

    def get(self, request, format=None):
        """
        This is just to list all routes or urls used in this project
        """
        routes = [
            'api/login',
            'api/token/refresh',
            'api/stocks'
        ]
        return Response(routes)

class StocksView(APIView):

    @action(methods=['GET'], detail=True)
    def get(self, request, format=None):
        """
        This is to list stocks in the market
        """
        stocks = Stock.objects.all()
        serializer = StockSerializer(stocks, many=True)

        return Response(serializer.data)
    
class CreateStocksView(APIView):

    @action(methods=['POST'], detail=True)
    def post(self, request):
        body = json.loads(request.body.decode('utf-8'))
        
        
        Stock.objects.create(name=body['name'], price=body['price'], supply=body['supply'])
        
        return Response(body)
    
class StockDetailView(APIView):
    

    @action(methods=['GET'], detail=True)
    def get(self, request, pk):
        """
        Get details of a specific stock
        """
        stock = get_object_or_404(Stock, id=pk)
        serializer = StockSerializer(instance=stock, many=False)

        return Response(serializer.data)

class TradeView(APIView):
    permission_classes = [IsAuthenticated]

    @action(methods=['POST'], detail=True)
    def post(self, request):
        body = json.loads(request.body.decode('utf-8'))

        stock_id = body['stock_id']
        quantity = body['quantity']
        is_buy = body['is_buy']

        stock = get_object_or_404(Stock, id=stock_id)

        supply = stock.supply
        name = stock.name

        data = {
            "user": request.user.id,
            "stock": stock_id,
            "quantity": quantity,
            "is_buy": is_buy,
        }

        # To check if there are missing required fields using is_valid
        serializer = TradeSerializer(data=data, many=False)
        if serializer.is_valid():
            if quantity < 1:
                raise NotAcceptable(detail=f"Invalid quantity, please input higher than 0")
            
            inventory_check = StockInventory.objects.filter(stock=stock, user=request.user).exists()

            if is_buy:

                if supply < 1:
                    raise NotAcceptable(detail=f"Sorry, {name} is out of stock")
                elif supply < quantity:
                    raise NotAcceptable(detail=f"Sorry, {name} have only {supply} stock left for trade.")
                
                purchase_total = supply - quantity
                stock.supply = purchase_total
                stock.save()

                if inventory_check:
                    update_inventory = StockInventory.objects.get(user=request.user, stock=stock)
                    update_inventory.total += quantity
                    update_inventory.save()

                    serializer_update_inventory = StockInventorySerializer(update_inventory, many=False)
                    return Response(serializer_update_inventory.data)
                
                StockInventory.objects.create(user=request.user, stock=stock, total=quantity)

                trade = Trade.objects.create(user=request.user, stock=stock, quantity=quantity, is_buy=is_buy)
                trade_serializer = TradeSerializer(trade, many=False)
                return Response(trade_serializer.data)
            
            stock_inventory = get_object_or_404(StockInventory, user=request.user, stock=stock)

            if stock_inventory.total < quantity:
                raise NotAcceptable(detail=f"Sorry, you don't have enough stock to trade {name}.")

            stock.supply += quantity
            stock.save()

            stock_inventory.total -= quantity
            stock_inventory.save()
            
            trade = Trade.objects.create(user=request.user, stock=stock, quantity=quantity, is_buy=is_buy)
            trade_serializer = TradeSerializer(trade, many=False)
            return Response(trade_serializer.data)
        
        return Response(serializer.errors)

class TradeViewCSV(APIView):
    
    @action(methods=['POST'], detail=True)
    def post(self, request):
        # Read CSV file into a DataFrame
        csv_file_path = 'api/csv/trade.csv'
        df = pd.read_csv(csv_file_path)

        # Iterate through the DataFrame
        for index, row in df.iterrows():
            stock_id = row['stock_id']
            quantity = row['quantity']
            is_buy = row['is_buy']
            

            stock = get_object_or_404(Stock, id=stock_id)

            supply = stock.supply
            name = stock.name

            data = {
                "user": request.user.id,
                "stock": stock_id,
                "quantity": quantity,
                "is_buy": is_buy,
            }

            # To check if there are missing required fields using is_valid
            serializer = TradeSerializer(data=data, many=False)
            if serializer.is_valid():
                if quantity < 1:
                    raise NotAcceptable(detail=f"Invalid quantity, please input higher than 0")
                
                inventory_check = StockInventory.objects.filter(stock=stock, user=request.user).exists()

                if is_buy:

                    if supply < 1:
                        raise NotAcceptable(detail=f"Sorry, {name} is out of stock")
                    elif supply < quantity:
                        raise NotAcceptable(detail=f"Sorry, {name} have only {supply} stock left for trade.")
                    
                    purchase_total = supply - quantity
                    stock.supply = purchase_total
                    stock.save()

                    if inventory_check:
                        update_inventory = StockInventory.objects.get(user=request.user, stock=stock)
                        update_inventory.total += quantity
                        update_inventory.save()

                        serializer_update_inventory = StockInventorySerializer(update_inventory, many=False)
                        return Response(serializer_update_inventory.data)
                    
                    StockInventory.objects.create(user=request.user, stock=stock, total=quantity)

                    trade = Trade.objects.create(user=request.user, stock=stock, quantity=quantity, is_buy=is_buy)
                    trade_serializer = TradeSerializer(trade, many=False)
                    return Response(trade_serializer.data)
                
                stock_inventory = get_object_or_404(StockInventory, user=request.user, stock=stock)

                if stock_inventory.total < quantity:
                    raise NotAcceptable(detail=f"Sorry, you don't have enough stock to trade {name}.")

                stock.supply += quantity
                stock.save()

                stock_inventory.total -= quantity
                stock_inventory.save()
                
                trade = Trade.objects.create(user=request.user, stock=stock, quantity=quantity, is_buy=is_buy)
                trade_serializer = TradeSerializer(trade, many=False)
                return Response(trade_serializer.data)
            
            return Response(serializer.errors)
    
class StockInventoryView(APIView):

    permission_classes = [IsAuthenticated]

    @action(methods=['GET'], detail=True)
    def get(self, request, format=None):
        """
        Retrieve the total value invested per stock
        """
        stocks = StockInventory.objects.filter(user=request.user.id)
        serializer = StockInventorySerializer(stocks, many=True)
        return Response(serializer.data)
        