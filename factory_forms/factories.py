# -*- coding: utf-8 -*-
__author__ = 'Kirill S. Yakovenko'
__email__ = 'kirill.yakovenko@gmail.com'
__copyright__ = 'Copyright 2014, Kirill S. Yakovenko'

from factory.fuzzy import FuzzyText, FuzzyChoice

from . import unicode_letters
from .fuzzy import FuzzyModelChoice, FuzzyMultiModelChoice, FuzzyRegex


class FormConverter(object):

    def convert(self, form, field, field_args={}):
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
        return FuzzyText(**attrs)

    def convert_TypedChoiceField(self, field, **kwargs):
        attrs = {
            'choices': [i[0] for i in field.choices],
        }
        attrs.update(kwargs)
        return FuzzyChoice(**attrs)

    def convert_EmailField(self, field, **kwargs):
        attrs = {
            'length': field.max_length - 9,
            'suffix': '@mail.com'
        }
        attrs.update(kwargs)
        return FuzzyText(**attrs)

    def convert_ModelChoiceField(self, field, **kwargs):
        attrs = {
            'choices': field.choices,
        }
        attrs.update(kwargs)
        return FuzzyModelChoice(**attrs)

    def convert_ModelMultipleChoiceField(self, field, **kwargs):
        attrs = {
            'choices': field.choices,
        }
        attrs.update(kwargs)
        return FuzzyMultiModelChoice(**attrs)

    def convert_RegexField(self, field, **kwargs):
        attrs = {
            'regex': field._regex,
            'max_length': field.max_length
        }
        attrs.update(kwargs)
        return FuzzyRegex(**attrs)