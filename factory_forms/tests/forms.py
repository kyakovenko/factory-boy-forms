# -*- coding: utf-8 -*-
__authors__ = 'Kirill S. Yakovenko, '
__email__ = 'contacts@crystalnix.com'
__copyright__ = 'Copyright 2014, Crystalnix'

from django import forms

CHOICES = (
    ('1', '1'),
    ('2', '2'),
    ('3', '3'),
    ('4', '4'),
    ('5', '5'),
)


class DjangoTestForm(forms.Form):
    boolean = forms.BooleanField()
    chars = forms.CharField(max_length=100)
    choice = forms.ChoiceField(CHOICES)
    #date = forms.DateField()
    #datetime = forms.DateTimeField()
    #decimal = forms.DecimalField()
    email = forms.EmailField()
    #float = forms.FloatField()
    #integer = forms.IntegerField()
    #ip = forms.IPAddressField()
    #multiple_choice = forms.MultipleChoiceField(CHOICES)
    #null_boolean = forms.NullBooleanField()
