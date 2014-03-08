# -*- coding: utf-8 -*-
__author__ = 'eveliotc'
__license__ = 'See LICENSE'

import alfred
from common import le_result, tell_alfred

args = alfred.args()
query = args[0]

if query.startswith("search="):
    query = query[7:]
    tell_alfred(u"gp %s" % query)
else:
    le_result(query)