#! /usr/bin/env python
# -*- coding: utf-8 -*-

import smtplib  
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from optparse import OptionParser
import getpass
import sys

#####################################################
# Using gmail (default isp) to send mails           #
# recipients are sourced from [*.csv]               #
# Note CSV the first line assumed to be its header  #
# emails are in the third column or in python [2]   #
#####################################################

def sendMails(isp, user, passwd, subject, input_f, body):

    # login
    server = smtplib.SMTP(isp)
    #server.set_debuglevel(1)
    server.starttls() 
    server.login(user, passwd)

    # build the structure of an email
    msg = MIMEText(body)
    msg['From'] = user
    msg['Subject'] = subject

    # send this email to each contact line (csv)
    with open(input_f) as in_f:
        next(in_f)
        for line in in_f:
            # get the email address (3rd column)
            recipient = line.rstrip().split(',')[2]
            server.sendmail(msg.get('From'), recipient, msg.as_string())
        server.quit()

def parse_options():
    parser = OptionParser(usage="""\
         Send email to each contact(per line) in csv
         Usage: %prog [options] 
         e.g:

         """)
    parser.add_option('-u', '--user', action='store', type='string', 
                      help='user for email authentication')                     
    parser.add_option('-P', '--password', action='store_true', dest='readpass', 
                      default=False, 
                     help='read password (for password auth) from stdin')
    parser.add_option('-s', '--subject', 
                      type = 'string', action = 'store',
                      default = 'Hello World',
                      help = 'Subject of your email')
    parser.add_option("-f", "--file",
                      action="store", type="string", dest="filename")
    parser.add_option('-b', '--body', 
                      type = 'string', action = 'store',
                      help = 'Multiple line body! use """[you email] """')
    (options, args) = parser.parse_args()
    return options

def main():
    options = parse_options()
    password = None
    if options.readpass:
        passwd = getpass.getpass('Enter password: ')
        isp = 'smtp.gmail.com:587'
        try:
            sendMails(isp = isp, user = options.user,
                      passwd = passwd, subject = options.subject,
                      input_f = options.filename, body = options.body)
        except Exception, e:
            print e
            sys.exit(1)
        except KeyboardInterrupt:
            sys.exit(0)


if __name__ == '__main__':
    main()    
    
