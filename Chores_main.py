# -*- coding: utf-8 -*-
"""
Created on Fri Mar 04 16:37:44 2016
Main method to control a taskboard and other relevant files.  Sends periodic emails

@author: dkenefick
"""
###############
### IMPORTS ###
###############

from Credentials import *
import smtplib

from datetime import datetime
from datetime import timedelta
from datetime import date

from Taskboard import taskboard

########################
### HELPER FUNCTIONS ###
########################

# sends an email
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
        server = smtplib.SMTP(server, 587,10)
        server.ehlo()
        server.starttls()
        server.login(gmail_user, gmail_pwd)
        server.sendmail(FROM, TO, message)
        server.close()
        print 'successfully sent the mail'
    except:
        print "failed to send mail"

#

def main():
    #start a taskboard, and populate it. 
    t = taskboard()
    t.read_chores_from_file(chores_path)
    t.update_chore_tasks()
    
    print('Taskmaster running.  Press Ctrl+{0} to exit'.format('Break' if os.name == 'nt' else 'C'))

    try:
        while True:
            today = date.today()            
            
            #each day, remove expired tasks.
            t.remove_expired_tasks()
            
            #each day, update chore tasks.
            t.update_chore_tasks()
            
            #each week, end email with this week's tasks
            if today.strftime("%A") == 'Sunday':
                send_email(sending_email,app_pwd,to_emails,t.gen_task_email_text())
                
            #each month, send a chore reminer email
            if today.day == 1:
                pass
            
            #check emails for complete tasks        
            
            #wait until the next day            
            now = datetime.today()
            future = now + timedelta(days=1)
            future = datetime(future.year,future.month,future.day, second = 5)
            sleep((future-now).total_seconds())
    
    except (KeyboardInterrupt, SystemExit):
        #save the taskboard
        t.save_taskboard(save_out_path)
        pass
            




