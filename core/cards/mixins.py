class HashedImageMixin:
    @property
    def image_hash(self):
        if self.hashed_image:
            return self.hashed_image.hash
        return None
