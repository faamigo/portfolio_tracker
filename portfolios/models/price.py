from django.db import models
from django.core.exceptions import ValidationError
from core.models import BaseModel
from .asset import Asset
from django.utils import timezone


class Price(BaseModel):
    asset = models.ForeignKey(Asset, on_delete=models.CASCADE)
    date = models.DateField()
    price = models.DecimalField(max_digits=12, decimal_places=2)

    class Meta:
        unique_together = ('asset', 'date')
        ordering = ['date']
    
    def clean(self):
        if self.price <= 0:
            raise ValidationError("Price must be positive")
        if self.date > timezone.now().date():
            raise ValidationError("Price date cannot be in the future")
    
    def __str__(self):
        return f"{self.asset.name} - {self.date} - {self.price}"
