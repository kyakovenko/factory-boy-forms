# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import unicode_literals

__authors__ = 'Kirill S. Yakovenko, '
__email__ = 'contacts@crystalnix.com'
__copyright__ = 'Copyright 2014, Crystalnix'

import six
from factory import fuzzy
from django.forms import BaseForm
from django.forms.formsets import BaseFormSet

from . import unicode_letters
from ..fuzzy import FuzzyModelChoice, FuzzyModelMultiChoice, FuzzyRegex


class DjangoFormConverter(object):

    def __init__(self, form):
        self.form = form

    @staticmethod
    def can_convert(form):
        return issubclass(form, (BaseForm, BaseFormSet))

    def fields(self):
        return six.iteritems(getattr(self.form, 'base_fields', {}))

    def convert_field(self, form, field, field_args={}):
        """
        Returns a factory field for a single form field.

        :param form:
            The ``django.forms.Form`` class that contains the field.
        :param field:
            The form field: a ``django.forms.Field`` instance.
        :param field_args:
            Optional keyword arguments to construct the property.
        """

        # check for generic property
        prop_type_name = type(field).__name__
        converter = getattr(self, 'convert_{0}'.format(prop_type_name), None)
        if converter is not None:
            return converter(field, **field_args)
        else:
            return self.fallback_converter(field, **field_args)

    def fallback_converter(self, field, **kwargs):
        prop_type_name = type(field).__name__
        raise NotImplementedError('There is no a converter for "{0}" field '.format(prop_type_name))

    def convert_CharField(self, field, **kwargs):
        attrs = {
            'length': field.max_length or 1000,
            'chars': unicode_letters
        }
        attrs.update(kwargs)
        return fuzzy.FuzzyText(**attrs)

    def convert_TypedChoiceField(self, field, **kwargs):
        attrs = {
            'choices': [i[0] for i in field.choices if not field.required or i[0]],
        }
        attrs.update(kwargs)
        return fuzzy.FuzzyChoice(**attrs)

    convert_ChoiceField = convert_TypedChoiceField

    def convert_EmailField(self, field, **kwargs):
        attrs = {
            'length': (field.max_length or 1000) - 9,
            'suffix': '@mail.com'
        }
        attrs.update(kwargs)
        return fuzzy.FuzzyText(**attrs)

    def convert_ModelChoiceField(self, field, **kwargs):
        attrs = {
            'empty_value': None if field.required else field.empty_values[0],
            'queryset':  field.choices.queryset,
        }
        attrs.update(kwargs)
        return FuzzyModelChoice(**attrs)

    def convert_ModelMultipleChoiceField(self, field, **kwargs):
        attrs = {
            'empty_value': None if field.required else field.empty_values[0],
            'queryset':  field.choices.queryset,
        }
        attrs.update(kwargs)
        return FuzzyModelMultiChoice(**attrs)

    def convert_RegexField(self, field, **kwargs):
        attrs = {
            'regex': field._regex,
            'max_length': field.max_length
        }
        attrs.update(kwargs)
        return FuzzyRegex(**attrs)

    def convert_BooleanField(self, field, **kwargs):
        attrs = {
            'choices': [True, False]
        }
        attrs.update(kwargs)
        return fuzzy.FuzzyChoice(**attrs)
    
    def convert_IntegerField(self, field, **kwargs):
        attrs = {
            'low': field.min_value if field.min_value else -100,
            'high': field.max_value if field.max_value else 100,
        }
        attrs.update(kwargs)
        return fuzzy.FuzzyInteger(**attrs)
