# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db.models import (ForeignKey, OneToOneField, ManyToManyField)


class DefaultAdminMixin:
    raw_id_fields = ()

    def __init__(self, model, admin_site, *args, **kwargs):
        self.raw_id_fields = self.setup_raw_id_fields(model)
        super().__init__(model, admin_site, *args, **kwargs)

    def setup_raw_id_fields(self, model):
        return tuple(
            f.name for f in model._meta.get_fields() if
            isinstance(f, ForeignKey) or
            isinstance(f, OneToOneField) or
            isinstance(f, ManyToManyField)
        )
