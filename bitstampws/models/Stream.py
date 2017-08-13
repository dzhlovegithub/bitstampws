import json

from ._BaseModel import BaseModel
from .DiffOrderBook import DiffOrderBook
from .Order import Order
from .OrderBook import OrderBook
from .Trade import Trade


class Stream(BaseModel):

    def __init__(self, timestamp, datetime, payload):
        self._timestamp = timestamp
        self._datetime = datetime
        self.event = payload['event']
        self.channel = payload['channel']

        data = json.loads(payload['data'])
        if self.channel.startswith('live_trades'):
            self.book = self._get_book(2)
            self.data = self._build_data_object(data, Trade)
        elif self.channel.startswith('order_book'):
            self.book = self._get_book(2)
            self.data = self._build_data_object(data, OrderBook)
        elif self.channel.startswith('diff_order_book'):
            self.book = self._get_book(3)
            self.data = self._build_data_object(data, DiffOrder)
        elif self.channel.startswith('live_orders'):
            self.book = self._get_book(2)
            self.data = self._build_data_object(data, Order)

    def _get_book(self, length):
        if len(self.channel.split('_')) == (length + 1):
            return self.channel.split('_')[-1]
        elif len(self.channel.split('_')) == length:
            return 'btcusd'

    def _build_data_object(self, data, type):
        return type(self._timestamp, self._datetime, self.book, data)

    def __repr__(self):
        return "Stream({Stream})".format(
            Stream=self._repr('event', 'channel', 'book')
        )

