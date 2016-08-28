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
IGNORE = (
    'head', 'code', 'kbd', 'pre', 'samp', 'script', 'style', 'tt', 'xmp',
    '[class^="pull-"]', '[class^="push-"]', '.small-caps'
)


def smart_filter(funct):
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

        return mark_safe(funct(esc(text)))

    wrapper.needs_autoescape = True
    register.filter(funct.__name__, wrapper)

    return wrapper


def _process_text_nodes(text_to_proc, proc):
    for child_node in text_to_proc.childNodes:
        # Should this node be ignored?
        if text_to_proc.contains(IGNORE):
            return False

        # Is it a TEXT_NODE?
        if child_node.nodeType == 3:
            content = child_node.data

            content = content.re(r'/&#39;/g, "\'"')
            content = content.re(r'/&quot;/g, \'"\'')

            child_node.data = content
            child_node.replaceWith(proc(content, child_node))

        # Then keep looking.
        else:
            _process_text_nodes(child_node, proc)


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

    def _has_adjacent_text(test_node):
        '''
        Test for text adjacent to current word, even if within a different node.
        '''
        test_sibling = test_node.previousSibling

        if test_sibling and test_sibling.childNodes and len(test_sibling.childNodes):
            last_child = test_sibling.childNodes.slice(-1)[0]

            if last_child and last_child.nodeType == 3:
                return True

        if not test_node.parentNode or not len(test_node.parentNode):
            return False

        previous_parent = test_node.parentNode[0].previousSibling

        # Ensure the parent has text content and is not simply a newline seperating tags.
        if previous_parent and previous_parent.nodeType == 3 and previous_parent.data.trim():
            return True

        return False

    if len(text) < 2:
        output = text
    else:
        output = _process_text_nodes(text, _proc_hanging)

    def _proc_hanging(content, child_node):
        # Remove consecutive double spaces then create array of distinct words.
        words = child_node.split(' ').join(' ').split(' ')

        for i, word in enumerate(words):
            for punc in double_width:
                punctuation = punc
                if word.slice(0, len(punctuation)) == punctuation:
                    insert = _pull('double', punctuation)

                    if words[i-1]:
                        words[i-1] = words[i-1] + _push('double', '')
                    elif _has_adjacent_text(child_node):
                        insert = _push('double', '') + insert

                    word = insert + word.slice(len(punctuation))

            for punc in single_width:
                punctuation = punc
                if word.slice(0, len(punctuation)) == punctuation:
                    insert = _pull('single', punctuation)

                    if words[i-1]:
                        words[i-1] = words[i-1] + _push('single', '')
                    elif _has_adjacent_text(child_node):
                        insert = _push('single', '') + insert

                    word = insert + word.slice(len(punctuation))

        return words

    return output
