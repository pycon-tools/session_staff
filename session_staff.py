#!/usr/bin/env python
#  count sessions staff signed up
#  -n to emit names

import sys

import requests
from lxml import html

if __name__ == '__main__':

    print_table = '-n' not in sys.argv

    url = "https://us.pycon.org/2017/schedule/sessions/"

    headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'}
    page = requests.get(url, headers=headers)
    tree = html.fromstring(page.content)


    sessions = []
    session_divs = tree.xpath('//div[@class="box-content"]/ul/li')

    if print_table:
        print('{:12s} {:50s} {:36s} {:36s}'.format('Session#', 'Session URL', 'Chair', 'Runner'))

    for session_div in session_divs:
        session_a = session_div.xpath('a')[0]
        session_number = session_a.text
        session_url = 'https://us.pycon.org' + session_a.attrib['href']

        chair = ''
        runner = ''
        for x in session_div.xpath('div/ul/li'):
            try:
                volunteer = ''.join([text.strip() for text in x.xpath('text()')])
                if volunteer.startswith(': '):
                    volunteer = volunteer[2:]
                role = x.xpath('b/text()')[0]
                if 'Chair' in role:
                    chair = volunteer
                elif 'Runner' in role:
                    runner = volunteer
            except IndexError:
                # No volunteers signed up
                pass

        sessions.append((session_number, session_url, chair, runner,))

        if print_table:
            print('{:12s} {:50s} {:36s} {:36s}'.format(session_number, session_url, chair, runner))

    num_sessions = len(sessions)
    sessions_w_chair = len([1 for _, _, chair, _ in sessions if chair != ''])
    sessions_w_runner = len([1 for _, _, _, runner in sessions if runner != ''])

    we_have = sessions_w_chair + sessions_w_runner

    if print_table:
        print()

    print('have = {}, need = {}'.format(we_have, len(sessions)*2 - we_have))
    print
    print('Sessions without chair: ' + str(num_sessions - sessions_w_chair))
    print('Sessions without runner: ' + str(num_sessions - sessions_w_runner))
    print

    print('Total number of sessions: ' + str(num_sessions))
