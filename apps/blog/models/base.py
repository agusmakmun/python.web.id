# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.utils.html import strip_tags
from django.contrib.contenttypes.models import ContentType


class TimeStampedModel(models.Model):
    """
    TimeStampedModel

    An abstract base class model that provides self-managed
    "created_at", "updated_at" and "deleted_at" fields.
    """
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True, null=True, blank=True)
    deleted_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        abstract = True


class DefaultManager(models.Manager):
    """
    Class to assign as ORM queryset manager,
    for example usage:

    class ModelName(models.Model):
        ...
        objects = DefaultManager()

    >>> ModelName.objects.published()
    >>> ModelName.objects.deleted()
    """

    def published(self):
        """ return queryset for not-deleted objects only. """
        return self.filter(deleted_at__isnull=True)

    def deleted(self):
        """ return queryset for deleted objects only. """
        return self.filter(deleted_at__isnull=False)

    def get_or_none(self, **kwargs):
        """ function to get the object or None. """
        try:
            return self.get(**kwargs)
        except (Exception, self.model.DoesNotExist):
            return None


class ContentTypeModel(object):

    def get_content_type(self):
        """ function to get the content_type object for current model """
        return ContentType.objects.get_for_model(self)


class ContentTypeToGetModel(ContentTypeModel):

    """
    requires fields:
        - content_type: FK(ContentType)
        - object_id: PositiveIntegerField()
    """

    def get_related_object(self):
        """
        return the related object of content_type.
        eg: <Question: Holisticly grow synergistic best practices>
        """
        # This will return an error: MultipleObjectsReturned
        # if you return self.content_type.get_object_for_this_type()
        # So, i handle it with this one:
        model_class = self.content_type.model_class()
        return model_class.objects.get(id=self.object_id)

    @property
    def _model_name(self):
        """
        return lowercase of model name.
        eg: `question`, `answer`
        """
        return self.get_related_object()._meta.model_name


class XSSModelCleaner(object):
    """
    class to handle the xss injection
    before it save into database by using `strip_tags`.

    class ModelName(XSSModelCleaner, models.Model):
        pass
    """
    excluded_xss_model_fields = []

    def save(self, *args, **kwargs):
        # handle the xss injection
        for field in self._meta.fields:
            if field.name not in self.excluded_xss_model_fields:
                value = getattr(self, field.name)
                if isinstance(value, str):
                    value_clean = strip_tags(value)
                    setattr(self, field.name, value_clean)
        return super().save(*args, **kwargs)
