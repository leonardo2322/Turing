class DictMixin:
    def to_dict(self):
        """
        Convierte el objeto del modelo en un diccionario.
        """
        # Utiliza el método _meta para obtener los campos del modelo
        data = {}
        for field in self._meta.get_fields():
            if field.concrete and not field.many_to_many and not field.one_to_one:
                value = getattr(self, field.name)
                if callable(value):
                    value = value()
                data[field.name] = value
            elif field.many_to_many:
                data[field.name] = list(getattr(self, field.name).values())
            elif field.one_to_one:
                data[field.name] = getattr(self, field.name).to_dict()
        return data
