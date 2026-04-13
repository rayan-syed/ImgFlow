from events.events import make_event, validate_event


def test_make_event():
    event = make_event("test.topic", {"x": 1})

    assert "event_id" in event
    assert event["topic"] == "test.topic"
    assert validate_event(event) is True


def test_validate_event_missing_payload():
    bad_event = {
        "event_id": "evt_123",
        "topic": "test.topic",
        "timestamp": "2026-04-13T12:00:00Z",
    }

    try:
        validate_event(bad_event)
        assert False
    except ValueError as e:
        assert "payload" in str(e)


def test_validate_event_payload_dict():
    bad_event = {
        "event_id": "evt_123",
        "topic": "test.topic",
        "timestamp": "2026-04-13T12:00:00Z",
        "payload": "not_a_dict",
    }

    try:
        validate_event(bad_event)
        assert False
    except ValueError as e:
        assert "payload" in str(e)


def test_validate_event_topic_empty():
    bad_event = {
        "event_id": "evt_123",
        "topic": "",
        "timestamp": "2026-04-13T12:00:00Z",
        "payload": {},
    }

    try:
        validate_event(bad_event)
        assert False
    except ValueError as e:
        assert "topic" in str(e)
