# -*- coding: utf-8 -*-
__author__ = 'eveliotc'
__license__ = 'See LICENSE'

import alfred
from alfred import Item
from common import empty_result, join_query, json_to_obj, xml_result
from local import local_search
from mavencentral import maven_central_search


CONFIGURATIONS = ('compile', 'provided', 'runtime', 'instrumentTest', 'androidTest', 'testCompile',)
DEFAULT_CONFIGURATION = 'compile'

EXCLUDE_PACKAGING = ('apk', 'pom')
DEFAULT_PACKAGING = 'jar'

args = alfred.args()
configuration = DEFAULT_CONFIGURATION
count = len(args)

if count < 1:
    empty_result()
elif count == 1:
    query = args[0]
elif args[0] in CONFIGURATIONS:
    configuration = args[0]
    query = join_query(args[1:])
else:
    query = join_query(args)

if (len(query) == 0):
    empty_result()

# TODO async this
try:
    localDocs = local_search(query)
    # TODO refactor doc to Item code below so we can send partial results here e.g. xml_result(results, False)
except: # pokemon catch em all
    localDocs = [] # TODO do something about it like let user know to define $ANDROID_HOME, install local repo etc.

# TODO async this
(mavenCentralDocs, suggestions) = maven_central_search(query)


fullDocs = []
fullDocs.extend(localDocs)
fullDocs.extend(mavenCentralDocs)

results = []
for doc in fullDocs:
    doc = json_to_obj(doc)
    packaging = doc.p
    id = doc.id
    if packaging not in EXCLUDE_PACKAGING:
        # If not jar use @aar or whatever
        atPackaging = u'' if packaging.lower() == DEFAULT_PACKAGING else '@' + doc.p
        # In case of compiler dependency use provided
        lineConfiguration = u'provided' if 'compiler' in id else configuration
        depLine = u"%s '%s:%s%s'" % (lineConfiguration, id, doc.latestVersion, atPackaging)
        source = doc.source if hasattr(doc, 'source') and len(doc.source) > 0 else 'Maven Central'
        item = Item(
            attributes={'uid': alfred.uid(id), 'arg': depLine},
            title=doc.a,
            subtitle=u'Paste (from %s): %s' % (source, depLine),
            icon=u'icon.png'
        )
        results.append(item)

for suggestion in suggestions:
    if isinstance(suggestion, dict):
        for sug in suggestion['suggestion']:
            item = Item(
            attributes={'uid': alfred.uid(sug), 'arg': u'search=%s' % sug},
            title=sug,
            subtitle=u"Did you mean '%s'..." % sug,
            icon=u'icon.png'
        )
        results.append(item)

xml_result(results)