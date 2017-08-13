from decimal import Decimal

from ._BaseModel import BaseModel


class Order(BaseModel):

    def __init__(self, timestamp, datetime, book, data):
        self._timestamp = timestamp
        self._datetime = datetime
        self.book = book

        for (param, value) in data.items():
            if param == 'id':
                setattr(self, 'id', int(str(value)))
            elif param == 'amount':
                setattr(self, 'amount', Decimal(str(value)))
            elif param == 'price':
                setattr(self, 'price', Decimal(str(value)))
            elif param == 'order_type':
                if value == 0:
                    setattr(self, 'order_type', 'buy')
                elif value == 1:
                    setattr(self, 'order_type', 'sell')
                else:
                    setattr(self, 'order_type', None)
            elif param == 'datetime':
                setattr(self, 'datetime', datetime)

    def __repr__(self):
        return "Order({Order})".format(
            Order=self._repr('book','id','amount','price','datetime')
        )

