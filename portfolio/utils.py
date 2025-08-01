
from .models import Holding, Transaction

def update_holdings_on_transaction(transaction, is_reversal=False):
    print(f"--- update_holdings_on_transaction called for transaction: {transaction.id} ---")
    print(f"Transaction details: Type={transaction.transaction_type}, Quantity={transaction.quantity}, Price={transaction.price}, Stock={transaction.stock.symbol}")

    holding, created = Holding.objects.get_or_create(
        portfolio=transaction.portfolio,
        stock=transaction.stock,
        defaults={'quantity': 0, 'average_buy_price': 0}
    )
    print(f"Holding before update: Quantity={holding.quantity}, Avg Price={holding.average_buy_price}")

    if transaction.transaction_type == 'buy':
        if is_reversal: # This is a reversal of a sell, so it's a buy back
            holding.quantity += transaction.quantity
            print(f"Buy reversal: New quantity={holding.quantity}")
        else:
            total_cost = (holding.quantity * holding.average_buy_price) + (transaction.quantity * transaction.price)
            new_quantity = holding.quantity + transaction.quantity
            
            if new_quantity > 0: # Avoid division by zero
                holding.average_buy_price = total_cost / new_quantity
            else:
                holding.average_buy_price = 0 # Should not happen for a buy
            
            holding.quantity = new_quantity
            print(f"Buy transaction: New quantity={holding.quantity}, New Avg Price={holding.average_buy_price}")

    elif transaction.transaction_type == 'sell':
        if is_reversal: # This is a reversal of a buy, so it's a sell back
            holding.quantity -= transaction.quantity
            print(f"Sell reversal: New quantity={holding.quantity}")
        else:
            # Realized gain/loss calculation
            cost_of_sold_shares = holding.average_buy_price * transaction.quantity
            proceeds_from_sale = transaction.price * transaction.quantity
            realized_gain = proceeds_from_sale - cost_of_sold_shares
            
            portfolio = transaction.portfolio
            portfolio.realized_gain_loss += realized_gain
            portfolio.save()
            print(f"Realized Gain/Loss for portfolio {portfolio.id}: {portfolio.realized_gain_loss}")

            holding.quantity -= transaction.quantity
            print(f"Sell transaction: New quantity={holding.quantity}")

    if holding.quantity > 0:
        holding.save()
        print(f"Holding saved: Quantity={holding.quantity}, Avg Price={holding.average_buy_price}")
    else:
        holding.delete()
        print("Holding deleted as quantity is 0 or less.")
    print(f"--- End of update_holdings_on_transaction ---")
