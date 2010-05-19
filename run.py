#!/usr/bin/env python
# encoding: utf-8
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
"""

import sys
import getopt


help_message = '''
The help message goes here.
'''


class Usage(Exception):
    def __init__(self, msg):
        self.msg = msg


def main(argv=None):
    directory = ''
    if argv is None:
        argv = sys.argv
    try:
        try:
            opts, args = getopt.getopt(argv[1:], "hd:v", ["help", "directory="])
        except getopt.error, msg:
            raise Usage(msg)
        
        # option processing
        for option, value in opts:
            if option == "-v":
                verbose = True
            if option in ("-h", "--help"):
                raise Usage(help_message)
            if option in ("-d", "--directory"):
                directory = value
    
        from attbill import Attbill
        from report import Report, Directory
        bill = Attbill()
        for filename in args:   
            bill.process(filename)
        directory = Directory(directory)
        report = Report(bill, directory=directory)
        for line in report.text():
          print line
    
    except Usage, err:
        print >> sys.stderr, sys.argv[0].split("/")[-1] + ": " + str(err.msg)
        print >> sys.stderr, "\t for help use --help"
        return 2


if __name__ == "__main__":
    sys.exit(main())
