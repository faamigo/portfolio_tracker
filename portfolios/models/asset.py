from django.db import models
from django.core.exceptions import ValidationError
from django.utils import timezone
from core.models import BaseModel


class Asset(BaseModel):
    name = models.CharField(max_length=100, unique=True)

    def clean(self):
        if not self.name.strip():
            raise ValidationError("Asset name cannot be empty")
        if len(self.name) < 2:
            raise ValidationError("Asset name must be at least 2 characters long")

    def __str__(self):
        return self.name
