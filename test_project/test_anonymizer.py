import pytest
from django.core.management import call_command

from django_anonymous.register import load_anonymizer, register, registered_models
from test_project.anon import ItemAnonymizer
from test_project.models import Item, Order


def test_load_anonymizer():
    load_anonymizer()
    assert len(registered_models) == 2


def test_load_anonymizer_no_models():
    with pytest.raises(ValueError) as excinfo:

        @register()
        class Test:
            pass

    assert "At least one model must be passed to register" in str(excinfo)


def test_load_anonymizer_not_subclass():
    with pytest.raises(ValueError) as excinfo:

        @register(Order)
        class Test:
            pass

    assert "Wrapped class must subclass Anonymizer" in str(excinfo)


@pytest.mark.django_db
def test_anonymizer():
    order1 = Order.objects.create(first_name="Master", last_name="Chief")
    order2 = Order.objects.create(first_name="Master2", last_name="Chief2")
    order3 = Order.objects.create(first_name="Master3", last_name="Chief3")
    item = Item.objects.create(order=order1, description="Some item", amount=12.50)
    call_command("anonymize")

    for order in [order1, order2, order3]:
        new_order = Order.objects.get(id=order.id)
        assert order.created_on == new_order.created_on
        assert order.first_name != new_order.first_name
        assert new_order.last_name == f"Anon{new_order.id}"

    new_item = Item.objects.get(id=item.id)
    assert item.order_id == new_item.order_id
    assert item.description != new_item.description
    assert 25 == new_item.amount


@pytest.mark.django_db
def test_anonymizer_seed():
    item = Item.objects.create(
        order=Order.objects.create(first_name="Master", last_name="Chief"),
        description="test",
        amount=12.50,
    )
    anon = ItemAnonymizer(Item)

    anon.anonymize_object(item)
    assert item.description != "test"

    # Should generate same description
    seed_description = item.description
    item.description = "test"
    anon.anonymize_object(item)
    assert item.description == seed_description

    # Should generate different description
    item.id = item.id + 1
    anon.anonymize_object(item)
    assert item.description != seed_description
