import json

from ._BaseModel import BaseModel


class Stream(BaseModel):

    def __init__(self, timestamp, datetime, payload):
        self.event = payload['event']
        self.channel = payload['channel']
        if 'data' in payload:
            book = self.channel.split('_')[-1]
            data = json.loads(payload['data'])
            if self.event.startswith('live_trades'):
                logger.info(data)
            elif self.event.startswith('order_book'):
                pass
            elif self.event.startswith('diff_order_book'):
                pass
            elif self.event.startswith('live_orders'):
                pass

