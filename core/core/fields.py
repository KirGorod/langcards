from rest_framework import serializers

from django.core.files.base import ContentFile

import base64
import uuid


class Base64ImageField(serializers.ImageField):
    """
    A Django Rest Framework Field for handling
    image uploads through raw base64 encoded strings.
    """

    def to_internal_value(self, data):
        if ';base64,' in data:
            format, imgstr = data.split(';base64,')
            ext = format.split('/')[-1]
            avatar_file = ContentFile(
                base64.b64decode(imgstr),
                name=f"{uuid.uuid4()}.{ext}"
            )
            return avatar_file
        return super(Base64ImageField, self).to_internal_value(data)
