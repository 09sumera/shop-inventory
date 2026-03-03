class Product:
    def __init__(self, data):
        self.id = int(data.get("id"))
        self.name = data.get("name")
        self.price = float(data.get("price"))
        self.qty = int(data.get("qty"))

    def is_valid(self):
        if not self.name:
            return False, "Product name is required"
        if self.price < 0:
            return False, "Price cannot be negative"
        if self.qty < 0:
            return False, "Quantity cannot be negative"
        return True, None

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "price": self.price,
            "qty": self.qty
        }
