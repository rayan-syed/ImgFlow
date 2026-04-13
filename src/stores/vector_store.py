class VectorStore:
    def __init__(self):
        self.vectors = {}

    def save_embedding(self, image_id, embedding):
        self.vectors[image_id] = embedding

    def get_embedding(self, image_id):
        return self.vectors.get(image_id)

    def has_image(self, image_id):
        return image_id in self.vectors
