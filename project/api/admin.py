from django.contrib import admin
from . models import Stock, Trade, StockInventory

# Register your models here.
admin.site.register(Stock)
admin.site.register(Trade)
admin.site.register(StockInventory)