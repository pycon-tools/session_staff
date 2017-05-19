#!/usr/bin/env python

'''
usage:
    session_staff [<url>]
    session_staff --report [<kind>] [<url>]
    session_staff --version
    session_staff --debug

options:
    -h, --help      usage, options, and notes.
    -r, --report    generate report of <kind> [default: names]
                    Report types are
                        names:   #number of slots signed up for: staff name
                        vacant:  vacant session: task
                        staff:   staff name: list of session: tasks
                        all:     vacant & staff reports
    -v, --version   show version
    -d, --debug     show options, and exit

notes:
    Requires python 3.6 or later (we like f-strings).
    Default <url> is https://us.pycon.org/<current-year>/schedule/sessions/
    This version is PyCon-2017 specific.  An improvement would automate the configuration
    for extracting elements (probably will need to be trained).
    For now, to update for future PyCon's, the selection patterns need to be updated
    manually, although not very much year to year (seems to depend on html theme used).
'''

from bs4 import BeautifulSoup
import requests
import sys
import time
from docopt import docopt
from collections import defaultdict


class Session(object):
    # class variables:
    ## This gives count of volunteers,
    # and back reference to their assignments
    names = defaultdict(list)  # list of staff: Session instance
    chairs = runners = 0
    errors = 0
    @classmethod
    def add_name(cls, name, self):
        cls.names[name].append(self)

    @classmethod
    def inc_chairs(cls):
        cls.chairs += 1

    @classmethod
    def inc_runners(cls):
        cls.runners += 1

    @classmethod
    def inc_errors(cls):
        cls.errors += 1

    def __init__(self, s):
        ''' pass s - a single session entry from sessions '''
        #-----#
        # get session name
        c = s.parent
        self.session = c.contents[1].text
        #-----#
        # get staff names for staff slots
        chair = runner = None
        jobs = s.select('ul li')
        # at most two entries:
        for e in jobs:
            if len(e) < 3: # "No Volunteers"
                continue
            staff_name = e.contents[-1].lstrip(': ').rstrip()
            # collects list of volunteering gigs per person:
            self.add_name(staff_name, self)
            # either 'Session Chair' or 'Session Runner'
            # - no other choices at this point;
            # len('Session ') == 8
            if e.contents[1].text[8:] == 'Chair':
                chair = staff_name
                self.inc_chairs()
            else:
                runner = staff_name
                self.inc_runners()
        if chair == runner:
            self.error = 1
            self.inc_errors()
            print(f'error {self.session}: {chair} is, but cannot be chair and runner in same session!', file=sys.stderr)
        self.chair = chair
        self.runner = runner
        #-----#
        # get slots info for report details,
        #  i.e. room, time, talks
        # FIXME: too much magic; figure out
        #   easier to read select() way to get to this
        slots = c.contents[3].contents[-2].text.strip().replace('\n\n', '\n')
        self.slots = slots.replace('\n\n', '\n').split('\n')

    # FIXME:don't print from the instance; return a string; maybe
    #       opt in a formatter?
    def show_slots(self, name):
        # slot generator:
        ##
        # this seems too long; just show them
        # the starting date/time/room, i.e. the first string:
        '''
        slots = self.slots
        gsl = (i for i in slots)  # gsl: generator of slots
        # slot text is pair of time & room-info, with talk title & author:
        for _ in range(len(slots)//2):
            print(f'{next(gsl)}:\n\t{next(gsl)}')
        '''
        role = 'Chair ' if self.chair==name else 'Runner'
        print(f'  {self.session}, {role} starting with:  {self.slots[0]}')

    def show_unstaffed(self):
        if self.chair is None:
            print(f'{self.session}: Session Chair:  {self.slots[0]}')
        if self.runner is None:
            print(f'{self.session}: Session Runner: {self.slots[0]}')


# FIXME: be smarter abotu the selection stuff throughout here;
#        maybe use read in a configuration, and write a setup to generate it;
#        anyway, something better than this step from a quick-hack...
def url_select(url, sel='.well'):
    ''' given a url and s selector, return results
    '''
    soup = BeautifulSoup(requests.get(url).text, "html.parser")
    # there's exactly one of box-content - which contain the sessions
    # - this was 2016: entries = soup.body.div.select(".box-content ul li ul li")
    # - in 2017, the session staff are in a well div
    # each of the sessions:
    return soup.body.select(sel)


def report_staff(names):
    print('--- Staff Assignments ---')
    for name in names:
        print(f'\n{name} ({len(Session.names[name])}):')
        # get the collected sessions per name
        for session in Session.names[name]:
            session.show_slots(name)


def report_unfilled(sessions):
    print(f'--- Unfilled Session Staff Slots '
          f'({len(sessions)*2-(Session.chairs+Session.runners)}) ---')
    for session in sessions:
        session.show_unstaffed()


if __name__ == '__main__':
    if sys.version_info.major < 3 or sys.version_info.minor < 6:
        print("Python v3.6 or later required")
        sys.exit(-1)

    # docopts
    opt = docopt(__doc__, version='Version: PyCon-2017')
    if opt['--debug']:
        print(opt)
        sys.exit()

    if opt['--report']:
        report = opt['<kind>'] or 'names'
    else:
        report = None

    # session staff is interesting close to conference, so
    #  no need to parameterize this:
    url = opt['<url>'] or "https://us.pycon.org/" + time.strftime('%Y') + "/schedule/sessions/"
    site_sessions = url_select(url)
    # each volunteer slot w/in a session;
    # Sessions class instance now accumulates
    # - unique list of names, with their session instances
    # - count of chairs
    # - count of runners
    sessions = []
    for s in site_sessions:
        sessions.append(Session(s))

    # uniq names:
    names = list(Session.names)  # grab keys from defaultdict into list
    # print names
    if report:
        names.sort()
        if report.startswith('n'):
            # print count: name
            for i in names:
                print(f"{len(Session.names[i])}: {i}")
        elif report.startswith('v'):  # vacancies
            # cycle through staff spots set to 'None'
            report_unfilled(sessions)
            pass
        elif report.startswith('s'):  # staff assignments
            # print by staff /blank line after each for "cutting"
            report_staff(names)
            pass
        elif report.startswith('a'):  # all option (vacant+staff)
            report_unfilled(sessions)
            print('')
            report_staff(names)
            pass
    else:  # print count
        print( f"Sessions:   {len(sessions)}")
        print( f"Volunteers: {Session.chairs+Session.runners} slots, {len(names)} volunteers" )
        print( f"   Chairs:  {Session.chairs}  ")
        print( f"   Runners: {Session.runners}  ")
        print( f"=> Short:  ({len(sessions)*2 - (Session.chairs+Session.runners)})" )
        print( f"=> errors:  {Session.errors}  ")
        if Session.errors > 0:
            for session in sessions:
                if session.error:
                    print(f' >> error {session.session}: Chair: {session.chair}; Runner: {session.runner}')

