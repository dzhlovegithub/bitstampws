import json
import logging
import tornado.gen
import tornado.websocket
from dppy.behavioral import pubsub


class _Client:

    def __init__(self, publisher, channel, book=None):
	self.publisher = publisher
	self.channel = channel
	self.book = book
	self._conn = None
	self._url = 'wss://ws.pusherapp.com/app/de504dc5763aeef9ff52?protocol=7'

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
		    'channel': "%s_%s" % o if book else "%s" % self.channel
		}
	    }))
	except:
	    logger.exception("failed to connect")
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
		    _json = json.loads(msg)
		    if self.channel.startswith('live_trades'):
			# self.publisher.notify(Trade())
			pass
		    elif self.channel.startswith('order_book'):
			# self.publisher.notify(OrderBook())
			pass
		    elif self.channel.startswith('diff_order_book'):
			# self.publisher.notify(DiffOrderBook())
			pass
		    elif self.channel.startswith('live_orders'):
			# self.publisher.notify(Order())
			pass
	    except:
		logger.exception("failed on listen")
		raise


class Client(pubsub.AbsPublisher):

    def __init__(self):
        self._channels = [
            'live_trades', 'order_book', 'diff_order_book', 'live_orders'
        ]
        self._books = [
            'btceur', 'eurusd', 'xrpusd', 'xrpeur', 'xrpbtc', 'ltcusd', 'ltceur', 'ltcbtc'
        ]

    def connect(self):
	pass

    def subscribe(self):
        for channel in self._channels:
            self._subscribe(channel)
            for book in self._books:
                self._subscribe(channel, book)

