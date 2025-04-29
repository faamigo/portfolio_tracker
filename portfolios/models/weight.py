from django.db import models
from django.core.exceptions import ValidationError
from django.db.models import Sum
from django.utils import timezone
from core.models import BaseModel
from .asset import Asset
from .portfolio import Portfolio


class Weight(BaseModel):
    portfolio = models.ForeignKey(Portfolio, on_delete=models.CASCADE)
    asset = models.ForeignKey(Asset, on_delete=models.CASCADE)
    date = models.DateField()
    weight = models.DecimalField(max_digits=6, decimal_places=4)

    class Meta:
        unique_together = ('portfolio', 'asset', 'date')
        ordering = ['date']
    
    def clean(self):
        if self.weight <= 0 or self.weight > 1:
            raise ValidationError("Weight must be between 0 and 1")
        if self.date > timezone.now().date():
            raise ValidationError("Weight date cannot be in the future")
    
    def __str__(self):
        return f"{self.portfolio.name} - {self.asset.name} - {self.date} - {self.weight}"
