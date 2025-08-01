
from rest_framework import serializers
from .models import Portfolio, Transaction, Holding
from nepse_data.serializers import StockSerializer

class MemberSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=100)

class PortfolioSerializer(serializers.ModelSerializer):
    members = MemberSerializer(many=True, required=False)
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = Portfolio
        fields = ['id', 'user', 'name', 'type', 'members', 'realized_gain_loss']

    def create(self, validated_data):
        members_data = validated_data.pop('members', [])
        validated_data['members'] = [member['name'] for member in members_data]
        portfolio = Portfolio.objects.create(**validated_data)
        return portfolio

    def update(self, instance, validated_data):
        members_data = validated_data.pop('members', [])
        instance.members = [member['name'] for member in members_data]
        return super().update(instance, validated_data)

from nepse_data.models import Stock # Import Stock model

class TransactionSerializer(serializers.ModelSerializer):
    stock_details = StockSerializer(source='stock', read_only=True)
    stock_symbol = serializers.CharField(write_only=True, required=True) # New field

    class Meta:
        model = Transaction
        fields = ['id', 'portfolio', 'stock_symbol', 'stock_details', 'transaction_type', 'quantity', 'price', 'transaction_date', 'total_cost']
        read_only_fields = ['total_cost', 'stock'] # Make stock read-only as it will be set internally

    def create(self, validated_data):
        stock_symbol = validated_data.pop('stock_symbol')
        try:
            stock = Stock.objects.get(symbol=stock_symbol)
        except Stock.DoesNotExist:
            raise serializers.ValidationError({"stock_symbol": "Stock with this symbol does not exist."})
        validated_data['stock'] = stock
        return super().create(validated_data)

    def update(self, instance, validated_data):
        stock_symbol = validated_data.pop('stock_symbol', None)
        if stock_symbol:
            try:
                stock = Stock.objects.get(symbol=stock_symbol)
            except Stock.DoesNotExist:
                raise serializers.ValidationError({"stock_symbol": "Stock with this symbol does not exist."})
            validated_data['stock'] = stock
        return super().update(instance, validated_data)

class HoldingSerializer(serializers.ModelSerializer):
    stock = StockSerializer()
    current_value = serializers.SerializerMethodField()
    unrealized_gain_loss = serializers.SerializerMethodField()
    unrealized_gain_loss_percent = serializers.SerializerMethodField()
    total_cost = serializers.SerializerMethodField() # Add this line

    class Meta:
        model = Holding
        fields = ['id', 'stock', 'quantity', 'average_buy_price', 'current_value', 'unrealized_gain_loss', 'unrealized_gain_loss_percent', 'total_cost'] # Add total_cost here

    def get_current_value(self, obj):
        return obj.quantity * obj.stock.last_price

    def get_unrealized_gain_loss(self, obj):
        gain_loss = self.get_current_value(obj) - (obj.quantity * obj.average_buy_price)
        return max(0, gain_loss)

    def get_unrealized_gain_loss_percent(self, obj):
        total_cost = obj.quantity * obj.average_buy_price
        if total_cost == 0:
            return 0
        return (self.get_unrealized_gain_loss(obj) / total_cost) * 100

    def get_total_cost(self, obj):
        return obj.quantity * obj.average_buy_price

class PortfolioDetailSerializer(PortfolioSerializer):
    holdings = HoldingSerializer(many=True, read_only=True)
    transactions = TransactionSerializer(many=True, read_only=True)
    total_value = serializers.SerializerMethodField()
    total_investment = serializers.SerializerMethodField()
    total_unrealized_gain_loss = serializers.SerializerMethodField()

    class Meta(PortfolioSerializer.Meta):
        fields = PortfolioSerializer.Meta.fields + ['holdings', 'transactions', 'total_value', 'total_investment', 'total_unrealized_gain_loss']

    def get_total_investment(self, obj):
        return sum(h.quantity * h.average_buy_price for h in obj.holdings.all())

    def get_total_value(self, obj):
        return sum(self.get_current_value(h) for h in obj.holdings.all())

    def get_total_unrealized_gain_loss(self, obj):
        return self.get_total_value(obj) - self.get_total_investment(obj)

    def get_current_value(self, holding):
        return holding.quantity * holding.stock.last_price
