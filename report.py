"""

    Copyright Russell Ferriday 2010 
    russf@topia.com 
    First release May 2010

    This file is part of ATTUsageAnalysis.

    ATTUsageAnalysis is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    ATTUsageAnalysis is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with ATTUsageAnalysis.  If not, see <http://www.gnu.org/licenses/>.

Doctests
--------

Now make a usage object, and pass it to a new Report. Handing in a directory
helps to interpret the traffic report.

    >>> from attusage import AttUsage
    >>> usage = AttUsage()
    >>> usage.process('testreport.csv')
    >>> directory = Directory('testdir.dir')
    >>> report = Report(usage, directory=directory)
    >>> print report
    <Report>
    >>> for line in report.text():
    ...   print line
    Directory:
    508-235-6915 Roger Smith
    508-235-7829 Jane Smith
    <BLANKLINE>
    Summary By User:
    Starting 2010-03-17 10:07:00, Ending 2010-04-03 17:48:00
    <BLANKLINE>
    Name: JANE SMITH, Number: 508-235-7829
    Calls In: 0, Out:10
    Texts In: 7, Out:3
                              :    Calls     |    Texts    |  Text Sessions
                              : From     To  | From    To  |   In   Out
     508-235-6915 Roger Smith :           6  |    4     2  |    4     2
     508-235-7829  Jane Smith :           1  |             |           
     508-534-0399           - :           1  |             |           
     508-704-1151           - :              |    3     1  |    1     1
     508-748-9880           - :           2  |             |           
    --------------------------------------------------------------------------------
    Name: ROGER SMITH, Number: 508-235-6915
    Calls In: 6, Out:4
    Texts In: 4, Out:10
                              :    Calls     |    Texts    |  Text Sessions
                              : From     To  | From    To  |   In   Out
     480-786-7200           - :     1        |             |           
            48368           - :              |    2        |    2      
     508-235-6915 Roger Smith :           1  |             |           
     508-235-7829  Jane Smith :     2        |    1     1  |    1     1
     508-544-3223           - :           1  |             |           
     508-546-3100           - :           1  |             |           
     508-550-6500           - :           1  |             |           
     508-704-0185           - :              |    1     3  |          1
     508-704-1151           - :              |          3  |          3
     508-927-5208           - :     2        |             |           
     949-218-9820           - :     1        |             |           
    Data Transfer           - :              |          3  |          2
    --------------------------------------------------------------------------------

"""
import datetime

EXCHANGE_DURATION = datetime.timedelta(minutes=5)
def fmt(value):
    return value or ''
    
class Directory(dict):
    def __init__(self, filename):
        super(Directory, self).__init__()
        self.filename = filename
        if not filename:
            return
        with open(self.filename) as table:
            for line in iter(table):
                line = line.split()
                if len(line) > 1:
                    number, name = line[0], ' '.join(line[1:])
                    self[number] = name
    def __repr__(self):
        return '<Directory> entries: %s' % len(self)
        
class Report(object):
    def __init__(self,usage, directory=None):
        self.directory = directory or {}
        self.usage=usage
        self.lines = []
    def __repr__(self):
        return '<Report>'
    def p(self,line):
        "Print a line to the print buffer"
        self.lines.append(line)
    def put_directory(self):
        "Puts the directory into the print buffer"
        self.p('Directory:')
        for number, id in sorted(self.directory.items(), key=lambda i: i[0]):
            self.p('%12s %s' % (number, id))
    def do_summary(self):
        "Puts a summary to print buffer"
        self.p('Summary By User:')
        self.put_timespan()
        self.p('')
        for user in self.usage.users.values():
            incalls, outcalls, intexts, outtexts = 0,0,0,0
            parties = {}
            self.p('Name: %s, Number: %s' % (user.name, user.number))
            for call in user.calls:
                party = parties.setdefault(call.number, \
                        {'fromcalls':0, 'tocalls':0, \
                         'fromtexts':0, 'totexts':0,\
                          'lastexchangestarted':datetime.datetime(2000,1,1),
                          'textexchangesrc': 0,
                          'textexchangedst': 0
                          })
                if call.is_incoming():
                    incalls+=1
                    party['fromcalls'] += 1
                else:
                    outcalls+=1
                    party['tocalls'] += 1
            for text in user.texts:
                party = parties.setdefault(text.number, \
                        {'fromcalls':0, 'tocalls':0, \
                         'fromtexts':0, 'totexts':0,\
                         'lastexchangestarted':datetime.datetime(2000,1,1),
                         'textexchangesrc': 0,
                         'textexchangedst': 0
                         })
                if text.is_incoming():
                    intexts+=1
                    party['fromtexts'] += 1
                else:
                    outtexts+=1
                    party['totexts'] += 1
                if text.time > party['lastexchangestarted'] + EXCHANGE_DURATION:
                    party['lastexchangestarted'] = text.time
                    if text.incoming :
                        party['textexchangesrc'] += 1
                    else:
                        party['textexchangedst'] += 1                    
                                
            self.p('Calls In: %s, Out:%s' % (incalls, outcalls))
            self.p('Texts In: %s, Out:%s' % (intexts, outtexts))
            self.p('                          :    Calls     |'\
                                              '    Texts    |'\
                                              '  Text Sessions')
            self.p('                          : From     To  |'\
                                              ' From    To  |'\
                                              '   In   Out')
            for number, party in sorted(parties.items(), key=lambda i: i[0]):
                id = self.directory.get(number, '-')
                self.p('%13s %11s :  %4s  %4s  |'\
                       ' %4s  %4s  |'\
                       ' %4s  %4s' % \
                       (number, id, \
                        fmt(party['fromcalls']), fmt(party['tocalls']),\
                        fmt(party['fromtexts']), fmt(party['totexts']),\
                        fmt(party['textexchangesrc']), fmt(party['textexchangedst'])\
                        ))
            self.p('-' * 80)            
    def put_timespan(self):
        "Finds earliest and latest calls in the report, puts to print buffer"
        earliest = datetime.datetime.now()
        latest = datetime.datetime(2000,1,1)
        for user in self.usage.users.values():
            for call in user.calls:
                if call.time < earliest:
                    earliest = call.time
                elif call.time > latest:
                    latest = call.time
            for text in user.texts:
                if text.time < earliest:
                    earliest = text.time
                elif text.time > latest:
                    latest = text.time
        self.p('Starting %s, Ending %s' % (earliest, latest))    
    def text(self):
        "generate a text report and return as a sequence of lines"
        self.put_directory();
        self.p('')
        self.do_summary()
        return self.lines


if __name__ == "__main__":
    import doctest
    doctest.testmod()
