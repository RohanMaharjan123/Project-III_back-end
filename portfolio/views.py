from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import Portfolio, Transaction, Holding
from .serializers import PortfolioSerializer, TransactionSerializer, PortfolioDetailSerializer
from .permissions import IsOwner
from .utils import update_holdings_on_transaction

class PortfolioViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated, IsOwner]

    def get_queryset(self):
        return Portfolio.objects.filter(user=self.request.user)

    def get_serializer_class(self):
        if self.action in ['retrieve', 'list']:
            return PortfolioDetailSerializer
        return PortfolioSerializer

class TransactionViewSet(viewsets.ModelViewSet):
    serializer_class = TransactionSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Transaction.objects.filter(portfolio__user=self.request.user)

    def perform_create(self, serializer):
        transaction = serializer.save()
        update_holdings_on_transaction(transaction)

    def perform_destroy(self, instance):
        # Revert holdings before deleting the transaction
        reverted_transaction = Transaction(
            portfolio=instance.portfolio,
            stock=instance.stock,
            quantity=instance.quantity,
            price=instance.price,
            transaction_type='sell' if instance.transaction_type == 'buy' else 'buy'
        )
        update_holdings_on_transaction(reverted_transaction, is_reversal=True)
        instance.delete()