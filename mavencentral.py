# -*- coding: utf-8 -*-
__author__ = 'eveliotc'
__license__ = 'See LICENSE'

import sys
# sigh not using requests to minimize deps and simplify this little scrypt
import urllib
import urllib2
import json
from common import json_to_obj


def maven_central_search(query):

    base_url = u'http://search.maven.org/solrsearch/select?wt=json&q=%s'
    url = base_url % urllib.quote_plus(query)

    parsed_json = json.load(urllib2.urlopen(url))
    root = json_to_obj(parsed_json)
    docs = root.response.docs
    s_docs = sorted(docs, key=lambda doc: doc['latestVersion'], reverse=True)
    suggestions = root.spellcheck.suggestions

    return (s_docs, suggestions)


def main(args):
    print maven_central_search(' '.join(args))
    pass


if __name__ == '__main__':
    main(sys.argv[1:])
