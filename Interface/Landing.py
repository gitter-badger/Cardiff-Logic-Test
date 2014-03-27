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
    "" @author: Dhiren Solanki
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

        