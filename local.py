# -*- coding: utf-8 -*-
__author__ = 'eveliotc'
__license__ = 'See LICENSE'

import sys
from os import walk, environ, path

try:
    import xml.etree.cElementTree as ET
except ImportError:
    import xml.etree.ElementTree as ET

# TODO refactor gp.py to use this instead of dynamic obj
class Pom(object):
    a = ''
    g = ''
    p = ''
    latestVersion = ''

    @property
    def id(self):
        return self.g + ':' + self.a

    def __repr__(self):
        #notjson #justdebugginthings
        return '{id:%s a:%s g:%s p:%s v:%s}' % (self.id, self.a, self.g, self.p, self.latestVersion)

def findtext(element, tag, alt='', ns='http://maven.apache.org/POM/4.0.0'):
    fulltag = str(ET.QName(ns, tag))
    return element.findtext(fulltag, alt)

def to_pom(project):
    pom = Pom()
    pom.a = findtext(project, 'artifactId')
    pom.g = findtext(project, 'groupId')
    pom.p = findtext(project, 'packaging', 'jar')
    pom.latestVersion = findtext(project, 'version')
    return pom

def local_search(query):
    # TODO a better more relaxed (partial) search e.g. supportv4 should match, fuzzywuzzy?
    docs = []
    if len(query) < 1:
        return docs

    andys_home = path.normpath(environ['ANDROID_HOME'])
    extras_room = path.join(andys_home, 'extras')

    for (dirpath, dirnames, filenames) in walk(extras_room):
        if 'm2repository' in dirpath:
            for file in filenames:
                if file.endswith('.pom') and query in file:
                    fullpath = path.join(dirpath, file)
                    root = ET.parse(fullpath).getroot()
                    doc = to_pom(root)
                    docs.append(doc)

    return sorted(docs, key=lambda doc: doc.latestVersion, reverse=True)

def main(args):
    print local_search(' '.join(args))
    pass

if __name__ == '__main__':
    main(sys.argv[1:])
