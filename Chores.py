# -*- coding: utf-8 -*-
"""
Created on Mon Feb 29 18:01:24 2016
Structures for the chores, task management.  
@author: dkenefick
"""
#################
### LIBRARIES ###
#################
from datetime import datetime
from datetime import timedelta
from datetime import date
from Credentials import trade_out_path
import calendar
import os

###################
### GLOBAL VARS ###
###################





class chore():
    """ 
    A chore is a repeating task.  Creating one requires:
        - Name (string):  the title of the chore
        - Owner (string):  Who currently owns the task
        - time_unit (datetime):  'week', 'year', 'month', or 'occasionally'.  The frequency with which the chore is done.
        - number_of_times_per_unit (int):  how many times per the above unit the chore should be completed
        - start_date - a date object representing the starting date
        - last_gen_date - a date object representing the last time  task was generated
        
        Whenever you create a task, you update the last_gen_date variable, and also set the next_gen_date
    """
    ### 'Static' Vars
    # an assumption for the frequency of  occasionaly taks
    occasionaly_assumption = ("year",4)

    def __init__(self, **kwargs):
        #pull the relevant details from the iniialization
        #maybe keep these in a dict?
        self.name = kwargs.get("name","")
        self.owner = kwargs.get("owner","")
            
        self.time_unit = kwargs.get("time_unit","").lower()
        self.number_of_times_per_unit = kwargs.get("num",1)
            
        self.start_date = kwargs.get("start_date",None)    
        self.next_gen_date = self.start_date
        self.last_gen_date = None        
        
        # if the unit is occasionaly, implement our assumtion
        if self.time_unit == "occasionaly":
            self.time_unit, self.number_of_times_per_unit = self.occasionaly_assumption
        
    def __str__(self):
        """
        Generates a laundry list of items about the chore.  
        """        
        if self.time_unit.lower() != "occasionaly":
            string = "\nChore \nName:  "+self.name+"\nStart Date:  "+str(self.start_date)+"\nUnit:  "+self.time_unit+"\nNumber of Times per "+self.time_unit+":  "+ str(self.number_of_times_per_unit)+"\nOwner:  "+self.owner+"\nNext Task Generation:  "+str(self.next_gen_date)
        else:
            string = "\nChore \nName:  "+self.name+"\nStart Date:  "+str(self.start_date)+"\nUnit:  "+self.time_unit+"\nOwner:  "+self.owner  +"\nNext Task Generation:  "+str(self.next_gen_date )
 
        return string
           
    def __repr__(self):
        """
        returns the __str__ method
        """
        return str(self)
    
    def __eq__(self,other):
        return str(self) ==str(other)
    
    def create_task(self):
        """
        Generate a new task, based on this chore's charateristics.
        The due date of the resulting task is the day before the next gen date.
        This function will also update the next_gen_date and last_gen_date variables        
        """
        # get and set the next gen date
        self.next_gen_date = self.get_next_gen_date()
        #next due date is next gen date - 1
        next_due_date = self.next_gen_date - timedelta(1)
        #generate the task
        tk =  task(name=self.name, due_date = next_due_date, owner=self.owner, parent = self)
        
        #now that task is generated, update last gen date
        self.last_gen_date = date.today()        
        
        # return the task
        return tk

    def get_next_gen_date(self):
        """
        Generate the next gen date based on the last_gen_date or the start_date, depending.  
        finds the next time a task should be generated based on the time unit and the number of 
        times per unit.  Right now it only handles a few arbitrary cases, based on initial task assignments.
        """
        #get the starting point
        if self.last_gen_date is None:
            start = self.start_date
        else:
            start = self.last_gen_date
        
        # Processing depends on the time unit
        #daily is easy - incremeent the day
        if self.time_unit == 'day':
            new = start + timedelta(days = 1)

        # weekly.  if weekly, add 7 days If 2 times per week, alternate 3 and 4 days
        elif self.time_unit == 'week':
            if self.number_of_times_per_unit == 1:
                new = start + timedelta(days = 7)
                
            elif self.number_of_times_per_unit == 2:
                diff = (start - self.start_date).days % 7
                if (diff == 0) | (diff == 3): 
                    new = start + timedelta(days = 4)
                else: 
                    new = start + timedelta(days = 3)
            else:
                raise ValueError("Invalid recurrance of chore: "+self.number_of_times_per_unit+" time(s) per "+self.time_unit)
        
        # monthly:  if monthly, add a month.  If semimonthly, add 2 weeks
        elif self.time_unit == 'month':
            if self.number_of_times_per_unit == 1:
                new = self.add_months(start,1)
            else:
                #twice per month is really every two weeks
                new = start + timedelta(weeks = 2)
            
        # year, half, or quarter.  add a year, 6 months, or 3 months respectively. 
        elif self.time_unit == 'year':
            if self.number_of_times_per_unit == 1:
                new = date(start.year+1,start.month,start.day)
            elif self.number_of_times_per_unit == 2:
                new = self.add_months(start,6)
            elif self.number_of_times_per_unit == 4:
                new = self.add_months(start,3)
            else:
                raise ValueError("Invalid recurrance of chore: "+self.number_of_times_per_unit+" time(s) per "+self.time_unit)

        else:
            raise ValueError("Invalid recurrance of chore: "+self.number_of_times_per_unit+" time(s) per "+self.time_unit)

        return new
        

    def add_months(self,sourcedate,months):
        """ Helper function to add months to a date object while incrementing the year """
        month = sourcedate.month - 1 + months
        year = int(sourcedate.year + month / 12 )
        month = month % 12 + 1
        day = min(sourcedate.day,calendar.monthrange(year,month)[1])
        return date(year,month,day)        

    def trade(self, additional, traded, extra1="",extra2=""):
       """
       switches the owner of 0 or more chores and tasks.
       Also records the terms of trade (including extra)
       """
       if additional is not None:
           if type(additional) is not list: additional = [ additional ]
           additional.append(self)
           
       else:
           additional = self
       
       trade_tasks(additional,traded,extra1,extra2)

class task():
    """
    This class is an instance of something to be done.  It can be generated by a chore
    or as a one-off.  Has similar attributes to a chore, but also a status and a due date
    """
    def __init__(self, name = "", due_date = None, owner = "",parent = None):
        self.name=name
        self.due_date=due_date
        self.owner = owner
        self.status = "in progress"
        self.chore = chore
        self.parent = parent
    
    def __str__(self):
        return "\nTask\nName:  "+self.name+"\nDue date:  "+str(self.due_date) +"\nOwner:  "+self.owner+"\nStatus:  "+self.status
        
    def __repr__(self):
        return str(self)
        
    def finish(self):
        self.status = "done"


#might incorporate this into a 'task board' class
def trade_tasks(obj0,obj1,extra0="",extra1=""):
    """
    Switches the owner of 0 or more chores and tasks.
    each input is a list, but handles single objects
    Also records the terms of trade (including extra)
    """    
    
    # make input a lits
    if type(obj1) is not list: obj1 = [ obj1 ]
    if type(obj0) is not list: obj0 = [ obj0 ]

    # get owner for each object list
    owner0 = obj0[0].owner
    owner1 = obj1[0].owner
    
    if owner1 == owner0: raise ValueError("Task Collections must have different owners")    
    
    #ensure all owners are the same
    if len(obj0) >1:
        for i in range(1,len(obj0)):
            if obj0[i].owner != owner0:
                raise ValueError("Invalid trade.  All of the elements of obj0 must have the same owner.")
                
    if len(obj1) >1:            
        for i in range(1,len(obj1)):
            if obj1[i].owner != owner1:
                raise ValueError("Invalid trade.  All of the elements of obj1 must have the same owner.")
    
    list0 = ""
    list1 = ""
    #now, switch the relevant items and construct the print string
    for obj in obj0:
        obj.owner=owner1
        if type(obj) is task: 
            tp = "(task)"
        else:
            tp = "(chore)"
        list0 = list0+ obj.name+" "+tp+", "
        
    for obj in obj1:
        obj.owner = owner0
        if type(obj) is task: 
            tp = "(task)"
        else:
            tp = "(chore)"
        list1 = list1+ obj.name+" "+tp+", "
        
        #remove trailing commas
        list1 = list1[0:-2]
        list0 = list0[0:-2]
        
    #record the trade, including the current time and date.
    with open(trade_out_path,'a') as f:
        #construct the output string                
        f.write("Date: "+str(datetime.now().date())+"\nParty1:  "+owner0+
                                                    "\nParty2:  "+owner1+
                                                    "\nTraded1:  "+list0+
                                                    "\nTraded2:  "+list1+
                                                    "\nExtra1:  "+extra0+
                                                    "\nExtra2:  "+extra1+"\n\n")
    
    
    
    
    
    
    
    
    
    
    
    
    