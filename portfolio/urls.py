
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import PortfolioViewSet, TransactionViewSet

router = DefaultRouter()
router.register(r'portfolios', PortfolioViewSet, basename='portfolio')
router.register(r'transactions', TransactionViewSet, basename='transaction')

urlpatterns = [
    path('', include(router.urls)),
]
