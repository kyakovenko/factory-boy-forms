# -*- coding: utf-8 -*-
__authors__ = 'Kirill S. Yakovenko, '
__email__ = 'contacts@crystalnix.com'
__copyright__ = 'Copyright 2014, Crystalnix'

from factory import fuzzy
from nose.tools import assert_in, assert_equal, assert_is_none

from ..factories import FormFactory


class FakeFormFactory(FormFactory):
    field = fuzzy.FuzzyText()


# class FakeFormSetFactory(FormSetFactory):
#     _sub_factory = FakeFormFactory


class FakeFormFactoryWithPrefix(FormFactory):
    field = fuzzy.FuzzyText()

    class Meta:
        prefix = 'prefix'


def test_form_factory_attributes():

    data = FakeFormFactory.attributes()
    assert_in('field', data)

    data = FakeFormFactory.attributes(prefix='test')
    assert_in('test-field', data)

    data = FakeFormFactoryWithPrefix.attributes()
    assert_in('prefix-field', data)

    data = FakeFormFactoryWithPrefix.attributes(prefix='test')
    assert_in('test-field', data)

