# -*- coding: utf-8 -*-
__author__ = 'Kirill S. Yakovenko'
__email__ = 'kirill.yakovenko@gmail.com'
__copyright__ = 'Copyright 2014, Crystalnix'

from nose.tools import assert_true, assert_equal, assert_is_none

from .forms import DjangoTestForm
from ..factories import FormFactory
from ..utils import construct_factory_from_form


def test_construct_factory_from_form():
    form_factory = construct_factory_from_form(DjangoTestForm)
    assert_true(issubclass(form_factory, FormFactory))
    assert_equal(form_factory._meta.form, DjangoTestForm)
    assert_is_none(form_factory._meta.fields)
    assert_is_none(form_factory._meta.exclude)
    assert_equal(form_factory._meta.settings, {})
