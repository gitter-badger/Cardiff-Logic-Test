#!/usr/bin/env python
# encoding: utf-8
# Created by Dhiren Solanki & Matthew Thompson - 04/03/2014

import threading, Queue, time
import tkMessageBox

class ContinuityHandler():

	def __init__(self, appdelegate):
		self.appdelegate = appdelegate

	"""
	"" @name: Initiate
	"" @author: Dhiren Solanki
	"" @description: Resets axillary storage used by this class
	"" @prams: None
	"" @return: Void
	"""

	def initiate(self):

		# Temporary store for test results before test is finished and these data is stored to database.
		self.question_data = []
		# Textual representation of question type used for setting frame title
		self.question_type = ""
		# Counts the amount of answered or skipped questions
		self.question_count = 0
		# Clears the test id, which will be set on database insert
		self.test_id = False

		# Clears the thread references
		self.insert_test_thread = False
		self.finish_test_thread = False

		# if this is not a practice test call method to insert test into database
		if not self.appdelegate.test.isPractice:
			self.insert_test_thread = threading.Thread(target = self.insert_test_table)
			self.insert_test_thread.start()

	"""
	"" @name: Insert test table 
	"" @author: Dhiren Solanki
	"" @description: Starts a new test instance in the database
	"" @prams: None
	"" @return: Void
	"""

	def insert_test_table(self):

		# inserts an instance of a test into the database
		self.test_id = self.appdelegate.db.insert('test', query_data = {
			# starts recording the time taken for the test to be completed
			'started_timestamp':str(time.time()),
			# sets an initial value for the amount of skips
			'skips':'0',
			'user_id':str(self.appdelegate.user_id)
				})
	"""
	"" @name: Finish test
	"" @author: Dhiren Solanki
	"" @description: Method to store all of the pupil's answers, questions, correct answers and test ID from self.question_data
	"" @prams: None
	"" @return: Void
	"""
	
	def finish_test(self):
		self.insert_test_thread.join()
		# Function exists only to save data from sub thread
		i = 1
		for question in self.question_data:
			# inserts the indexes, answers, questions, correct answers and test ID into the database  
			self.appdelegate.db.insert('test_question', query_data={
				'index':i,
				'answer': question['answer'],
				'question': question['question'],
				'correct_answer': question['correct_answer'],
				'test_id':str(self.test_id)
					})
			i += 1
		# updated the test instance in the database with the final time taken, amount of skips and the user ID
		self.appdelegate.db.update('test', data = {
			'finished_timestamp':str(time.time()),
			'skips':self.appdelegate.test.skips,
			'user_id':str(self.appdelegate.user_id)
				}, where=("(`test_id` == '%s')" % self.test_id), limit=1)

	"""
	"" @name: Test type textual
	"" @author: Dhiren Solanki
	"" @description: Method to check if a practice test is being run
	"" @prams: None
	"" @return: (String) test type
	"""

	def test_type_textual(self):

		# if statement to check if a practice is being run and return string
		if self.appdelegate.test.isPractice:
			return "Practice Logic Test"
		return "Logic Test"   

	"""
	"" @name: Start
	"" @author: Dhiren Solanki
	"" @description: Method to initialise and re-instantiate the composite instance of a test
	"" @prams: None
	"" @return: Void 
	"""

	def start(self):
		
		# initialises an instance of a test
		self.appdelegate.test.__init__()
		# clear continuity handler variables
		self.initiate()
		# call method to start showing questions
		self.initiate_question()

	"""
	"" @name: Start practise
	"" @author: Dhiren Solanki
	"" @description: Method to initialise and re-instantiate the composite instance of a practice test
	"" @prams: None
	"" @return: Void
	"""

	def start_practice(self):

		# initialises an instance of a test
		self.appdelegate.test.__init__()
		# Checks if a practice test is being run
		self.appdelegate.test.isPractice = True
		# clear continuity handler variables
		self.initiate()
		# call method to start showing questions
		self.initiate_question()

	"""
	"" @name: Finish
	"" @author: Dhiren Solanki
	"" @description: Method to finish the test
	"" @prams: None
	"" @return: Void
	"""
			
	def finish(self):

		# if not a practice
		if not self.appdelegate.test.isPractice:
			# start a thread to call a method to insert the test results into the database
			self.finish_test_thread = threading.Thread(target=self.finish_test)
			self.finish_test_thread.start()

		# call method to display results    
		self.appdelegate.test.results(self.question_data, self.test_type_textual())

	"""
	"" @name: Quit 
	"" @author: Dhiren Solanki
	"" @description: Method to exit partially completed test
	"" @prams: None
	"" @return: Void
	"""

	def quit(self):

		# deletes the test ID from the database, as an incomplete test does not get stored
		self.appdelegate.db.delete('test', where=("(`test_id` == '%s')" % self.test_id), limit=1)
		# draw landing page
		self.appdelegate.landing_page.draw()

	"""
	"" @name: Skip
	"" @author: Dhiren Solanki
	"" @description: Method to handle the user wishing to skip a question
	"" @prams:  (Dictionary) Question data
	"" @return: Void
	"""

	def skip(self, data):
		# Adding one to the skip data each time the skip button is pressed
		self.appdelegate.test.skips += 1
		self.question_data.append({'question':data['question'], 'answer':'Skipped', 'correct_answer':data['correct_answer']})
		# returns if finished
		if self.is_finished():
			self.finish()
			return
		# runs initiate_question
		self.initiate_question()

	"""
	"" @name: Answer
	"" @author: Dhiren Solanki & Matt Thompson
	"" @description: Method to handle the answering of the question
	"" @prams: Question, Answer, Correct Answer
	"" @return: (String)
	"""

	def answer(self, question, answer, correct_answer):

		# appends the question, pupil's answer and correct answer
		self.question_data.append({'question':question, 'answer':answer, 'correct_answer':correct_answer})
		# if statement to check if the practice test is finished   
		if self.is_finished():
			self.finish()
			return
		# if statement to see if a practise test is being run 
		if self.appdelegate.test.isPractice:
			# if statement to compare the pupil's answer to the questions correct answer
			if answer == correct_answer:
				# TKinter message box is generated with the string message shown
				tkMessageBox.showinfo("Info", "Well done your answer is correct!")
			else:
				tkMessageBox.showinfo("Info", "Sorry, that was not the correct answer.\nDidier is currently 42 years old, Wayne is one third of this age, so Wayne is 42.\n\n Wayne is double the age of Fernando so Fernando is 7 years old.")

		self.initiate_question()

	"""
	"" @name: Initate Question
	"" @author: Matt Thompson
	"" @description: Method to start showing a question
	"" @prams: None
	"" @return: Void
	"""
	
	def initiate_question(self):
		# Initiates the questions, decides which question to show next
		self.set_flags()
		self.question_count += 1
		# checks if the next question will be verbal or pictorial    
		if self.is_next_verbal():
			self.appdelegate.test.verbalQuestion()  
		else:
			self.appdelegate.test.graphQuestion()

	"""
	"" @name: Set Flags
	"" @author: Matt Thompson
	"" @description: 
	"" @prams: None
	"" @return: Void
	"""

	def set_flags(self):

		self.appdelegate.test.isLast = 0
		self.appdelegate.test.isFirst = 0
		# Checks if its the last question
		if self.is_last():       
			self.appdelegate.test.isLast = 1
		# Checks if its the first question
		if self.question_count == 0:
			self.appdelegate.test.isFirst = 1

	"""
	"" @name: Is the next question verbal
	"" @author: Matt Thompson
	"" @description: Checks if the next question is verbal
	"" @prams: Must be on the test
	"" @return: Void
	"""

	def is_next_verbal(self):
		# Check if the question type is verbal or pictorial
		if self.question_type == "Verbal Question":
			self.question_type = "Graph Question"
		# Changes from verbal to pictorial or vice versa 
		else:
			self.question_type = "Verbal Question"
			self.appdelegate.parent.title("%s | %s" % (self.test_type_textual(), self.question_type))
		if self.question_type == "Verbal Question":
			return True
		return False

	"""
	"" @name: Is this the last question
	"" @author: Matt Thompson
	"" @description: checks if the test is on the last question 
	"" @prams: Must be on the practice test or full test
	"" @return: Void
	"""


	def is_last(self): 
		# Checks whether the question is practice or the main test and then checks to see if it is the last question
		if self.appdelegate.test.isPractice and self.question_count == 1 or self.question_count == 5:
		# If its practice its checks to see if the question count is 1 which would be the last and checks to see if the main test value is 5  
			return True
		return False

	"""
	"" @name: Is Finished
	"" @author: Matt Thompson
	"" @description: Checks the test to see if it has finished
	"" @prams: Must be on the practice test or full test
	"" @return: Void
	"""

	def is_finished(self):
		 #Checks whether the question is practice or the main test and then checks to see if it is the last question
		if self.appdelegate.test.isPractice and self.question_count == 2 or self.question_count == 6:
			 #  If its practice its checks to see if the question count is 2 which would be the end and checks to see if the main test value is 6
			return True
		return False
