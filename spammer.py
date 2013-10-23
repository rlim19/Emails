#! /usr/bin/env python
# -*- coding: utf-8 -*-

import mailer
import getpass
from optparse import OptionParser

def parse_options():
    parser = OptionParser(usage=
        """
        Spam email Multiple Times
        Usage: %prog [options]
        """)
    parser.add_option('-f', '--from', action='store', type='string',
                      help='the sender', dest='from_')
    parser.add_option('-t', '--to', action='store', type='string',
                      help='the recipient', dest='to_')
    parser.add_option('-s', '--subject', action='store',
                      type='string',
                      default='Hello World')
    parser.add_option('-b', '--body', action='store',
                      type='string',
                      help='multiple line body')
    parser.add_option('-u', '--user', action='store', type='string',
                      help='user for email authentication')
    parser.add_option('-p', '--password', action='store_true',
                      dest='readpass', default=False,
                      help='read password from stdin')
    parser.add_option('-x', '--times', action='store', 
                       type='int')
    (options, args) = parser.parse_args()
    return options



if __name__ == "__main__":
    options = parse_options()
    password = None
    if options.readpass:
        passwd = getpass.getpass('Enter password:')

        message = mailer.Message()
        message.From = options.from_
        message.To = options.to_
        message.Subject = options.subject
        message.Body = options.body

        mailer = mailer.Mailer()
        mailer.host = 'smtp.gmail.com:587'
        mailer._usr = options.user
        mailer._pwd = passwd

        # send emails repeatedly
        count = 0
        limit = options.times
        while count < limit: 
            mailer.send(message)
            count += 1
