from django.db import models
from django.core.exceptions import ValidationError
from django.utils import timezone
from core.models import BaseModel
from .asset import Asset
from .portfolio import Portfolio


class Holding(BaseModel):
    portfolio = models.ForeignKey(Portfolio, on_delete=models.CASCADE)
    asset = models.ForeignKey(Asset, on_delete=models.CASCADE)
    date = models.DateField()
    quantity = models.DecimalField(max_digits=12, decimal_places=2)

    class Meta:
        unique_together = ('portfolio', 'asset', 'date')
        ordering = ['date']

    def clean(self):
        if self.date > timezone.now().date():
            raise ValidationError("Holding date cannot be in the future")

    def __str__(self):
        return f"{self.portfolio.name} - {self.asset.name} - {self.quantity}"
