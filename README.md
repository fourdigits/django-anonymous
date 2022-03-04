# django-anonymous

Simple Djanngo module to anonymize production data for safe usage on none production environments.

## Installation

    pip install django-anonymous

## Usage

In your app create a file `anon.py`:

```python
from django_anonymous import Anonymizer, Faker, register
from .model import YourModel


@register(YourModel)
class YourModelAnonymizer(Anonymizer):
    
    # You can give any callable, Faker is a small wrapper around the `faker` library. 
    email = Faker("email", unique=True)
    
    # You can also use any static value
    first_name = "Anon"
```

Run the anonymizer

    python manage.py anonymize

## Custom QuerySet

You can set a custom QuerySet to filter out some objects

```python
from django_anonymous import Anonymizer, Faker, register
from .model import YourModel


@register(YourModel)
class YourModelAnonymizer(Anonymizer):
    email = Faker("email", unique=True)

    def get_queryset(self):
        return super().get_queryset().filter(is_staff=True)
```

## Settings for Anonymizer

Per Anonymizer you can set the select chunk size and update batch size.

```python
from django_anonymous import Anonymizer, Faker, register
from .model import YourModel


@register(YourModel)
class YourModelAnonymizer(Anonymizer):
    SELECT_CHUNK_SIZE = 100
    UPDATE_BATCH_SIZE = 25
    
    email = Faker("email", unique=True)
```

## Inspired by

- https://github.com/Tesorio/django-anon
- https://github.com/FactoryBoy/factory_boy