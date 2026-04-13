import json

from src.broker.redis_broker import RedisBroker
from src.events.events import make_event
from src.events.topics import IMAGE_SUBMITTED


class FakeRedisClient:
    def __init__(self):
        self.published_messages = []

    def publish(self, topic, data):
        self.published_messages.append((topic, data))


def test_publish_sends_json_to_correct_topic():
    fake_client = FakeRedisClient()
    broker = RedisBroker(client=fake_client)

    event = make_event(
        IMAGE_SUBMITTED,
        {
            "image_id": "img_001",
            "image_path": "images/test.jpg",
            "source": "cli",
        },
    )

    broker.publish(IMAGE_SUBMITTED, event)

    assert len(fake_client.published_messages) == 1

    topic, raw_data = fake_client.published_messages[0]

    assert topic == IMAGE_SUBMITTED

    decoded = json.loads(raw_data)
    assert decoded["topic"] == IMAGE_SUBMITTED
    assert decoded["payload"]["image_id"] == "img_001"
    assert decoded["payload"]["image_path"] == "images/test.jpg"
