import json
import logging
import tornado.gen
import tornado.websocket
from dppy.behavioral import pubsub
from time import time

from .models import (
    DiffOrderBook, Order, OrderBook, Trade
)


logger = logging.getLogger('bitstampws')


class _Client:

    def __init__(self, publisher, channel, book=None):
        self.publisher = publisher
        self.channel = channel
        self.book = book
        self._conn = None
        self._url = 'wss://ws.pusherapp.com/app/de504dc5763aeef9ff52?protocol=7'

    @property
    def type(self):
        if self.channel.startswith('live_trades'):
            return Trade
        elif self.channel.startswith('order_book'):
            return OrderBook
        elif self.channel.startswith('diff_order_book'):
            return DiffOrderBook
        elif self.channel.startswith('live_orders'):
            return Order
        else:
            raise NotImplementedError('unknown channel')

    @tornado.gen.coroutine
    def connect(self):
        try:
            o = (self.channel, self.book or 'btcusd')
            logger.info("subscribing(channel=%s, book=%s)" % o)
            websocket_connect = tornado.websocket.websocket_connect
            self._conn = yield websocket_connect(self._url)
            self._conn.write_message(json.dumps({
                'event': 'pusher:subscribe',
                'data': {
                    'channel': "%s_%s" % o if self.book else "%s" % self.channel
                }
            }))
        except:
            logger.exception("failed to connect (%s,%s)" % (self.book, self.channel))
        else:
            logger.info("connected")
            self.listen()

    @tornado.gen.coroutine
    def listen(self):
        while True:
            try:
                msg = yield self._conn.read_message()
                if msg is None:
                    logger.info("connection closed")
                    self._conn = None
                    break
                else:
                    if self.channel.startswith('live_trades'):
                        o = self.type(time(), self.book, **json.loads(msg))
                        logger.info(o)
                        self.publisher.notify(o)
            except:
                logger.exception("failed on listen")
                raise


class Client(pubsub.AbsPublisher):

    def __init__(self):
        self._clients = {}

    @property
    def channels(self):
        return [
            'live_trades', 'order_book', 'diff_order_book', 'live_orders'
        ]

    @property
    def books(self):
        return [
            'btceur', 'eurusd', 'xrpusd', 'xrpeur', 'xrpbtc', 'ltcusd', 'ltceur', 'ltcbtc'
        ]

    def connect(self):
        for channel in self.channels:
            self._clients[(channel,)] = _Client(self, channel)
            self._clients[(channel,)].connect()
            for book in self.books:
                self._clients[(channel, book)] = _Client(self, channel, book)
                self._clients[(channel, book)].connect()

