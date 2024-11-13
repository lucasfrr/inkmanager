import factory
import factory.fuzzy

from inkmanager.models import Ink, Needle, Product, User

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

ink_brands = [
    'Electric Ink',
    'Viper',
    'Dynamic',
    'The Ink',
    'Intenze',
    'Iron Works',
    'Solid Ink',
]

needle_brands = [
    'Electric Ink',
    'Dynamic',
    'Aston',
    'X-Net',
    'Mast',
    'WJX',
    'Arkham',
    'Big Wasp',
    'Quelle',
    'Skin Ink',
    'White Head',
]

needle_model = ['RL', 'RS', 'MG', 'MGR']

needle_size = [
    '0801',
    '0803',
    '0805',
    '0807',
    '0809',
    '0811',
    '0813',
    '0814',
    '0815',
    '0817',
    '0819',
    '0821',
    '0823',
    '0825',
    '0827',
    '1001',
    '1003',
    '1005',
    '1007',
    '1009',
    '1011',
    '1013',
    '1014',
    '1015',
    '1017',
    '1019',
    '1021',
    '1023',
    '1025',
    '1027',
    '1201',
    '1203',
    '1205',
    '1207',
    '1209',
    '1211',
    '1213',
    '1214',
    '1215',
    '1217',
    '1219',
    '1221',
    '1223',
    '1225',
    '1227',
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
    brand = factory.fuzzy.FuzzyChoice(choices=ink_brands)
    color = factory.fuzzy.FuzzyChoice(choices=colors)
    in_use = True
    weight = '60ml'


class NeedleFactory(factory.Factory):
    class Meta:
        model = Needle

    name = factory.Sequence(lambda n: f'Agulha {n}')
    brand = factory.fuzzy.FuzzyChoice(choices=needle_brands)
    model = factory.fuzzy.FuzzyChoice(choices=needle_model)
    size = factory.fuzzy.FuzzyChoice(choices=needle_size)
    amount = factory.fuzzy.FuzzyInteger(low=0)
