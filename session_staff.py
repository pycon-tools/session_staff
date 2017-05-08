#!/usr/bin/env python
#  count sessions staff signed up
#  -n to emit names
#
# assumes you're using python3.6 or later (fstrings)

from bs4 import BeautifulSoup
import requests
import sys
import time

# session staff is interesting close to conference, so
#  no need to parameterize this:
url = "https://us.pycon.org/" + time.strftime('%Y') + "/schedule/sessions/"
soup = BeautifulSoup(requests.get(url).text, "html.parser")
# there's exactly one of box-content - which contain the sessions
# - this was 2016: entries = soup.body.div.select(".box-content ul li ul li")
# - in 2017, the session staff are in a well div
# each of the sessions:
sessions = soup.body.select('.well')
# each volunteer slot w/in a session:
slots = [s.select('ul li') for s in sessions]
chairs = runners = 0
names = []
for s in slots:
    # s contains at most two <li>'s, i.e. two names
    #  or "No volunteers..."
    for e in s:
        if len(e) < 2: # or 3 - then "No volunteers"
            continue       
        names.append( e.contents[-1].lstrip(': ').rstrip() )
        job = e.text[1:]  # contents start w/ "\nSession..."
        if job.startswith('Session Chair'):
            chairs += 1
        elif job.startswith('Session Runner'):
            runners += 1

# uniq:
n = list(set(names))
# print names
if sys.argv[-1] == '-n':
    n.sort()
    for i in n:
        print(f"({names.count(i)}) {i}")
else:  # print count
    print( f"Sessions:   {len(sessions)}")
    print( f"Volunteers: {len(names)} slots, {len(n)} volunteers" )
    print( f"   Chairs:  {chairs}  ")
    print( f"   Runners: {runners}  ")
    print( f"=> Short:  ({len(sessions)*2 - len(names)})" )
