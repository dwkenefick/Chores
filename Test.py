# -*- coding: utf-8 -*-
"""
Created on Tue Mar 01 10:12:14 2016

@author: dkenefick
"""
import time 
from Credentials import *

from datetime import datetime
from datetime import timedelta
from datetime import date

from Taskboard import taskboard
from apscheduler.schedulers.background import BackgroundScheduler

"""
t1 = task(name = "Clean the Bed", due_date = date(2016,3,7) , owner = "DK")
t2 = task(name = "Clean the Kitchen", due_date = date(2016,3,7) , owner = "MW")

c1 = chore(name = "Getting mail",owner="DK",time_unit="Week",num=2,start_date = date(2016,3,1))
c2 = chore(name = "Wipe bathroom counter ",owner="MW",time_unit="Week",num=1,start_date = date(2016,3,1))

c1.trade(additional = None,traded=c2,extra1="",extra2="")

c1.trade(additional = t2,traded=c2,extra1="",extra2="")

# test biweekly
t3 = c1.create_task()
c1.last_gen_date = c1.next_gen_date
t4 = c1.create_task()
c1.last_gen_date = c1.next_gen_date
t5 = c1.create_task()
c1.last_gen_date = c1.next_gen_date
t6 = c1.create_task()
c1.last_gen_date = c1.next_gen_date
t7 = c1.create_task()
c1.last_gen_date = c1.next_gen_date
t8 = c1.create_task()

#test weekly
t3 = c2.create_task()
c2.last_gen_date = c2.next_gen_date
print(str(c2.next_gen_date))

t4 = c2.create_task()
c2.last_gen_date = c2.next_gen_date
print(str(c2.next_gen_date))

t5 = c2.create_task()
c2.last_gen_date = c2.next_gen_date
print(str(c2.next_gen_date))

"""

    #may move this to 'main' method
def send_email(user, pwd, recipient, subject, body):

    gmail_user = user
    gmail_pwd = pwd
    FROM = user
    TO = recipient if type(recipient) is list else [recipient]
    SUBJECT = subject
    TEXT = body

    # Prepare actual message
    message = """\From: %s\nTo: %s\nSubject: %s\n\n%s
    """ % (FROM, ", ".join(TO), SUBJECT, TEXT)
    try:
        server = smtplib.SMTP("smtp.gmail.com", 587,10)
        server.ehlo()
        server.starttls()
        server.login(gmail_user, gmail_pwd)
        server.sendmail(FROM, TO, message)
        server.close()
        print 'successfully sent the mail'
    except:
        print "failed to send mail"



t = taskboard()
t.read_chores_from_file(chores_path)
t.update_chore_tasks()
a = t.gen_chore_email_text()
b = t.gen_task_email_text()
#d = t.gen_tasks_by_owner()

#send_mail(sending_email,app_pwd,to_emails,t.gen_task_email_text())

"""
t.save_taskboard(save_out_path)
t.remove_expired_tasks()
with open(save_out_path, 'rb') as inp:
    p = pickle.load(inp)
"""
"""
text = "A banana"
def simple():
    print( text )
    
scheduler = BackgroundScheduler()
job = scheduler.add_job(simple, 'interval', seconds=1)
print(job)
scheduler.start()
time.sleep(2)
text = "two bananas"
time.sleep(2)
scheduler.shutdown()
"""