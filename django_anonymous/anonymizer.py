class Anonymizer:
    SELECT_CHUNK_SIZE = 500
    UPDATE_BATCH_SIZE = 100
    ANONYMIZE_EMPTY_FIELD = False

    def __init__(self, model):
        self._fields = self._get_fields()
        self._model = model

    def get_total(self):
        return self.get_queryset().count()

    def run_anonymizer(self):
        for batch in self.get_batches():
            self._model.objects.bulk_update(
                [self.anonymize_object(obj) for obj in batch],
                fields=self._fields,
            )
            yield len(batch)

    def _get_fields(self):
        reserved_names = list(Anonymizer.__dict__.keys())
        return {
            name: getattr(self, name)
            for name in dir(self)
            if not name.startswith("__") and name not in reserved_names
        }

    def get_queryset(self):
        return self._model.objects.get_queryset()

    def get_batches(self):
        batch = []
        for obj in self.get_queryset().iterator(chunk_size=self.SELECT_CHUNK_SIZE):
            batch.append(obj)
            if len(batch) >= self.UPDATE_BATCH_SIZE:
                yield batch
                batch = []
        if batch:
            yield batch

    def get_object_seed(self, obj):
        return obj.id

    def anonymize_object(self, obj):
        for field, value in self._fields.items():
            if not self.ANONYMIZE_EMPTY_FIELD and not getattr(obj, field):
                continue

            if callable(value):
                new_value = value(obj, self.get_object_seed(obj))
            else:
                new_value = value

            # using obj.__dict__ instead of setattr for performance reasons
            # see https://stackoverflow.com/a/9791053/639465
            obj.__dict__[field] = new_value
        return obj
