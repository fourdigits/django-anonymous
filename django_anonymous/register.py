from importlib import import_module
from django.apps import apps

registered_models = {}


def register(*models):
    """Register an anonymizer for one or multiple models"""
    from .anonymizer import Anonymizer

    def _class_wrapper(anonymizer_class):
        if not models:
            raise ValueError('At least one model must be passed to register.')

        if not issubclass(anonymizer_class, Anonymizer):
            raise ValueError('Wrapped class must subclass Anonymizer')

        for model in models:
            registered_models[model] = anonymizer_class(model)

        return anonymizer_class
    return _class_wrapper


def load_anonymizer():
    """Load all Anonymizer classes"""
    for app in apps.get_app_configs():
        for module in ["anonymizer", "anonymous", "anon"]:
            try:
                import_module('{}.{}'.format(getattr(app.module, '__package__'), module))
            except ImportError:
                pass
