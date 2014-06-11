# -*- coding: utf-8 -*-
__authors__ = 'Kirill S. Yakovenko, '
__email__ = 'contacts@crystalnix.com'
__copyright__ = 'Copyright 2014, Crystalnix'

import mock
from nose.tools import assert_equal, assert_is_none, assert_in, assert_true, assert_false

from .forms import SimpleDjangoFormSet
from ..django import FormSetFactory, TOTAL_FORM_COUNT, INITIAL_FORM_COUNT, MAX_NUM_FORM_COUNT


class FakeFormSetFactory(FormSetFactory):
    class Meta:
        form = SimpleDjangoFormSet


def test_form_set_factory_metaclass():
    assert_equal(FakeFormSetFactory._meta.form, SimpleDjangoFormSet)
    assert_is_none(FakeFormSetFactory._meta.fields)
    assert_is_none(FakeFormSetFactory._meta.exclude)
    assert_equal(FakeFormSetFactory._meta.settings, {})


def test_form_set_factory_attributes():
    data = FakeFormSetFactory.attributes()
    assert_in('form-' + TOTAL_FORM_COUNT, data)
    assert_in('form-' + INITIAL_FORM_COUNT, data)
    assert_in('form-' + MAX_NUM_FORM_COUNT, data)


@mock.patch.dict('django.conf.os.environ', {"DJANGO_SETTINGS_MODULE": 'factory_forms.tests.djapp.settings'})
def test_form_validation():
    data = FakeFormSetFactory.attributes(prefix='prefix', count=1)
    form_set = SimpleDjangoFormSet(data, prefix='prefix')
    assert_true(form_set.is_valid())
    assert_true(form_set[0].has_changed())
