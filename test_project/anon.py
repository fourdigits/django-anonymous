from django_anonymous import Anonymizer, Faker, register
from .models import Order, Item


@register(Order)
class OrderAnonymizer(Anonymizer):
    first_name = Faker("first_name", unique=True)
    last_name = "Anon"


@register(Item)
class ItemAnonymizer(Anonymizer):
    description = Faker("sentence")
    amount = 25
