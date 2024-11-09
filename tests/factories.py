import factory
import factory.fuzzy

from inkmanager.models import Product, User


class ProductFactory(factory.Factory):
    class Meta:
        model = Product

    name = factory.Faker('text')
    amount = 3


class UserFactory(factory.Factory):
    class Meta:
        model = User

    username = factory.Sequence(lambda n: f'user{n}')
    email = factory.LazyAttribute(lambda obj: f'{obj.username}@test.com')
    password = factory.LazyAttribute(
        lambda obj: f'{obj.username.capitalize()}@01saA'
    )
    fullname = factory.LazyAttribute(
        lambda obj: f'{obj.username.capitalize()} Silva'
    )
