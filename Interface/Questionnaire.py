#!/usr/bin/env python
# encoding: utf-8
# Created by Craig Harris & Ryan Day - 11/03/2014

from Tkinter import *
import Tkinter as TK
from ttk import *
from Application.Chart import *

import tkMessageBox
import random, sys, re
import math
import threading, Queue, time

class Questionnaire():

    def __init__(self, appdelegate):
        
        self.appdelegate = appdelegate
        self.results = {'BSc Computer Science with High Performance Computing':0, 'BSc Computer Science with Security and Forensic':0, 'BSc Software Engineerin':0, 'BSc Business Information System':0, 'BSc Computer Scienc':0, 'BSc Joint Honours Computing & Mathematic':0, 'BSc Business Information System':0, 'BSc Computer Science with Visual Computing':0}

    """
    "" @name: Insert Questionnaire Table
    "" @author: Craig Harris 
    "" @description: A method to insert a new questionnaire into the database. This method should be called from a thread.
    "" @prams: None
    "" @return: Void
    """

    def insert_questionnaire_table(self):
        # Fetch any exisitng questionnaire for user, using user_id.
        existing_questionnaire = self.appdelegate.db.select('questionnaire', where="(`user_id` == '%s')" % str(self.appdelegate.user_id), limit=1)
        
        # If query did return results.
        if len(existing_questionnaire) and len(existing_questionnaire[0]):
            # Delete the questionnaire and questionnaire questions from the database.
            self.appdelegate.db.delete('questionnaire', where="(`questionnaire_id` == '%s')" % existing_questionnaire[0]['questionnaire_id'], limit=1)
            self.appdelegate.db.delete('questionnaire_question', where="(`questionnaire_id` == '%s')" % existing_questionnaire[0]['questionnaire_id'])
        
        # Insert new questionnaire including the started timestamp and user_id.
        self.questionnaire_id = self.appdelegate.db.insert('questionnaire', query_data = {
            'started_timestamp':str(time.time()),
            'user_id':str(self.appdelegate.user_id)
                })

    """
    "" @name: Draw
    "" @author: Craig Harris
    "" @description: A method to draw questionnaire page.
    "" @prams: None
    "" @return: Void
    """
    
    def draw(self):
        #Clean GUI
        self.appdelegate.flush_ui()
        self.appdelegate.pack(fill = BOTH, expand=1)
        self.appdelegate.rowconfigure(0, weight=1)
        self.appdelegate.grid_columnconfigure(1, weight=1)
        # Initialise new thread to draw questionnaire.
        self.insert_questionnaire_thread = threading.Thread(target = self.insert_questionnaire_table)
        self.insert_questionnaire_thread.start()

        # Setup questionnaire to display on page
        for i in range(13):
            self.appdelegate.rowconfigure(i, pad=20)

        self.appdelegate.rowconfigure(3, pad=30)
        self.appdelegate.rowconfigure(4, pad=0)
        self.appdelegate.rowconfigure(17, pad=100)
        self.appdelegate.option_add("*background", "#ECF0F1")
        self.results = {'BSc Computer Science':0,'BSc Computer Science with High Performance Computing':0,'BSc Computer Science with Security and Forensics':0,'BSc Software Engineering':0,'BSc Business Information Systems':0,'BSc Joint Honours Computing & Mathematics':0,'BSc Computer Science with Visual Computing':0}

        self.create_fav_sub_q()
        self.create_y_or_n_q()
        self.create_buttons()

    """
    "" @name: Create favourite subject question
    "" @author: Craig Harris
    "" @description: A method to insert a question label with choices in a list box with scroll bar
    "" @prams: None
    "" @return: Void
    """

    def create_fav_sub_q(self):
        
        # Creates label in row 0, column 0 with column span 6 and aligned to the bottom right
        lblFav = Label(self.appdelegate, text='1. Which of the following subjects did you most enjoy in school?', style="Questionnaire.TLabel")
        lblFav.grid(row=0, column=0, columnspan=6, sticky='se')

        # Sets the list box border to fromat from appdelegate
        listbox_select_border = Frame(self.appdelegate)

        # Sets the list box height to 3 and width to length of text within
        self.listbox_select = Listbox(listbox_select_border, height=3)

        # Creates scrollbar for y axis scroll
        scroll = Scrollbar(listbox_select_border, command= self.listbox_select.yview)
        self.listbox_select.configure(yscrollcommand=scroll.set)

        # Sets list box contents to left side and gives padding 3 to both x and y
        self.listbox_select.pack(side=LEFT, fill=X, padx=3, pady=3)
        # sets scrollbar to right side
        scroll.pack(side=RIGHT,fill=Y)

        # Creates list box in row 0, column 6  with column span 3 and aligned to bottom left
        listbox_select_border.grid(row=0, column=6, columnspan=3, sticky='sw')

        # Inserts Biology, Business, Computing, English, Information Technology, Maths and Physics into list box
        for item in ["Biology", "Business", "Computing", "English", "Information Technology", "Maths", "Physics"]:
            self.listbox_select.insert(END, item)

        # Ends selection in list box after contents
        self.listbox_select.selection_set(END)

        # Receives inputed answer in list box when answer is selcted
        self.listbox_select.bind("<<ListboxSelect>>", self.on_listbox_select)

    -
    """
    "" @name: Clear Response
    "" @author: Craig Harris
    "" @description: A method which is called from the create_buttons method when the 'reset' button is pressed.
    "" @prams: None
    "" @return: Void
    """
    
    def clear_response(self):
        # Sets the list box current selection to nothing.
        self.listbox_select.selection_clear(0, END)
        self.listbox_select.selection_set(END)
        # Sets the radio button values to -1, this will clear and selections made by the user.
        self.varQ2.set(-1)
        self.varQ3.set(-1)
        self.varQ4.set(-1)
        self.varQ5.set(-1)
        self.varQ6.set(-1)
        self.varQ7.set(-1)
        self.varQ8.set(-1)
        self.varQ9.set(-1)
        self.varQ10.set(-1)

    """
    "" @name: Store Response
    "" @author: Craig Harris
    "" @description: A method that validates the responses to the questionnaire
    "" @prams: None
    "" @return: Void
    """

    def store_response(self):
        # Set default variables for listbox values
        index = self.listbox_select.curselection() [0]
        strProg = str(self.listbox_select.get(index))
        strMsg=""
        # Check that a subject has been chosen. If not then throw error.
        if strProg == "":
            strMsg = "You have not selected a favorite subject. " + '\n'
        # Check all values for the yes / no questions. If value is -1 then it has not been selected so throw an error.
        if (self.varQ2.get()==-1) or (self.varQ3.get()==-1) or (self.varQ4.get()==-1) or (self.varQ5.get()==-1) or (self.varQ6.get()==-1) or (self.varQ7.get()==-1) or (self.varQ8.get()==-1) or (self.varQ9.get()==-1) or (self.varQ10.get()==-1):
            strMsg = strMsg + "You need to answer all Yes / No questions. "
        # If strMsg is empty then all questions have been answered. Send weightings to dictionary and display results.
        if strMsg == "":
            self.evaluate_course_dictionary()
            self.open_results_window()
        # Error message if something goes wrong that is not covered in main loop.
        else:
            tkMessageBox.showwarning("Entry Error", strMsg)

    """
    "" @name: Create Buttons
    "" @author: Craig Harris
    "" @description: Method to draw the Home, Reset and Results buttons
    "" @prams: None
    "" @return: Void
    """

    def create_buttons(self):
        # Setup button and name to be displayed
        butSubmit = Button(self.appdelegate, text='Home')
        # Direct button to specified page once used.
        butSubmit['command'] = self.appdelegate.landing_page.draw
        # Set placement of button.
        butSubmit.grid(row=17, column=0, columnspan=2, pady=[5,30], sticky="sw")

        # Setup button and name to be displayed
        butClear = Button(self.appdelegate, text='Reset', style="Admin.TButton")
        # Direct button to specified page once used.
        butClear['command'] = self.clear_response
        # Set placement of button.
        butClear.grid(row=17, column=7, columnspan=1, pady=[5, 30], sticky="se")

        # Setup button and name to be displayed
        butResult = Button(self.appdelegate, text='Results', style='Green.TButton')
        # Direct button to specified page once used.
        butResult['command'] = self.store_response
        # Set placement of button.
        butResult.grid(row=17, column=8, columnspan=2, pady=[5,30], sticky="se")

    """
    "" @name: Finish Questionnaire
    "" @author: Craig Harris    
    "" @description: Method to process questionnaire
    "" @prams: None
    "" @return: Void
    """

    def finish_questionnaire(self):

        # Make sure we've finished inserting table.
        self.insert_questionnaire_thread.join()

        # Lets loop over each questionnaire result and add these as relations to the question in the DB.
        i = 1
        for degree in self.results:
            # Insert degree name and weightings.
            self.appdelegate.db.insert('questionnaire_question', query_data={
                'degree': degree,
                'weight': self.results[degree],
                'questionnaire_id': str(self.questionnaire_id),
                    })
            i += 1

        # Update questionnaire data with results.
        self.appdelegate.db.update('questionnaire', data = {
            'finished_timestamp':str(time.time()),
            'recommended_degree':self.recommended_degree,
            'user_id':str(self.appdelegate.user_id)
                }, where=("(`questionnaire_id` == '%s')" % self.questionnaire_id), limit=1)

    """
    "" @name: Quit
    "" @author: Craig Harris
    "" @description: Method to ensure that only 1 questionnaire result is stored and quit.
    "" @prams: None
    "" @return: Void
    """

    def quit(self):
        # Check to see if there are other questionnaire results for user. If so, delete the old result.
        self.appdelegate.db.delete('questionnaire', where=("(`questionnaire_id` == '%s')" % self.questionnaire_id), limit=1)
        # Draw landing page on quit
        self.appdelegate.landing_page.draw()

    """
    "" @name: Open Results Window
    "" @author: Craig Harris
    "" @description: Method to draw the results window
    "" @prams: None
    "" @return: Void
    """

    def open_results_window(self):
        # Clear GUI.
        self.appdelegate.flush_ui()
        # Setup Canvas page.
        self.canvas = Canvas(self.appdelegate, bg='#ECF0F1', width=600, height=700, bd=0, highlightthickness=0)
        data = [self.results[i] for i in self.results]
        origin_x = 242
        origin_y = 100
        size = 540
        outer_width = 50

        maxIndex, max = 0, 0
        for i in xrange(len(data)):
            # Insert data gathered from questionnaire weightings.
            if data[i] > max:
                max = data[i]
                maxIndex = i

        self.recommended_degree = self.results.keys()[maxIndex]

        # Save results
        self.finish_questionnaire_thread = threading.Thread(target=self.finish_questionnaire)
        self.finish_questionnaire_thread.start() 
        
        # Create doughnut chart used to display results.
        chart = Chart(self.canvas)
        chart.doughnut(centre=self.recommended_degree, font_size=self.appdelegate.font_size_for_os(13), origin_x = origin_x, origin_y = origin_y, size = size, outer_width = outer_width, data=data, label=self.results.keys())

        # Set positioning of chart.
        self.canvas.grid(row=1, column=0, columnspan=10, sticky="we")

        self.appdelegate.columnconfigure(1, weight=1)
        self.appdelegate.rowconfigure(17, weight=1)
        
        # Draw Home and Restart buttons and set positionings.
        butSubmit = Button(self.appdelegate, text='Home')
        butSubmit['command'] = self.appdelegate.landing_page.draw
        butSubmit.grid(row=17, column=0, columnspan=2, pady=[5,30], sticky="sw")

        butClear = Button(self.appdelegate, text='Restart', style="Admin.TButton")
        butClear['command'] = self.draw
        butClear.grid(row=17, column=8, columnspan=2, pady=[5, 30], sticky="se")