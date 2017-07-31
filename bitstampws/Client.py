import json
import logging
import tornado.gen
import tornado.websocket
from datetime import datetime
from dppy.behavioral import pubsub
from time import time

from .models import Stream


logger = logging.getLogger('bitstampws')


class _Client:

    def __init__(self, publisher):
        self.publisher = publisher
        self._conn = None
        self._url = 'wss://ws.pusherapp.com/app/de504dc5763aeef9ff52?protocol=7'

    @tornado.gen.coroutine
    def connect(self):
        try:
            websocket_connect = tornado.websocket.websocket_connect
            self._conn = yield websocket_connect(self._url)
        except:
            logger.exception("failed to connect")
        else:
            logger.info("connected")
            self.listen()

    def subscribe(self, channel, book=None):
        o = (channel, book or 'btcusd')
        logger.info("subscribing(channel=%s, book=%s)" % o)
        self._conn.write_message(json.dumps({
            'event': 'pusher:subscribe',
            'data': {
                'channel': "%s_%s" % o if book else "%s" % channel
            }
        }))

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
                    payload = json.loads(msg)
                    if 'channel' in payload:
                        timestamp = time()
                        params = {
                            'timestamp': timestamp,
                            'datetime': datetime.fromtimestamp(timestamp),
                            'payload': payload
                        }
                        self.publisher.notify(Stream(**params))
                    else:
                        logger.info(payload)
            except:
                logger.exception("failed on listen")
                raise


class Client(pubsub.AbsPublisher):

    def __init__(self):
        self._client = None

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

    @tornado.gen.coroutine
    def connect(self):
        self._client = _Client(self)
        yield self._client.connect()
        for channel in self.channels:
            self._client.subscribe(channel)
            for book in self.books:
                self._client.subscribe(channel, book)
