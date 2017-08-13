from decimal import Decimal

from ._BaseModel import BaseModel


class Trade(BaseModel):

    def __init__(self, timestamp, datetime, book, data):
        self._timestamp = timestamp
        self._datetime = datetime
        self.book = book
        for (param, value) in data.items():
            if param == 'id':
                setattr(self, 'id', value)
            elif param == 'amount':
                setattr(self, 'amount', value)
            elif param == 'price':
                setattr(self, 'price', value)
            elif param == 'type':
                setattr(self, 'type', value)
            elif param == 'timestamp':
                setattr(self, 'timestamp', value)
            elif param == 'buy_order_id':
                setattr(self, 'buy_order_id', value)
            elif param == 'sell_order_id':
                setattr(self, 'sell_order_id', value)

    def __repr__(self):
        return "Trade({Trade})".format(
            Trade=self._repr('book','id','amount','price')
        )

