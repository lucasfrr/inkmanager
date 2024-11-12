import factory
import factory.fuzzy

from inkmanager.models import Ink, Product, User

colors = [
    'Red',
    'Blue',
    'Violet',
    'Black',
    'Magenta',
    'Rose',
    'Yelloy',
    'Orange',
    'Salmon',
    'White',
    'Gray',
]

brands = [
    'Electric Ink',
    'Viper',
    'Dynamic',
    'The Ink',
    'Intenze',
    'Iron Works',
    'Solid Ink',
]


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


class ProductFactory(factory.Factory):
    class Meta:
        model = Product

    name = factory.Faker('text')
    amount = 3


class InkFactory(factory.Factory):
    class Meta:
        model = Ink

    name = factory.Sequence(lambda n: f'Tinta {n}')
    brand = factory.fuzzy.FuzzyChoice(choices=brands)
    color = factory.fuzzy.FuzzyChoice(choices=colors)
    in_use = True
    weight = '60ml'
