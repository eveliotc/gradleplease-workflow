# -*- coding: utf-8 -*-
__author__ = 'xrubioj'
__license__ = 'See LICENSE'

import sys
# sigh not using requests to minimize deps and simplify this little scrypt
import urllib
import urllib2
import json
from common import json_to_obj, Pom


def to_pom(doc):
    docs = []
    for system_id in doc['system_ids']:
        #for version in doc.versions: # we will just use latest_version
        parts = system_id.split(':', 2)

        pom = Pom()
        pom.g = parts[0]
        pom.a = parts[1] if len(parts) > 1 else ''
        pom.p = 'jar'
        pom.latestVersion = doc['latest_version']
        pom.source = 'jcenter'

        docs.append(pom)

    return docs


def jcenter_search(query):

    base_url = u'https://bintray.com/api/v1/search/packages/maven?q=%s*'
    url = base_url % urllib.quote_plus(query)

    parsed_json = json.load(urllib2.urlopen(url))
    root = json_to_obj(parsed_json)

    p_docs = []
    for doc in root:
        docs = to_pom(doc)
        p_docs.extend(docs)

    s_docs = sorted(p_docs, key=lambda doc: doc.latestVersion, reverse=True)

    return s_docs


def main(args):
    print maven_central_search(' '.join(args))
    pass


if __name__ == '__main__':
    main(sys.argv[1:])
