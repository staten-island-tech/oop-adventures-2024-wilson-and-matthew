class shopdude:
    def __init__(self, name, stock, items):
        self.name = name
        self.stock = stock
        self.items = items
    def sell(self, item):
        self.stock.append(item)
        print(self.inventory)
