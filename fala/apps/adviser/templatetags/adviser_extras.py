# -*- coding: utf-8 -*-
from django import template

register = template.Library()


def multiply(value, arg):
    return value * arg


def val(field):
    return field.value() if field.value() else ''


def checked(field, index):
    return ' checked' if field.data == field[index].choice_value else ''


def selected(field, index):
    return ' checked' if field.data and field[index].choice_value in \
                                        field.data else ''


register.filter('multiply', multiply)
register.filter('checked', checked)
register.filter('selected', selected)
register.filter('val', val)
