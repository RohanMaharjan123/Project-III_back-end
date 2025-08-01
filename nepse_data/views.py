from rest_framework import viewsets
from .models import Stock
from .serializers import StockSerializer
from rest_framework.filters import SearchFilter

class StockViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Stock.objects.all()
    serializer_class = StockSerializer
    filter_backends = [SearchFilter]
    search_fields = ['symbol', 'name']