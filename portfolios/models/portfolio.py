from django.db import models
from django.core.exceptions import ValidationError
from core.models import BaseModel


class Portfolio(BaseModel):
    name = models.CharField(max_length=100, unique=True)
    initial_value = models.DecimalField(max_digits=20, decimal_places=2, null=True, blank=True)

    def clean(self):
        if not self.name.strip():
            raise ValidationError("Portfolio name cannot be empty")
        if len(self.name) < 2:
            raise ValidationError("Portfolio name must be at least 2 characters long")
        if self.initial_value is not None and self.initial_value <= 0:
            raise ValidationError("Initial value must be positive")

    def __str__(self):
        return self.name
