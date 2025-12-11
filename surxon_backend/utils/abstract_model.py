import uuid
from django.db import models


class AbstractBaseModel(models.Model):
    """
    Abstract base model with UUID primary key and timestamp fields.
    """
    id = models.UUIDField(
        primary_key=True, 
        default=uuid.uuid4,  # Using UUID4 for compatibility
        editable=False
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        abstract = True
        ordering = ["-created_at"]