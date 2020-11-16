from django.db import models
import uuid

class File(models.Model):
    file_uuid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    uploaded_at = models.DateTimeField(auto_now_add=True)
    zipname = models.CharField(max_length=100)
    user_uuid = models.UUIDField(primary_key=False, default=uuid.uuid4, editable=False)

    def __str__(self):
        return self.description
