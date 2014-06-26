#!/usr/bin/env python
# -*- coding: utf-8 -*-

import json
from collections import OrderedDict

# a = "system auth user modify username <username> password <password> [rolename <rolename> [mail <mail>]]"
a = "system auth user modify username <username> password <password>"



def list_to_deep_dict(s, d):
    if not s:
        return d
    item = s.pop()
    tmp = OrderedDict()
    if item.startswith("<"):
        k = item.strip("<>")
        tmp[k] = OrderedDict()
        #tmp[k]["cmd"] = "tst.py"
        tmp[k]["token"] = 1
        for i in d:
            tmp[k][i] = d[i]
    else:
        tmp[item] = d
    return list_to_deep_dict(s, tmp)

if __name__ == "__main__":
    a_list = a.split()
    r = list_to_deep_dict(a_list, {"cmd": "test.py"})
    print json.dumps(r, indent=2)
