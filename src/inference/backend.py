# mock for now
class InferenceBackend:
    def run(self, image_path):
        return {
            "tags": [
                {"label": "example_tag", "score": 0.95}
            ],
            "embedding": [0.1, 0.2, 0.3],
            "model_name": "dummy-backend",
        }
