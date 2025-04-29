import factory
from django.utils import timezone
from portfolios.models import (
    Portfolio,
    Asset,
    Price,
    Weight,
    Holding
)


class PortfolioFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Portfolio

    name = factory.Sequence(lambda n: f"Test Portfolio {n}")
    initial_value = factory.Faker('pydecimal', left_digits=5, right_digits=2, positive=True)
    created_at = factory.LazyFunction(timezone.now)

class AssetFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Asset

    name = factory.Sequence(lambda n: f"Test Asset {n}")

class PriceFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Price

    asset = factory.SubFactory(AssetFactory)
    date = factory.LazyFunction(timezone.now)
    price = factory.Faker('pydecimal', left_digits=5, right_digits=2, positive=True)

class WeightFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Weight

    portfolio = factory.SubFactory(PortfolioFactory)
    asset = factory.SubFactory(AssetFactory)
    date = factory.LazyFunction(timezone.now)
    weight = factory.Faker('pydecimal', left_digits=1, right_digits=2, positive=True, max_value=1)

class HoldingFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Holding

    portfolio = factory.SubFactory(PortfolioFactory)
    asset = factory.SubFactory(AssetFactory)
    date = factory.LazyFunction(timezone.now)
    quantity = factory.Faker('pydecimal', left_digits=5, right_digits=2, positive=True)
     