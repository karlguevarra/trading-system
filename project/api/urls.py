from django.urls import path
from . views import RoutesView, StocksView, StockDetailView, TradeView, StockInventoryView, TradeViewCSV, CreateStocksView
from . views import MyTokenObtainPairView
from rest_framework_simplejwt.views import (
    TokenRefreshView,
)

urlpatterns = [
    path('', RoutesView.as_view()),
    path('stocks/', StocksView.as_view()),
    path('stocks/create/', CreateStocksView.as_view()),
    path('stocks/<int:pk>/', StockDetailView.as_view()),
    path('stocks/trade/', TradeView.as_view()),
    path('stocks/trade/csv/', TradeViewCSV.as_view()),

    path('stocks/inventory/', StockInventoryView.as_view()),

    path('login/', MyTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]
