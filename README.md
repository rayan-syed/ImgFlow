# imgflow

Event-driven image annotation and retrieval pipeline using Redis pub-sub.

## System Architecture

### Services
- CLI Service
- Inference Service
- Storage Service
- Query Service

### Pub-Sub Topics (thorugh Redis)
- image.submitted
- inference.completed
- annotation.stored
- query.submitted
- query.completed

### Event Schema
All events follow:
```
{
    event_id,
    topic,
    timestamp,
    payload
}
```

### Diagram (text for now)
Image Upload: CLI → Redis → Inference Service → Redis → Storage

Query: CLI → Redis → Query Service → Redis → CLI