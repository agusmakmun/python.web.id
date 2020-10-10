"""
Base API fields serializers
"""
# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from rest_framework import serializers


class StringListField(serializers.ListField):
    """ serializer for string list fields """
    child = serializers.CharField()


class IntegerListField(serializers.ListField):
    """ serializer for integer list fields """
    child = serializers.IntegerField()


class DictListField(serializers.ListField):
    """ serializer for dict list fields """
    child = serializers.DictField()


class DynamicFieldsModelSerializer(serializers.ModelSerializer):
    """
    A ModelSerializer that takes an additional `fields` argument that
    controls which fields should be displayed.

    https://www.django-rest-framework.org/api-guide/serializers/#example
    """

    def __init__(self, *args, **kwargs):
        # Don't pass the 'fields' arg up to the superclass
        fields = kwargs.pop('fields', None)

        # Instantiate the superclass normally
        super().__init__(*args, **kwargs)

        if fields is not None:
            # Drop any fields that are not specified in the `fields` argument.
            allowed = set(fields)
            existing = set(self.fields)
            for field_name in existing - allowed:
                self.fields.pop(field_name)
