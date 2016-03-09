# -*- coding: utf-8 -*-
"""
Created on Wed Mar 02 11:57:04 2016

@author: dkenefick
"""
from Chores import chore

import cPickle as pickle
import csv

from datetime import date
from datetime import timedelta

class taskboard():
    """
    The taskboard keeps track of tasks and chores.  
    you can initialize it by reading in chores, or alteratively you
    can read in a saved version (from outside the file)
    """

    
    def __init__(self, data_path = "", init_from_saved = False):
        """
        Start the task board, initializing empty data lists 
        """
        self.tasks = []
        self.chores = []
        self.switch_chores = []
        
    def __str__(self):
        """ prints the string representation of the task and chore tables """
        return "\nChores:\n"+self.chores+"\nTasks:\n"+self.tasks
    
    def __repr__(self):
        """ Returns str of the object """
        return str(self)
    
    def read_chores_from_file(self,path):
        today = date.today()
        with open(path, 'rb') as csvfile:
            c = csv.DictReader(csvfile, delimiter=',')
            for row in c:
                self.add_chore(chore(start_date =today, owner = row['Person'], name = row['Chore'], time_unit = row['unit'], num = int(row['number of times'])))

    def add_chore(self,ch):
        """ Add a chore to the internal data structure
        if it is a switching chore, estabish an initial owner, and add to the switching list
        """
        # if switching owner, add to switch list and choose an initial owner
        if ch.owner == "Switch":
            ch.owner = ("DK" if "laundry" in ch.name.lower() else "MW")
            self.switch_chores.extend([ch])
        
        self.chores.extend([ch])
    
    def add_task(self,tk):
        """ add task to internal data structure """
        self.tasks.extend([tk])
    
    def remove_expired_tasks(self):
        """ Loop through the tasks and remove all that have a passed deadline 
        """
        today = date(2016,3,10)

        for tk in self.tasks[:]:
            if today > tk.due_date:
                self.tasks.remove(tk)
    
    def update_chore_tasks(self):
        """
        Make a new set of chore tasks, ans switch owners if this is a switching task
        """
        today = date.today()
        for ch in self.chores:
            if today == ch.next_gen_date :
                self.add_task(ch.create_task())
            if ch in self.switch_chores:
                ch.owner == ("MW" if ch.owner == "DK" else "MW")
        
    #http://stackoverflow.com/questions/4529815/saving-an-object-data-persistence-in-python
    def save_taskboard(self,path):
        with open(path, 'wb') as output:
            pickle.dump(self, output, pickle.HIGHEST_PROTOCOL)

    def gen_tasks_by_owner(self):
        result = {}
        for tk in self.tasks:
            if not result.has_key(tk.owner):
                result[tk.owner] = [tk]
            else:
                result[tk.owner].extend([tk])
        
        return result
    
    ### NEED TO FIX SWITCHING CHORES - NOT Showing swiffer
    def gen_chores_by_owner(self):
        result = {}
        for ch in self.chores:
            # if it is a switching task, treat separately
            if ch in self.switch_chores:
                if not result.has_key('Switching'):
                    result['Switching'] = [ch]
                else:
                    result['Switching'].extend([ch])
                    
            #otherwise, add it under its own name
            elif not result.has_key(ch.owner):
                result[ch.owner] = [ch]
            else:
                result[ch.owner].extend([ch])
        
        return result

    def gen_task_email_text(self):
        """
        to update - only task to do this week
        """
        owners = self.gen_tasks_by_owner()
        message = "The tasks for the week of "+str(date.today())+" are: \n\n"
        for person in owners.keys():
            if person == "Both":
                message = message + "Tasks for everyone are:\n"
            else: 
                message = message + "\n\n"+person+"'s tasks are:\n"

            for tk in owners[person]:
                if tk.due_date < (date.today() + timedelta(days=7)):
                    message = message + "("+str(owners[person].index(tk)+1)+") "+tk.name+" ("+str(tk.parent.number_of_times_per_unit)+ " time"+ ("s" if tk.parent.number_of_times_per_unit > 1 else "") + " per "+ tk.parent.time_unit + ")\n"

        return message
        
    def gen_chore_email_text(self):
        message = "Here is your monthly reminder of the chores you're signed up for: \n"
        owners = self.gen_chores_by_owner()

        for person in owners.keys():
            if person == "Both":
                message = message + "Chores for everyone are:\n"
            else: 
                message = message + "\n\n"+person+ ("'s" if person != "Switching" else "") + " Chores are:\n"
                
            for ch in owners[person]:
                message = message + "("+str(owners[person].index(ch)+1)+") "+ch.name+" ("+str(ch.number_of_times_per_unit)+ " time"+ ("s" if ch.number_of_times_per_unit > 1 else "") + " per "+ ch.time_unit + ")\n"

        return message
        
        
        
        
        
        
        
        
        
        
        