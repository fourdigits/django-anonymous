from django.core.management.base import BaseCommand

from django_anonymous.register import load_anonymizer, registered_models


class Command(BaseCommand):
    """
    Anonymize the database
    """

    help = __doc__

    def handle(self, *args, **options):
        load_anonymizer()
        for model_anonymizer in registered_models.values():
            total = model_anonymizer.run_anonymizer()
            if total == 1:
                model_name = model_anonymizer._model._meta.verbose_name.title()
            else:
                model_name = model_anonymizer._model._meta.verbose_name_plural.title()
            self.stdout.write(
                self.style.SUCCESS(f"{total} {model_name} are anonymized")
            )
