#!/usr/bin/env python
#  count sessions staff signed up
#  -n to emit names

from bs4 import BeautifulSoup
import requests
import sys

url = "https://us.pycon.org/2016/schedule/sessions/"
soup = BeautifulSoup(requests.get(url).text, "html.parser")
# there's exactly one of box-content - which contain the sessions
entries = soup.body.div.select(".box-content ul li ul li")
names = [e.contents[-1].lstrip(': ').rstrip() for e in entries]
# print names
if sys.argv[-1] == '-n':
    # uniq:
    n = list(set(names))
    n.sort()
    print( "\n".join(n) )
else:  # print count
    print( len(names) )
