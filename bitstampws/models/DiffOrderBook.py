from decimal import Decimal

from ._BaseModel import BaseModel


class _DiffOrder:

    def __init__(self, amount, price):
        self.amount = Decimal(str(amount))
        self.price = Decimal(str(price))


class DiffOrderBook(BaseModel):

    def __init__(self, timestamp, datetime, book, data):
        self._timestamp = timestamp
        self._datetime = datetime
        self.book = book

        for (param, value) in data.items():
            if param == 'timestamp':
                self.timestamp = Decimal(str(timestamp))
            elif param == 'bids':
                self.bids = self._build_difforders_list(value)
            elif param == 'asks':
                self.asks = self._build_difforders_list(value)

    def _build_difforders_list(self, data):
        _orders = []
        for order in data:
            _orders.append(_DiffOrder(order[1], order[0]))
        return _orders

    def __repr__(self):
        return "DiffOrderBook(book={book}, {num_bids} bids, {num_asks} asks)".format(
            book = self.book,
            num_bids = len(self.bids),
            num_asks = len(self.asks)
        )

