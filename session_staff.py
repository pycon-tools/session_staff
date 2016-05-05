#!/usr/bin/env python
#  count sessions staff signed up

from bs4 import BeautifulSoup
import requests

url = "https://us.pycon.org/2016/schedule/sessions/"
soup = BeautifulSoup(requests.get(url).text, "html.parser")
# there's exactly one of these - which contain the sessions
n = soup.body.div(class_='box-content')
# the session staff signed up are the only en-boldened elements
print( len(n[0].find_all('b')) )
