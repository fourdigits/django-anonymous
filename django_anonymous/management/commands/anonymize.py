from django.core.management.base import BaseCommand
from tqdm import tqdm

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
            model_name = model_anonymizer._model._meta.verbose_name_plural.title()
            object_count = model_anonymizer.get_total()
            if object_count:
                with tqdm(desc=f"Anonymizing {model_name}", total=object_count) as pbar:
                    for processed in model_anonymizer.run_anonymizer():
                        pbar.update(processed)
            else:
                self.stdout.write(
                    f"Skipping {model_name}, no objects found to anonymize"
                )
