import json
import logging
import tornado.gen
import tornado.websocket
from dppy.behavioral import pubsub


class Client(pubsub.AbsPublisher):

    def __init__(self):
        self._ws_client = None
        self._ws_url = 'wss://ws.pusherapp.com/app/de504dc5763aeef9ff52?protocol=7'
        self._channels = [
            'live_trades', 'order_book', 'diff_order_book', 'live_orders'
        ]
        self._books = [
            'btceur', 'eurusd', 'xrpusd', 'xrpeur', 'xrpbtc', 'ltcusd', 'ltceur', 'ltcbtc'
        ]

    @tornado.gen.coroutine
    def connect(self):
        logger.info("connecting")
        try:
            websocket_connect = tornado.websocket.websocket_connect
            self._ws_client = yield websocket_connect(self._ws_url)
            self.subscribe()
        except:
            logger.exception("failed to connect")
        else:
            logger.info("connected")
            self.listen()

    @tornado.gen.coroutine
    def listen(self):
        while True:
            try:
                msg = yield self._ws_client.read_message()
                if msg is None:
                    logger.info("connection closed")
                    self._ws_client = None
                    break
                else:
                    _json = json.loads(msg)
                    logger.info(msg)
            except:
                logger.exception("failed on listen")
                raise

    def _subscribe(self, channel, book=None):
        o = (channel, book or 'btcusd')
        logger.info("subscribing(channel=%s, book=%s)" % o)
        self._ws_client.write_message(json.dumps({
            'event': 'pusher:subscribe',
            'data': {
                'channel': "%s_%s" % o if book else "%s" % channel
            }
        }))

    def subscribe(self):
        for channel in self._channels:
            self._subscribe(channel)
            for book in self._books:
                self._subscribe(channel, book)

