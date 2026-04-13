import json
import redis

from src.events.events import validate_event


class RedisBroker:
    def __init__(self, url="redis://localhost:6379/0", client=None):
        self.client = client or redis.Redis.from_url(
            url, decode_responses=True)

    def publish(self, topic, event):
        validate_event(event)
        self.client.publish(topic, json.dumps(event))

    def subscribe(self, topic, handler):
        pubsub = self.client.pubsub()
        pubsub.subscribe(topic)

        for message in pubsub.listen():
            if message["type"] != "message":
                continue

            event = json.loads(message["data"])
            validate_event(event)
            handler(event)
