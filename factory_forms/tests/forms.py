# -*- coding: utf-8 -*-
__authors__ = 'Kirill S. Yakovenko, '
__email__ = 'contacts@crystalnix.com'
__copyright__ = 'Copyright 2014, Crystalnix'

import wtforms
from django import forms as django_forms
from django.forms.formsets import formset_factory


CHOICES = (
    ('1', '1'),
    ('2', '2'),
    ('3', '3'),
    ('4', '4'),
    ('5', '5'),
)


class SimpleDjangoForm(django_forms.Form):
    field1 = django_forms.CharField(required=True)
    field2 = django_forms.CharField()


class SimpleDjangoFormSet(formset_factory(SimpleDjangoForm,
                                          extra=3, can_order=True, can_delete=True, max_num=10, validate_max=True)):
    pass


class DjangoTestForm(django_forms.Form):
    boolean = django_forms.BooleanField()
    chars = django_forms.CharField(max_length=100)
    choice = django_forms.ChoiceField(CHOICES)
    #date = django_forms.DateField()
    #datetime = django_forms.DateTimeField()
    #decimal = django_forms.DecimalField()
    email = django_forms.EmailField()
    #float = django_forms.FloatField()
    #integer = django_forms.IntegerField()
    #ip = django_forms.IPAddressField()
    #multiple_choice = django_forms.MultipleChoiceField(CHOICES)
    #null_boolean = django_forms.NullBooleanField()


class SimpleWTForm(wtforms.Form):
    field1 = wtforms.StringField()
    field2 = wtforms.StringField()
