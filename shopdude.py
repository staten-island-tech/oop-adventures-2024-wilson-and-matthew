class shopdude:
    def __init__(self, name, stock, items):
        self.name = name
        self.stock = stock
        self.items = items
    def sell(self, item):
        self.stock.append(item)
        self.stock.remove(item)
        print(self.inventory)