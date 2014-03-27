#!/usr/bin/env python
# encoding: utf-8
# Created by Craig Harris, Matt Thompson & Dhiren Solanki - 04/03/2014

from Tkinter import *
from ttk import *
import random, sys, re

class LandingPage():
    def __init__(self, appdelegate):
        self.appdelegate = appdelegate

    """
    "" @name: Help (Page)
    "" @author: Dhiren Solanki and Matt Thompson
    "" @description: Method to render Help Page
    "" @prams: None
    "" @return: void
    """

    def help(self):

        # Clean the GUI
        self.appdelegate.flush_ui()

        # Make columns one and two fill thier avalible space using a weight > 0
        self.appdelegate.columnconfigure(0, weight=1)
        self.appdelegate.columnconfigure(2, weight=1)
        self.appdelegate.rowconfigure(57, weight=1)

        # Create widgets for Help page content.

        s1 = Label(self.appdelegate, text = '1. To leave the "Help" page select the "Home" button.', font=("Helvetica",self.appdelegate.font_size_for_os(12)))
        s1.grid(row=4, column = 1, rowspan= 2, sticky= NW)

        s2 = Label(self.appdelegate, text = '2. Select "Practise Test" button to attempt a practise test.', font=("Helvetica",self.appdelegate.font_size_for_os(12)))
        s2.grid(row=6, column = 1, rowspan= 2, sticky= NW)

        s3 = Label(self.appdelegate, text = '3. Read the question at the top of the screen and select your answer using the mouse.', font=("Helvetica",self.appdelegate.font_size_for_os(12)))
        s3.grid(row=8, column = 1, rowspan= 2, sticky= NW)

        s4 = Label(self.appdelegate, text = '4. If you want to skip the question, select the "Skip" button.', font=("Helvetica",self.appdelegate.font_size_for_os(12)))
        s4.grid(row=10, column = 1, rowspan= 2, sticky= NW)

        s5 = Label(self.appdelegate, text = '5. After you have answered the second practise test question, you will be redirected to the Home page.', font=("Helvetica",self.appdelegate.font_size_for_os(12)))
        s5.grid(row=12, column = 1, rowspan= 2, sticky= NW)

        s6 = Label(self.appdelegate, text = '6. If you would like to sit the logic reasoning test select the "User Details" button.', font=("Helvetica",self.appdelegate.font_size_for_os(12)))
        s6.grid(row=14, column = 1, rowspan= 2, sticky= NW)

        s7 = Label(self.appdelegate, text = '7. Enter your details into the correct fields.', font=("Helvetica",self.appdelegate.font_size_for_os(12)))
        s7.grid(row=16, column = 1, rowspan= 2, sticky= NW)

        s8 = Label(self.appdelegate, text = '8. Select the "Submit" button to continue.', font=("Helvetica",self.appdelegate.font_size_for_os(12)))
        s8.grid(row=18, column = 1, rowspan= 2, sticky= NW)

        s9 = Label(self.appdelegate, text = '9. If you wish to start the logic reasoning test then select the "Test" button.', font=("Helvetica",self.appdelegate.font_size_for_os(12)))
        s9.grid(row=20, column = 1, rowspan= 2, sticky= NW)

        s10 = Label(self.appdelegate, text = '10. Read the question at the top of the screen and select your answer using the mouse. ', font=("Helvetica",self.appdelegate.font_size_for_os(12)))
        s10.grid(row=22, column = 1, sticky= NW)

        s10_1 = Label(self.appdelegate, text = '\tOnce you answer or skip a question you will NOT be able to return to this question! ', font=("Helvetica",self.appdelegate.font_size_for_os(12)))
        s10_1.grid(row=23, column = 1, sticky= NW)

        s11 = Label(self.appdelegate, text = '11. If you want to skip the question, select the "Skip" button.', font=("Helvetica",self.appdelegate.font_size_for_os(12)))
        s11.grid(row=24, column = 1, rowspan= 2, sticky= NW)

        s12 = Label(self.appdelegate, text = '12. On the sixth question, select your answer or select the "Skip and Finish" button.', font=("Helvetica",self.appdelegate.font_size_for_os(12)))
        s12.grid(row=26, column = 1, rowspan= 2, sticky= NW)

        s13 = Label(self.appdelegate, text = '13. You will be redirected to the "Results" page.', font=("Helvetica",self.appdelegate.font_size_for_os(12)))
        s13.grid(row=28, column = 1, rowspan= 2, sticky= NW)

        s14 = Label(self.appdelegate, text = '14. On the results page you can see your test score and review your answers.', font=("Helvetica",self.appdelegate.font_size_for_os(12)))
        s14.grid(row=30, column = 1, rowspan= 2, sticky= NW)

        s15 = Label(self.appdelegate, text = '15. You can select the "Home" button to go back to the Home page.', font=("Helvetica",self.appdelegate.font_size_for_os(12)))
        s15.grid(row=32, column = 1, rowspan= 2, sticky= NW)

        #Create widgets for questionnaire help steps

        s16 = Label(self.appdelegate, text = '1. If you would like to sit the questionnaire, select the "User Details" button.', font=("Helvetica",self.appdelegate.font_size_for_os(12)))
        s16.grid(row=36, column = 1, rowspan= 2, sticky= NW)

        s17 = Label(self.appdelegate, text = '2. Enter your details into the correct fields.', font=("Helvetica",self.appdelegate.font_size_for_os(12)))
        s17.grid(row=38, column = 1, rowspan= 2, sticky= NW)

        s18 = Label(self.appdelegate, text = '3. Select the "Submit" button to continue.', font=("Helvetica",self.appdelegate.font_size_for_os(12)))
        s18.grid(row=40, column = 1, rowspan= 2, sticky= NW)

        s19 = Label(self.appdelegate, text = '4. If you wish to start the questionnaire then select the "Questionnaire" button.', font=("Helvetica",self.appdelegate.font_size_for_os(12)))
        s19.grid(row=42, column = 1, rowspan= 2, sticky= NW)

        s20 = Label(self.appdelegate, text = '5. Select which subject you enjoy most using the mouse.', font=("Helvetica",self.appdelegate.font_size_for_os(12)))
        s20.grid(row=44, column = 1, rowspan= 2, sticky= NW)

        s21 = Label(self.appdelegate, text = '6. Select your answers to the questions using the mouse.', font=("Helvetica",self.appdelegate.font_size_for_os(12)))
        s21.grid(row=46, column = 1, rowspan= 2, sticky= NW)

        s22 = Label(self.appdelegate, text = '7. You can view your result by selecting the "Results" button, or reset the questionnaire using the "Reset" button.', font=("Helvetica",self.appdelegate.font_size_for_os(12)))
        s22.grid(row=48, column = 1, rowspan= 2, sticky= NW)
        
        s23 = Label(self.appdelegate, text = '8. On the results page you can see your recommeneded course name.', font=("Helvetica",self.appdelegate.font_size_for_os(12)))
        s23.grid(row=50, column = 1, rowspan= 2, sticky= NW)

        s24 = Label(self.appdelegate, text = '9. You can select the "Home" button to go back to the Home page.', font=("Helvetica",self.appdelegate.font_size_for_os(12)))
        s24.grid(row=52, column = 1, rowspan= 2, sticky= NW)

        #Create widgets for exit software

        s25 = Label(self.appdelegate, text = 'You can exit the software at anytime by selecting the "Quit" button.', font=("Helvetica",self.appdelegate.font_size_for_os(12)))
        s25.grid(row=56, column = 1, rowspan= 2, sticky= NW)

        #Titles

        logic = Label(self.appdelegate, text = 'How to complete the Logic Reasoning Test:', font=("Helvetica",self.appdelegate.font_size_for_os(14), "bold"))
        logic.grid(row=3, column = 1, rowspan= 1, pady=[40,20])

        que = Label(self.appdelegate, text = 'How to complete the Questionnaire:', font=("Helvetica",self.appdelegate.font_size_for_os(14), "bold"))
        que.grid(row=34, column = 1, rowspan= 1, pady=[10,10])

        exit = Label(self.appdelegate, text = 'Exiting the software:', font=("Helvetica",self.appdelegate.font_size_for_os(14), "bold"))
        exit.grid(row=54, column = 1, rowspan= 1, pady=[10,10])

        # Create home button and set destination to landing page.
        home_btn = Button(self.appdelegate, text="Home")
        home_btn['command'] = lambda: self.appdelegate.landing_page.draw()
        home_btn.grid(row=57, column = 0, columnspan=3, sticky=SW, pady=[0, 20])



