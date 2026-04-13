class DocumentStore:
    def __init__(self):
        self.documents = {}

    def save_annotation(self, image_id, document):
        self.documents[image_id] = document

    def get_annotation(self, image_id):
        return self.documents.get(image_id)

    def has_image(self, image_id):
        return image_id in self.documents
