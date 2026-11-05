from pydantic import BaseModel

class LineItem(BaseModel):
    description: str
    quantity: float | None = None
    unit_price: float | None = None
    amount: float | None = None

class Invoice(BaseModel):
    vendor: str | None = None
    date: str | None = None          # always written YYYY-MM-DD
    total: float | None = None
    line_items: list[LineItem] = []
    currency: str | None = None 