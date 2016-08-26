# -*- coding: utf-8 -*-
# pylint: disable=import-error
'''
Template filters for excellent text formatting.
'''

import re

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


@smart_filter
def hanging(text):
    '''
    Wrap punctuation with <span> to apply negative margin. Prepend with empty
    <span> when adjacent to other text to offset the negative margin when not
    on the column edge.
    '''

    double_width = [
        '&quot;',
        '"',
        "“",
        "„",
        "”",
        "&ldquo;",
        "&OpenCurlyDoubleQuote;",
        "&#8220;",
        "&#x0201C;",
        "&rdquor;",
        "&rdquo;",
        '&CloseCurlyDoubleQuote;',
        '&#8221;',
        '&ldquor;',
        '&bdquo;',
        '&#8222;'
    ]
    single_width = [
        "'",
        '&prime;',
        '&apos;',
        '&lsquo;',
        '&rsquo;',
        '‘',
        '’'
    ]

    def _pull(classname, content):
        return '''<span class="pull-%s">%s</span>''' % (classname, content)

    def _push(classname, content):
        return '''<span class="push-%s">%s</span>''' % (classname, content)

    def _hasAdjacentText(node):
        '''
        if node.prev && node.prev.children && node.prev.children.length
            lastChild = node.prev.children.slice(-1)[0]

            if lastChild && lastChild.type === 'text'
                return true

        if !node.parent() || !nod).parent().length
            return false

        parentPrev = node.parent()[0].prev

        Ensure the parent has text content and is not simply a newline seperating tags.
        if parentPrev && parentPrev.type === 'text' && parentPrev.data.trim()
            return true

        return false
        '''
        
    if len(text) < 2:
        output = text
    else:
        '''
        for each words
            for each in double_width
                punctuation = double_width[j]
                if words[i].slice(0, punctuation.length) === punctuation
                    insert = pull('single', punctuation)

                    if (words[(i-1)])
                        words[(i-1)] = words[(i-1)] + _push('single')
                    else if hasAdjacentText
                        insert = _push('single') + insert

                    words[i] = insert + words[i].slice(punctuation.length)

            for each in single_width
                ...
        '''

    return output
