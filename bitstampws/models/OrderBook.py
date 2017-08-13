from decimal import Decimal

from ._BaseModel import BaseModel


class _Order:

    def __init__(self, amount, price):
        self.amount = Decimal(str(amount))
        self.price = Decimal(str(amount))


class OrderBook(BaseModel):

    def __init__(self, timestamp, datetime, book, data):
        self._timestamp = timestamp
        self._datetime = datetime
        self.book = book
        
        for (param, value) in data.items():
            if param == 'bids':
                self.bids = self._build_orders_list(value)
            elif param == 'asks':
                self.asks = self._build_orders_list(value)

    def _build_orders_list(self, data):
        _orders = []
        for order in data:
            _orders.append(_Order(order[1], order[0]))
        return _orders

    def __repr__(self):
        return "OrderBook(book={book}, {num_bids} bids, {num_asks} asks)".format(
            book = self.book,
            num_bids = len(self.bids),
            num_asks = len(self.asks)
        )

