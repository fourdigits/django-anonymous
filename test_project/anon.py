from django_anonymous import Anonymizer, Faker, register

from .models import Item, Order


@register(Order)
class OrderAnonymizer(Anonymizer):
    UPDATE_BATCH_SIZE = 2

    first_name = Faker("first_name", unique=True)
    last_name = "Anon"


@register(Item)
class ItemAnonymizer(Anonymizer):
    description = Faker("sentence")
    amount = 25
