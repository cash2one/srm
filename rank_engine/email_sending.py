#!/usr/bin/python
# -*- coding: utf-8 -*-

import smtplib
import datetime

# see mailing samples by link:
# http://stackoverflow.com/questions/10147455/trying-to-send-email-gmail-as-mail-provider-using-python
# see mailing samples with attachments by link:
# http://www.jayrambhia.com/blog/send-emails-using-python/


def send_ranking_report(report_date_time):
    gmail_user = "sergey.a.polyakov@gmail.com"
    gmail_pwd = "psA29November62"
    FROM = 'Page Ranker'
    TO = ['freelancer.sergey@gmail.com'] #must be a list
    SUBJECT = "report"
    TEXT = "Page ranks has been updated on %s" % report_date_time

    # Prepare actual message
    message = """\From: %s\nTo: %s\nSubject: %s\n\n%s
    """ % (FROM, ", ".join(TO), SUBJECT, TEXT)
    try:
        server = smtplib.SMTP("smtp.gmail.com", 587) #or port 465 doesn't seem to work!
        server.ehlo()
        server.starttls()
        server.login(gmail_user, gmail_pwd)
        server.sendmail(FROM, TO, message)
        server.close()
        print 'successfully sent the mail'
    except Exception:
        print "failed to send mail"


if __name__ == '__main__':
    cur_dt = datetime.datetime.now()
    send_ranking_report(cur_dt)
