#!/usr/bin/python3
# -*- coding: utf-8 -*-

import url
from urllib.parse import parse_qs
import re

utm=('utm_source', 'utm_medium', 'utm_campaign', 'utm_term', 'utm_content')
re_http = re.compile(r"^https?://.*")
re_url = re.compile(r"https?:\/\/(?:www\.)?[-a-zA-Z0-9@:%._\+~#=]{2,256}\.[a-z]{2,6}\b(?:[-a-zA-Z0-9@:%_\+.~#?&//=]*)")

def get_http_param(q):
    qs = parse_qs(q)
    http_param = set()
    for ps in qs.values():
        for p in ps:
            if re_http.match(p):
                http_param.add(p)
    return http_param

def clean_url(u):
    u = url.parse(u)
    u.deparam(utm)
    u.strip()
    u.canonical()
    u.abspath()
    u.unescape()
    https_param = get_http_param(u.query)
    if len(https_param)==1:
        u = https_param.pop()
        return clean_url(u)
    u = str(u)
    return u

if __name__=="__main__":
    import sys
    u = sys.argv[1]
    print(u)
    u = clean_url(u)
    print(u)
