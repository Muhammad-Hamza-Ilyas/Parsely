from src.schema import Invoice

inv = Invoice(vendor="Al-Fatah", date="2025-03-14", total=500,
              line_items=[{"description": "Milk", "amount": 380}])
print(inv)
print(inv.model_dump())