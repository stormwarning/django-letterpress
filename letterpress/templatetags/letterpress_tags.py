# -*- coding: utf-8 -*-
# pylint: disable=import-error
'''
Template filters for excellent text formatting.
'''

from django import template
from django.utils.html import conditional_escape
from django.utils.safestring import mark_safe

register = template.Library()

def smart_filter(fn):
    '''
    Escapes filter's content based on template autoescape mode and marks
    output as safe.
    '''
    def wrapper(text, autoescape=None):
        '''
        Filter output wrapper.
        '''
        if autoescape:
            esc = conditional_escape
        else:
            esc = lambda x: x

        return mark_safe(fn(esc(text)))

    wrapper.needs_autoescape = True
    register.filter(fn.__name__, wrapper)

    return wrapper
