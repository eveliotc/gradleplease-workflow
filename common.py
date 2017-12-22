# -*- coding: utf-8 -*-
__author__ = 'eveliotc'
__license__ = 'See LICENSE'

import alfred
from alfred import Item
import sys
from subprocess import Popen, PIPE

def json_to_obj(x):
    if isinstance(x, dict):
        return type('X', (), {k: json_to_obj(v) for k, v in x.iteritems()})
    else:
        return x

def join_query(dic):
    return ' '.join(dic)

def le_result(r, exit = True):
    alfred.write(r)
    if exit:
        sys.exit()

def xml_result(r, exit = True):
    if len(r) < 1:
        empty_result(exit)
    else:
        le_result(alfred.xml(r), exit)

def empty_result(exit = True):
    empty = Item(
            attributes={'uid': alfred.uid('empty'), 'arg': ''},
            title='Gradle Please',
            subtitle=u':( Nothing found.',
            icon=u'icon.png')
    xml_result([empty], exit)

def apple_script(scpt, args=[]):
     p = Popen(['osascript', '-'] + args, stdin=PIPE, stdout=PIPE, stderr=PIPE)
     stdout, stderr = p.communicate(scpt)
     return stdout

def tell_alfred(what):
    apple_script('tell application "Alfred 2" to search "%s"' % what)

# TODO refactor gp.py to use this instead of dynamic obj
class Pom(object):
    a = ''
    g = ''
    p = ''
    latestVersion = ''
    source = ''

    @property
    def id(self):
        return self.g + ':' + self.a

    def __repr__(self):
        #notjson #justdebugginthings
        return '{id:%s a:%s g:%s p:%s v:%s}' % (self.id, self.a, self.g, self.p, self.latestVersion)
