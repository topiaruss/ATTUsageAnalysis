"""

    Copyright Russell Ferriday 2010 
    russf@topia.com 
    First release May 2010

    This file is part of ATTBillAnalysis.

    ATTBillAnalysis is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    ATTBillAnalysis is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with ATTBillAnalysis.  If not, see <http://www.gnu.org/licenses/>.
      
  This package reads ATT CSV formatted bills into a neat structure

DocTests
--------
  
Check the date parser...
  
  >>> print maketime('03/17/2010','10:07PM')
  2010-03-17 22:07:00
  
Create a bill and read a csv report into it...
  
  >>> bill = Attbill()
  >>> bill.process('testreport.csv')
  >>> print bill
  {'ROGER SMITH': <User> 'ROGER SMITH' at '508-235-7829', 'JANE SMITH': <User> 'JANE SMITH' at '508-235-6915'}

Show that we have two users on the account...
  
  >>> for user in bill.users.values():
  ...   print user
  <User> 'ROGER SMITH' at '508-235-7829'
  <User> 'JANE SMITH' at '508-235-6915'
  
Look at the calls for the first user...
  
  >>> for call in bill.users.values()[0].calls:
  ...   print call
  <Call> 2010-03-18 08:45:00 to   508-235-7829 == VMAIL CL lasting 1 min
  <Call> 2010-03-18 08:46:00 to   508-748-9880 == SAN LUS O CA lasting 2 min
  <Call> 2010-03-18 12:27:00 to   508-235-6915 == SAN LUS O CA lasting 1 min
  <Call> 2010-03-18 12:28:00 to   508-235-6915 == SAN LUS O CA lasting 1 min
  <Call> 2010-03-18 16:20:00 to   508-748-9880 == SAN LUS O CA lasting 2 min
  <Call> 2010-03-18 16:43:00 to   508-534-0399 == SAN LUS O CA lasting 2 min
  <Call> 2010-03-18 21:14:00 to   508-235-6915 == SAN LUS O CA lasting 1 min
  <Call> 2010-03-18 21:17:00 to   508-235-6915 == SAN LUS O CA lasting 1 min
  <Call> 2010-03-18 21:19:00 to   508-235-6915 == SAN LUS O CA lasting 1 min
  <Call> 2010-03-18 21:25:00 to   508-235-6915 == SAN LUS O CA lasting 1 min
  
And now the texts...
  
  >>> for text in bill.users.values()[0].texts:
  ...   print text
  <Text> 2010-03-17 13:01:00 from 508-235-6915
  <Text> 2010-03-18 12:04:00 to   508-235-6915
  <Text> 2010-03-18 18:33:00 from 508-704-1151
  <Text> 2010-03-18 19:25:00 from 508-235-6915
  <Text> 2010-03-18 20:13:00 from 508-235-6915
  <Text> 2010-03-18 20:22:00 to   508-235-6915
  <Text> 2010-03-18 20:28:00 from 508-235-6915
  <Text> 2010-03-19 21:54:00 to   508-704-1151
  <Text> 2010-03-19 21:59:00 from 508-704-1151
  <Text> 2010-03-19 21:59:00 from 508-704-1151
  
Look at report.py to see more usage.
  
  """
import csv
import datetime
class User(object):
    def __init__(self, name='', number=''):
      self.name = name
      self.number = number
      self.calls = []
      self.texts = []
      
    def __repr__(self):
        return "<User> '%s' at '%s'" % (self.name, self.number)
      
class Call(object):
    def __init__(self, time, incoming, number, place, minutes):
        self.time = time
        self.incoming = incoming
        self.number = number
        self.place = place
        self.minutes = minutes
    def __repr__(self):
        return '<Call> %s %s %s == %s lasting %s min' % \
           (self.time, self.incoming and 'from' or 'to  ', \
           self.number, self.place, self.minutes)
    def is_incoming(self):
        return self.incoming
        
class Text(object):
    def __init__(self, time, incoming, number):
        self.time = time
        self.incoming = incoming
        self.number = number
    def __repr__(self):
        return '<Text> %s %s %s' % \
           (self.time, self.incoming and 'from' or 'to  ', \
           self.number)
    def is_incoming(self):
        return self.incoming

class Attbill(object):
    
    def __init__(self):
        self.users = {}
        self.current_user = None # current user object
        self.current_number = ''
        self.current_mode = '' # 'call' / 'data'
        
    def process(self, fqpath):
        self.fqpath = fqpath
        reader = csv.reader(open(self.fqpath, "rb"))
        for line in reader:            
            self._processline(line)
        for name, user in self.users.items():
            user.calls.sort(key=lambda call: call.time)
            user.texts.sort(key=lambda text: text.time)
                
    def _is_empty(self, line):
        return [ i for i in line if i ] == []
        
    def _is_int(self, s):
        try: 
            i = int(s)
            return True
        except:
            return False
            
    def _convert_data(self, line):
        time = maketime(line[2], line[3])
        text = Text(time, line[10]=='In', line[4])
        self.current_user.texts.append(text)
        
    def _convert_call(self, line):
        time = maketime(line[2], line[3])
        call = Call(time, line[5].startswith('INCOMING'), line[4], \
                    line[5], line[6])
        self.current_user.calls.append(call)
        
    def _processline(self, line):
        #all empty fields? - forget it
        if self._is_empty(line):
            return
        
        #what type of block?
        if line[0] == 'Call Detail':
            self.current_number = line[1]
            self.current_mode = 'call'
            return
        if line[0] == 'Data Detail':
            self.current_number = line[1]
            self.current_mode = 'data'
            return
        
        #update current user
        if line[0] == 'User Name:':
            username = line[1]
            self.current_user = self.users.setdefault(username, \
                                User(username, self.current_number) )
            return
        
        #see if we have a call or data record and process it
        if self._is_int(line[0]):
            if self.current_mode == 'data':
                self._convert_data(line)
            else:
                self._convert_call(line)
                
        return
            
    def __repr__(self):
        return str(self.users)
        
def maketime(d,t):
    dt = ' '.join((d,t))
    dt = datetime.datetime.strptime(dt, "%m/%d/%Y %I:%M%p" )
    return dt
    
if __name__ == "__main__":
    import doctest
    doctest.testmod()
  
