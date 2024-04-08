from rest_framework.serializers import ModelSerializer
from . models import Stock, Trade, StockInventory

class StockSerializer(ModelSerializer):
    class Meta:
        model = Stock
        fields = '__all__'

class TradeSerializer(ModelSerializer):
    class Meta:
        model = Trade
        fields = '__all__'

        def create(self, validated_data):
            return Trade.objects.create(**validated_data)
        
class StockInventorySerializer(ModelSerializer):
    class Meta:
        model = StockInventory
        fields = '__all__'