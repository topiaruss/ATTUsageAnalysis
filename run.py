#!/usr/bin/env python
# encoding: utf-8
"""
run.py

Created by Russ Ferriday on 2010-05-18.
Copyright (c) 2010 Topia Systems. All rights reserved.
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
