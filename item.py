from dataclasses import dataclass


@dataclass
class Item:
    """A purchase tracked by the budget app."""

    name: str
    category: str
    store: str
    quantity: int
    price: float
    date: str

    def to_dict(self):
        """Convert an Item object into a JSON-friendly dictionary."""
        return {
            "name": self.name,
            "category": self.category,
            "store": self.store,
            "quantity": self.quantity,
            "price": self.price,
            "date": self.date,
        }

    @classmethod
    def from_dict(cls, data):
        """Create an Item object from a dictionary loaded from JSON."""
        return cls(
            name=str(data["name"]),
            category=str(data["category"]),
            store=str(data["store"]),
            quantity=int(data["quantity"]),
            price=float(data["price"]),
            date=str(data["date"]),
        )

    def display(self):
        """Return a readable multi-line version of this item."""
        return (
            f"{self.name}\n"
            f"Category: {self.category}\n"
            f"Store: {self.store}\n"
            f"Quantity: {self.quantity}\n"
            f"Price: ${self.price:.2f}\n"
            f"Date: {self.date}"
        )
