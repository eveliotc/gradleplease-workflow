# -*- coding: utf-8 -*-
__author__ = 'eveliotc'
__license__ = 'See LICENSE'

import alfred
from alfred import Item
import urllib, urllib2 # sigh not using requests to minimize deps and simplify this little scrypt
import json
from common import empty_result, join_query, json_to_obj, xml_result

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

url = u'http://search.maven.org/solrsearch/select?wt=json&q=%s' % urllib.quote_plus(query)

json = json.load(urllib2.urlopen(url))
root = json_to_obj(json);

docs = root.response.docs
sortedDocs = sorted(docs, key=lambda doc: doc['latestVersion'], reverse=True)

results = []
for doc in sortedDocs:
    doc = json_to_obj(doc)
    packaging = doc.p
    id = doc.id
    if packaging not in EXCLUDE_PACKAGING:
        # If not jar use @aar or whatever
        atPackaging = u'' if packaging.lower() == DEFAULT_PACKAGING else '@' + doc.p
        # In case of compiler dependency use provided
        lineConfiguration = u'provided' if 'compiler' in id else configuration
        depLine = u"%s '%s:%s%s'" % (lineConfiguration, id, doc.latestVersion, atPackaging)
        item = Item(
            attributes={'uid': alfred.uid(id), 'arg': depLine},
            title=doc.a,
            subtitle=u'Paste %s' % depLine,
            icon=u'icon.png'
        )
        results.append(item)

suggestions = root.spellcheck.suggestions

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