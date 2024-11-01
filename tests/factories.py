import factory
import factory.fuzzy

from inkmanager.models import Product


class ProductFactory(factory.Factory):
    class Meta:
        model = Product

    name = factory.Faker('text')
    amount = 3
