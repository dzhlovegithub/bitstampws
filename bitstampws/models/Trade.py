from decimal import Decimal

from ._BaseModel import BaseModel


class Trade(BaseModel):

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
            elif param == 'type':
                if value == 0:
                    setattr(self, 'type', 'buy')
                elif value == 1:
                    setattr(self, 'type', 'sell')
                else:
                    setattr(self, 'type', None)
            elif param == 'timestamp':
                setattr(self, 'timestamp', int(str(value)))
            elif param == 'buy_order_id':
                setattr(self, 'buy_order_id', int(str(value)))
            elif param == 'sell_order_id':
                setattr(self, 'sell_order_id', int(str(value)))

    def __repr__(self):
        return "Trade({Trade})".format(
            Trade=self._repr('book','id','amount','price')
        )

