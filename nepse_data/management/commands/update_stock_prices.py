import os
import django

# Set up Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'neptrend.settings')
django.setup()

from nepse_data.models import Stock

# Data from your frontend's nepse-stocks.ts
NEPSE_STOCKS = [
  { "id": 1, "symbol": "NABIL", "name": "Nabil Bank Limited" },
  { "id": 2, "symbol": "NTC", "name": "Nepal Telecom" },
  { "id": 3, "symbol": "EBL", "name": "Everest Bank Limited" },
  { "id": 4, "symbol": "HBL", "name": "Himalayan Bank Limited" },
  { "id": 5, "symbol": "SCB", "name": "Standard Chartered Bank Nepal Ltd." },
  { "id": 6, "symbol": "ADBL", "name": "Agricultural Development Bank Ltd." },
  { "id": 7, "symbol": "CHCL", "name": "Chilime Hydropower Company Limited" },
  { "id": 8, "symbol": "UPPER", "name": "Upper Tamakoshi Hydropower Ltd." },
  { "id": 9, "symbol": "API", "name": "Api Power Company Ltd." },
  { "id": 10, "symbol": "HIDCL", "name": "Hydroelectricity Investment and Development Company Ltd." },
  { "id": 11, "symbol": "NLIC", "name": "Nepal Life Insurance Co. Ltd." },
  { "id": 12, "symbol": "LICN", "name": "Life Insurance Corporation Nepal Ltd." },
  { "id": 13, "symbol": "NIFRA", "name": "Nepal Infrastructure Bank Limited" },
  { "id": 14, "symbol": "CBBL", "name": "Citizens Bank International Limited" },
  { "id": 15, "symbol": "GBBL", "name": "Global IME Bank Ltd." },
  { "id": 16, "symbol": "PRVU", "name": " Prabhu Bank Limited" },
  { "id": 17, "symbol": "SBL", "name": "Siddhartha Bank Ltd." },
  { "id": 18, "symbol": "KBL", "name": "Kumari Bank Ltd." },
  { "id": 19, "symbol": "PCBL", "name": "Prime Commercial Bank Ltd." },
  { "id": 20, "symbol": "SANIMA", "name": "Sanima Bank Limited" },
]

def populate_stocks():
    print("Populating Stock data...")
    for stock_data in NEPSE_STOCKS:
        symbol = stock_data["symbol"]
        name = stock_data["name"]
        try:
            stock, created = Stock.objects.get_or_create(
                symbol=symbol,
                defaults={'name': name}
            )
            if created:
                print(f"Created stock: {symbol} - {name}")
            else:
                print(f"Stock already exists: {symbol} - {name}")
                # Optionally update name if it changed
                if stock.name != name:
                    stock.name = name
                    stock.save()
                    print(f"Updated name for {symbol}")
        except Exception as e:
            print(f"Error processing stock {symbol}: {e}")
    print("Stock population complete.")

if __name__ == '__main__':
    populate_stocks()
