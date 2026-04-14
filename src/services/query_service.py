from src.events.events import make_event
from src.events.topics import QUERY_SUBMITTED, QUERY_COMPLETED
from src.broker.redis_broker import RedisBroker
from src.stores.document_store import DocumentStore
from src.stores.vector_store import VectorStore


class QueryService:
    def __init__(self, broker, document_store=None, vector_store=None):
        self.broker = broker
        self.document_store = document_store or DocumentStore()
        self.vector_store = vector_store or VectorStore()

    def handle_query_submitted(self, event):
        try:
            payload = event["payload"]

            required_keys = ["query_id", "embedding", "top_k"]
            for key in required_keys:
                if key not in payload:
                    raise ValueError(f"query.submitted missing payload key: {key}")

            print(f"[QueryService] Received query.submitted for {payload['query_id']}")

            matches = self.vector_store.search(
                payload["embedding"],
                payload["top_k"],
            )

            results = []

            for image_id, score in matches:
                document = self.document_store.get_annotation(image_id)

                results.append({
                    "image_id": image_id,
                    "score": score,
                    "document": document,
                })

            out_event = make_event(
                QUERY_COMPLETED,
                {
                    "query_id": payload["query_id"],
                    "results": results,
                },
            )

            self.broker.publish(QUERY_COMPLETED, out_event)

            print(f"[QueryService] Published {QUERY_COMPLETED}")

        except Exception as e:
            print(f"[QueryService] Error: {e}")

    def start(self):
        print(f"[QueryService] Listening on topic: {QUERY_SUBMITTED}")
        self.broker.subscribe(
            QUERY_SUBMITTED,
            self.handle_query_submitted,
        )


if __name__ == "__main__":
    broker = RedisBroker()
    service = QueryService(broker)
    service.start()
