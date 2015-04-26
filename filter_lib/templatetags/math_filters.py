# -*- coding: utf-8 -*-

from django import template

register = template.Library()


@register.filter
def div(value, arg):
    """
    Divides the value; argument is the divisor.
    Returns empty string on any error.
    The usage is like:
        {{ var|div:2 }}
    """
    try:
        value = int(value)
        arg = int(arg)
        if arg:
            return value / arg
    except:
        pass
    return ''


@register.filter
def rem(value, arg):
    """
    Divides the value; argument is the divisor.
    Returns empty string on any error.
    The usage is like:
        {{ var|rem:2 }}
    """
    try:
        value = int(value)
        arg = int(arg)
        if arg:
            return value % arg
    except:
        pass
    return ''


@register.filter
def mult(value, arg):
    """
    Multiplication of the integer values;
    Returns empty string on any error.
    The usage is like:
        {{ var|mult:2 }}
    """
    try:
        value = int(value)
        arg = int(arg)
        if arg:
            return value * arg
    except:
        pass
    return ''

@register.filter
def neg(value):
    """
    Negation of the integer values;
    Returns empty string on any error.
    The usage is like:
        {{ var|neg }}
    """
    try:
        value = int(value)
        return -value
    except:
        pass
    return ''
