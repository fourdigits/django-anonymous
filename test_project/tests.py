from django.core.management import call_command
from django.test import TestCase
from django_anonymous.register import registered_models, load_anonymizer
from test_project.models import Order, Item


class TestAnonymizer(TestCase):

    def test_load(self):
        load_anonymizer()
        self.assertEqual(len(registered_models), 2)

    def test_anonymizer(self):
        order = Order.objects.create(first_name="Master", last_name="Chief")
        item = Item.objects.create(order=order, description="Some item", amount=12.50)
        call_command("anonymize")

        new_order = Order.objects.get(id=order.id)
        self.assertEqual(order.created_on, new_order.created_on)
        self.assertNotEqual(order.first_name, new_order.first_name)
        self.assertEqual("Anon", new_order.last_name)

        new_item = Item.objects.get(id=item.id)
        self.assertEqual(item.order_id, new_item.order_id)
        self.assertNotEqual(item.description, new_item.description)
        self.assertEqual(25, new_item.amount)

