from django.core.management.base import BaseCommand

from django_anonymous.register import load_anonymizer, registered_models


class Command(BaseCommand):
    """
    Anonymize the database
    """

    help = __doc__
    confirmation_text = "Are you sure you want to anonymize all data? [Y/n]: "

    def add_arguments(self, parser):
        parser.add_argument("--yes", action="store_true")

    def handle(self, *args, **options):
        if not options.get("yes") and input(self.confirmation_text).lower() == "n":
            exit(0)

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
