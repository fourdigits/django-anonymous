import faker
from django.utils.translation import get_language


class Faker:
    """Simple wrapper for 'faker' values"""

    _FAKER_REGISTRY = {}
    """Register faker per locale"""

    def __init__(self, provider, **kwargs):
        self.provider = provider
        self.locale = kwargs.pop("locale", get_language())
        self.unique = kwargs.pop("unique", False)
        self.kwargs = kwargs

    def __call__(self):
        local_faker = self._get_faker()
        if self.unique:
            local_faker = local_faker.unique
        return local_faker.format(self.provider, **self.kwargs)

    def _get_faker(self):
        if self.locale not in self._FAKER_REGISTRY:
            self._FAKER_REGISTRY[self.locale] = faker.Faker(locale=self.locale)
        return self._FAKER_REGISTRY[self.locale]
