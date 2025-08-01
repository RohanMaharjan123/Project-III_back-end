from django.db import models
from django.conf import settings

class Portfolio(models.Model):
    PERSONAL = 'personal'
    FAMILY = 'family'
    JOINT = 'joint'
    PORTFOLIO_TYPE_CHOICES = [
        (PERSONAL, 'Personal'),
        (FAMILY, 'Family'),
        (JOINT, 'Joint'),
    ]

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='portfolios')
    name = models.CharField(max_length=100)
    type = models.CharField(max_length=10, choices=PORTFOLIO_TYPE_CHOICES, default=PERSONAL)
    members = models.JSONField(default=list, blank=True) 
    realized_gain_loss = models.DecimalField(max_digits=15, decimal_places=2, default=0.00)

    def __str__(self):
        return f"{self.name} ({self.get_type_display()}) - {self.user.username}"

class Transaction(models.Model):
    BUY = 'buy'
    SELL = 'sell'
    TRANSACTION_TYPE_CHOICES = [
        (BUY, 'Buy'),
        (SELL, 'Sell'),
    ]

    portfolio = models.ForeignKey(Portfolio, on_delete=models.CASCADE, related_name='transactions')
    stock = models.ForeignKey('nepse_data.Stock', on_delete=models.CASCADE, related_name='transactions')
    transaction_type = models.CharField(max_length=4, choices=TRANSACTION_TYPE_CHOICES)
    quantity = models.PositiveIntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    transaction_date = models.DateField()
    total_cost = models.DecimalField(max_digits=15, decimal_places=2, editable=False)

    def save(self, *args, **kwargs):
        self.total_cost = self.quantity * self.price
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.transaction_type.upper()} {self.quantity} of {self.stock.symbol} @ {self.price}"

class Holding(models.Model):
    portfolio = models.ForeignKey(Portfolio, on_delete=models.CASCADE, related_name='holdings')
    stock = models.ForeignKey('nepse_data.Stock', on_delete=models.CASCADE, related_name='holdings')
    quantity = models.PositiveIntegerField()
    average_buy_price = models.DecimalField(max_digits=10, decimal_places=2)

    class Meta:
        unique_together = ('portfolio', 'stock')

    def __str__(self):
        return f"{self.quantity} of {self.stock.symbol} in {self.portfolio.name}"