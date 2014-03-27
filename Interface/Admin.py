#!/usr/bin/env python
# encoding: utf-8
# Created by Daniel Koehler - 18/03/2014

from Tkinter import *
from ttk import *
from Application.Chart import *

import random, sys
import threading, time
import math
import platform
import datetime

"""
"" @name: Admin Page (Class)
"" @author: Daniel Koehler
"" @description: Class to handle all aspects of the administrator system and interface
"""

class AdminPage():
	def __init__(self, appdelegate):
		# Clear and initialise main properties
		self.appdelegate = appdelegate
		self.isAuthorised = False
		self.group_page_segments = {}

		# Clear canvas properties
		self.canvas =  False
		self.isInitalised =  False
		self.canvas_width = 3012
		self.canvas_height = 3000
		self.canvas_columns = 0
		
		# Create some empty data structures to store aniimation specific data
		self.left_previous_column_with_top = {}
		self.current_column = 0

	"""
	"" @name: Group Popover (Message Box)
	"" @author: Daniel Koehler	
	"" @description: Method to display a popup allowing a group to be added
	"" @prams: none
	"" @return: void
	"""

	def group_popup(self):

		# Create popup widget
		self.top = Toplevel(self.appdelegate)

		# Create title label
		group_name_lbl = Label(self.top, text="Group Name",style="GroupPopup.TLabel")
		group_name_lbl.pack()

		# Create group name input box
		self.group_name = Entry(self.top, style="GroupPopup.TEntry")
		self.group_name.pack()

		# Create submit button
		submit_btn = Button(self.top, text='Submit', command=self.add_group)
		submit_btn.pack()

		# Create cancel button
		cancel_btn = Button(self.top, text='Cancel', command=lambda: self.top.destroy())
		cancel_btn.pack()

		# Ensure this is the topmost window
		self.top.wm_attributes("-topmost", 1)
		# Set title 
		self.top.title("Add Group")
		# Set min/max sizing for window.
		self.top.minsize(180,163)
		self.top.maxsize(180,163)

	"""
	"" @name: Add Group
	"" @author: Daniel Koehler	
	"" @description: Method to the get the required data and insert a new group into the database
	"" @prams: none
	"" @return: void
	"""

	def add_group(self):
		# Insert group into database
		self.appdelegate.db.insert('group', query_data={'group_name':self.group_name.get(), 'active':True})
		# Close popup
		self.top.destroy()
		# Clear Canvas
		self.canvas.delete("all")
		# Fetch data again
		self.fetch_data_thread()
		# Draw group panel
		self.group_panel()

	"""
	"" @name: Draw
	"" @author: Daniel Koehler	
	"" @description: Main class render method
	"" @prams: none
	"" @return: void
	"""

	def draw(self): 
		

		"""
		"" @name: Draw -> Validate Authorisation Key
		"" @description: Method to check whether the correct key has been entered
		"" @prams: Event args
		"" @return: (Boolean) Is Valid Value Entry
		"""

		def validate_authorisation_key(*args):
			# If the entry text not equal to correct key
			if entry_text.get() != "1": 
				# Set a red entry colour
				authorisation_key.config(style="InputBorderError.TEntry")
				return True
			else: 
				# Set a blue entry colour
				authorisation_key.config(style="InputBorder.TEntry")
				# Set the admin auth rights
				self.isAuthorised = True
				# Remove the input box
				authorisation_key.grid_remove()
				# Draw the group panel
				self.group_panel()

		"""
		"" @name: Draw -> Did Focus In
		"" @description: Method to change the entry display to *
		"" @prams: event args
		"" @return: None
		"""

		def did_focus_in(*args):
			authorisation_key['show'] = "*"
			authorisation_key.delete(0, END)

		# Fetch data from the data base
		self.query_thread = threading.Thread(target=self.fetch_data_thread)
		self.query_thread.daemon = True
		self.query_thread.start()

		# Clear GUI
		self.appdelegate.flush_ui()
		
		# Set page title
		self.appdelegate.parent.title("Admin Authorisation")

		# Add weight to centre column
		self.appdelegate.columnconfigure(1, weight=1)
			
		# Create a home button widget 
		home_btn = Button(self.appdelegate, text="Home", style="Admin.TButton")
		home_btn['command'] = lambda: self.logout()          
		home_btn.place(x=20,y=20)
		
		# Create managed Var.
		entry_text = StringVar()
		# Set default text
		entry_text.set("Authorisation Key")
		# Creat admin key entry input box
		authorisation_key = Entry(self.appdelegate, style="InputBorder.TEntry", justify=CENTER, textvariable=entry_text)       
		# Bind value changes to method
		entry_text.trace("w", validate_authorisation_key)    
		# Bind focus to method
		authorisation_key.bind("<FocusIn>", did_focus_in)
		# Grid the Entry
		authorisation_key.grid(row=2, column=1, pady=[370,0])

	"""
	"" @name: Fetch Data Thread (Page)
	"" @author: Daniel Koehler	
	"" @description: Method to Fetch data from the database - should be called from the database.
	"" @prams: none
	"" @return: void
	"""

	def fetch_data_thread(self):

		if not self.isInitalised:
			# Fetch Pupils
			self.pupils = self.appdelegate.db.select("user", where="(`type` == 'pupil')")
			# Fetch Tests
			self.tests = self.appdelegate.db.select("test")
			# Fetch Test Questions
			self.test_questions = self.appdelegate.db.select("test_question")
			# Fetch Questionnaires
			self.questionnaires = self.appdelegate.db.select("questionnaire")
			# Fetch Questionnaire Questions
			self.questionnaire_questions = self.appdelegate.db.select("questionnaire_question")

		# Sort gruops by newest first
		self.groups = sorted(self.appdelegate.db.select("group"), key=lambda k: int(k['group_id']), reverse=True)

		# Render the main in the background still in this sub thread, this takes a few miliseconds.

		# Thread stops and will be joined after password entry.

	"""
	"" @name: Group Panel (Page)
	"" @author: Daniel Koehler	
	"" @description:
	"" @prams: Event
	"" @return: void
	"""

	def group_panel(self, event = None):

		# Ensure we've fetched our data from the database
		self.query_thread.join()
		# Set up the main page
		self.set_up_main_page()

		if not self.isInitalised:
			# If the canvas hasn't been packed pack it
			self.vbar.pack(side=RIGHT,fill=Y)
			self.canvas.pack(side = LEFT)
			# Ensure it's not packed again
			self.isInitalised = True

		# Set title
		self.appdelegate.parent.title("Admin: Group Overviews")
		# Set column inde
		self.current_column = 0

		# If we're not on Windows
		if not self.appdelegate.isWindows:   
			# Create thread
			self.query_thread = threading.Thread(target=self.start_animation_thread)
			# Die if parent does
			self.query_thread.daemon = True
			# Start thread to perform animation 
			self.query_thread.start()

	"""
	"" @name: User Panel (Page)
	"" @author: Daniel Koehler	
	"" @description: 
	"" @prams: Event - optional
	"" @return: void
	"""

	def user_panel(self, event = None):

		"""
		"" @name: User Panel -> Open Group Panel
		"" @description: Method safely open the group panel
		"" @prams: event args - optional
		"" @return: Canvas identifier
		"""

		def open_group_panel(*args):
			# Clear the canvas
			self.canvas.delete("all")
			# Fetch data again
			self.fetch_data_thread()
			# Start draing the canvas
			self.group_panel()

		"""
		"" @name: User Panel -> Button ID for coordinates
		"" @description: Method to return the correct canvas identifier for the back rectangle piece of the button
		"" @prams: relative x, relative y
		"" @return: Canvas identifier
		"""

		def button_id_for_coords(x, y):
			# Get absolute coordinates from relative event coordinates.
			x = self.canvas.canvasx(x)
			y = self.canvas.canvasy(y)

			# Get the item that triggered the event
			item = self.canvas.find_closest(x, y)[0]
			# Get items that this item wraps.
			items = self.canvas.find_overlapping(*self.canvas.bbox(item))
				
			# Iterate over these items
			for item in items:
				# If the item has a button tag
				if len(self.canvas.gettags(item)) and self.canvas.gettags(item)[0] == "button":#
					# Return item
					return item
			# Default return to the item item in the items list - left in scope by the for loop.
			return item

		"""
		"" @name: User Panel -> Hover In
		"" @description: Method to change the fill of menu buttons on hover
		"" @prams: Event
		"" @return: Void
		"""

		def hover_in(event):    
			# Get button it using the `button_id_for_coords` method and change it's fill to the active colour.
			self.canvas.itemconfig(button_id_for_coords(event.x, event.y), fill="#1abc9c")

		"""
		"" @name: User Panel -> Hover Out
		"" @description: 
		"" @prams: Event 
		"" @return: Void
		"""
		
		def hover_out(event):    
			# Configure all buttons to their default style
			self.canvas.itemconfig("button", fill="#16A085")

		# Clear the canvas 
		self.canvas.delete("all")
		# Set a row height in pixels
		row = 160
		# Set VERTICAL offset
		x = 120
		# Set a HORIZONTAL offset
		y = 0
		
		# Bind return to group button press
		self.canvas.tag_bind('group', '<ButtonPress-1>', self.get_group)

		# Create home button
		home_btn = Button(self.appdelegate, text="Home", style="Admin.TButton")
		home_btn['command'] = lambda: self.logout()
		self.canvas.create_window(20, 20, anchor=NW, window=home_btn)

		# Create Groups button
		groups_btn = self.canvas.create_rectangle(83, 20, 163, 62, fill="#16a186", width=0, tag=("button", "hover-green"))
		groups_btn_text = self.canvas.create_text(121, 40, text="Groups", fill="#FFFFFF", tag="hover-green")        

		# Create Users button
		users_btn = self.canvas.create_rectangle(163, 20, 243, 62, fill="#16a186", width=0, tag=("button", "hover-green"))
		users_btn_text = self.canvas.create_text(201, 40, text="Users", fill="#FFFFFF", tag="hover-green")

		# Bind click events
		self.canvas.tag_bind(groups_btn, "<ButtonPress-1>", open_group_panel)
		self.canvas.tag_bind(groups_btn_text, "<ButtonPress-1>", open_group_panel)

		# Binf over hover in/out events
		self.canvas.tag_bind("hover-green", "<Enter>", hover_in)
		self.canvas.tag_bind("hover-green", "<Leave>", hover_out)
		
		r, l = 163, 243 # button left, button right
		# Create the small triangle to indicate which is the active button
		self.canvas.create_polygon((r + l) / 2 - 10, 62, (r + l) / 2, 55, (r + l) / 2 + 10, 62, fill="#ecf0f1", outline="#ecf0f1", state=DISABLED)

		# Set up some storage for the loops below
		scores = []
		pupils = []

		# Clear the datestring
		datestring = False

		# Create `pupils` label
		self.canvas.create_text(y + 100, x + 40, text="Pupils", anchor="nw",font=("Helvetica",self.appdelegate.font_size_for_os(30)), fill="#2c3e50", activefill="#2c3e50")
		# Create `total` pupils label
		self.canvas.create_text(y + 100, x + 90, text="Total Pupils: %s" % len(self.pupils), anchor="nw",font=("Helvetica",self.appdelegate.font_size_for_os(15)), fill="#2c3e50", activefill="#2c3e50")
		
		# Decrement vertical offset
		x -= 20

		# Set total tests value based on the number of tests a given user has taken for the number of users we have
		total_tests = len(scores)

		# Crea border top
		self.canvas.create_line(y + 150, x + 156, y + 850, x + 156, fill="#BDC3C7")

		# Create `Name` label
		self.canvas.create_text(y + 200, x + 160, text="Name", anchor="nw",font=("Helvetica",self.appdelegate.font_size_for_os(15), "bold"), fill="#34495e", activefill="#34495e")
		# Create `Created` label
		self.canvas.create_text(y + 500, x + 160, text="Created", anchor="nw",font=("Helvetica",self.appdelegate.font_size_for_os(15), "bold"), fill="#34495e", activefill="#34495e")
		# border bottom
		self.canvas.create_line(y + 150, x + 181, y + 850, x + 181, fill="#BDC3C7")        

		# Increment vertical offset by 28 pixels
		x += 28

		# If we don't have any pixels
		if not len(self.pupils):
			# Create default label 
			self.canvas.create_text(y + 502, x + 360, text="No Users In Data Store.",font=("Helvetica",self.appdelegate.font_size_for_os(15), "bold"), fill="#34495e", activefill="#34495e")

		# Iterate over all pupils
		for pupil in self.pupils:
			# Create pupil name label
			self.canvas.create_text(y + 202, x + 160, text="%s %s" % (pupil['first_name'], pupil['last_name']), anchor="nw",font=("Helvetica",self.appdelegate.font_size_for_os(15)), fill="#34495e", activefill="#34495e")
			# Get time added at string 
			d = int(datetime.datetime.fromtimestamp(int(pupil['added_timestamp'][0:10])).strftime('%d'))
			# Create `added` label
			self.canvas.create_text(y + 500, x + 160, text="%s" % (datetime.datetime.fromtimestamp(int(pupil['added_timestamp'][0:10])).strftime('%d' + ('th' if 11<=d<=13 else {1:'st',2:'nd',3:'rd'}.get(d%10, 'th')) + ' %B %Y,  %X ')), anchor="nw",font=("Helvetica",self.appdelegate.font_size_for_os(15)), fill="#34495e", activefill="#34495e")
			# Create boder bottom
			self.canvas.create_line(y + 150, x + 183, y + 850, x + 183, fill="#FFFFFF")
			# Create View Student button
			self.canvas.create_oval(y + 850, x + 160, y +  870, x + 180, fill="#ecf0f1", outline="#ecf0f1", activeoutline="#bdc3c7", activefill="#bdc3c7", tags=(("user-%s" % pupil['user_id']), "user"))
			# Create View Student button text
			self.canvas.create_text(y + 860, x + 170, text="⇢",font=("Helvetica",self.appdelegate.font_size_for_os(15)),state="disabled", fill="#2980b9", activefill="", tags=(("user-%s" % pupil['user_id']), "user"))
			
			# Increment vertical offset by 28 pixels
			x += 28

		# Bind View Student button press
		self.canvas.tag_bind('user', '<ButtonPress-1>', self.get_user)

		# Set Canvas Dimensions
		self.canvas_height = max(x + 300, 800)
		self.canvas.config(height=self.canvas_height)
		# Set Canvas Scroll Region
		self.canvas.config(scrollregion=(0,0,self.canvas_width,self.canvas_height))

	"""
	"" @name: Single Group (Page)
	"" @author: Daniel Koehler	
	"" @description: Method to start the animation of each group chart on the group page.
	"" @prams: none
	"" @return: void
	"""

	def start_animation_thread(self):
		# Loop over each created thread
		for thead in self.animate_chart_thread:
			# Start the animation
			thead.start()  

	"""
	"" @name: Set Up Main Page
	"" @author: Daniel Koehler	
	"" @description: Method to draw in the back ground the main group page elements
	"" @prams: None 
	"" @return: void
	"""

	def set_up_main_page(self):

		"""
		"" @name: Set Up Main Page -> Button ID for coordinates
		"" @description: Method to return the correct canvas identifier for the back rectangle piece of the button
		"" @prams: relative x, relative y
		"" @return: Canvas identifier
		"""

		def button_id_for_coords(x, y):
			# Get absolute coordinates from relative event coordinates.
			x = self.canvas.canvasx(x)
			y = self.canvas.canvasy(y)

			# Get the item that triggered the event
			item = self.canvas.find_closest(x, y)[0]
			# Get items that this item wraps.
			items = self.canvas.find_overlapping(*self.canvas.bbox(item))
				
			# Iterate over these items
			for item in items:
				# If the item has a button tag
				if len(self.canvas.gettags(item)) and self.canvas.gettags(item)[0] == "button":#
					# Return item
					return item
			# Default return to the item item in the items list - left in scope by the for loop.
			return item

		"""
		"" @name: Set Up Main Page -> Hover In
		"" @description: Method to change the fill of menu buttons on hover
		"" @prams: Event
		"" @return: Void
		"""

		def hover_in(event):    
			# Get button it using the `button_id_for_coords` method and change it's fill to the active colour.
			self.canvas.itemconfig(button_id_for_coords(event.x, event.y), fill="#1abc9c")

		"""
		"" @name: Set Up Main Page -> Hover Out
		"" @description: 
		"" @prams: Event 
		"" @return: Void
		"""
		
		def hover_out(event):    
			# Configure all buttons to their default style
			self.canvas.itemconfig("button", fill="#16A085")

		"""
		"" @name: Set Up Main Page -> On MouseWheel
		"" @description: Method to handle to mouse scrolling
		"" @prams: Event
		"" @return: void
		"""

		def _on_mousewheel(event):
			# We face operating system interoperability issues with this function call so we'll catch and display cleanly any errors we may hit.
			try: 
				# Scroll the canvas to the correct location based on the scroll event.
				self.canvas.yview_scroll(-1*(event.delta), "units")
			except:
				# Print error rather than let it throw and error.
				print "Scroll OS interoperability error, trying `-1*(event.delta)` - units."

		"""
		"" @name: Set Up Main Page -> Animate Chart
		"" @description: Method to animate the bar chart `onpageload`.
		"" @prams:  
		"" @return:
		"""

		def animate_chart(animation_index, inset, base):
			# Clear n
			n = 0
			# Set default inset value - given this page is being draw in first column a value of 840 will start drawing near to right hand side of the column
			inset_store = 840
			# Loop until we decide to break
			while 1:
				# Increment by an arbitrary small value
				n += 0.08
				# Set Y for X (n) 
				y = n * n
				# Reset inset
				inset = inset_store
				# If we've finished the animation
				if n*n >= 1:
					# loop over each rectangle
					for item in animation_index:
						# Configure the size of the rectangle 
						self.canvas.coords(item['name'], (inset, base, inset + 8, base - (item['value'])))
						# Reduce the insert
						inset -= 10
					break
				# loop over each rectangle
				for item in animation_index:
					# Configure the size of the rectangle 
					self.canvas.coords(item['name'], (inset, base, inset + 8, base - (item['value'] * y)))
					# Reduce the insert
					inset -= 10
					# Sleep for a small amount of time
					time.sleep(.0001)

		# If the canvas hasn't been configured.
		if not self.canvas:
			# Create new canvas
			self.canvas = Canvas(self.appdelegate, bg='#ECF0F1',width=self.canvas_width,height=self.canvas_height,bd=0, highlightthickness=0)
			# Set a default width - this will certainly change
			self.canvas_width = 1004 * 3
			# Create a vertical scrollbar 
			self.vbar = Scrollbar(self.appdelegate,orient=VERTICAL)
			# Link this to the canvas scroll action
			self.vbar.config(command=self.canvas.yview)
			# Create the inverse link
			self.canvas.config(yscrollcommand=self.vbar.set)
			# Set a scroll region
			self.canvas.config(scrollregion=(0,0,self.canvas_width,self.canvas_height))
			# Bind the mouse input to the method
			self.canvas.bind_all("<MouseWheel>", _on_mousewheel)

   
		# Set a row height in pixels
		row = 160
		# Set VERTICAL offset
		x = 120
		# Set a HORIZONTAL offset
		y = 0

		# Create a group label
		self.canvas.create_text(y + 100, x + 40, text="Groups", anchor="nw",font=("Helvetica",self.appdelegate.font_size_for_os(30)), fill="#2c3e50", activefill="#2c3e50")

		# Increment vertical offset
		x += 100

		# Clear animation thread storage
		self.animate_chart_thread = []

		# Loop over all groups ensuring they're not all inactive
		if all([group['active'] == False for group in self.groups]):
			self.canvas.create_text(y + 502, x + 160, text="No Groups In Data Store.",font=("Helvetica",self.appdelegate.font_size_for_os(15), "bold"), fill="#34495e", activefill="#34495e")

		# Iterate over all groups
		for group in self.groups:
			# Ensure the group is not inactive
			if group['active']:
				# Clear scores
				scores = []
				# Clear date string
				datestring = False

				# Loop over all pupils
				for pupil in self.pupils:
					# If the pupil belongs to this group
					if pupil['group_id'] == group['group_id']:
						# Loop over all tests
						for test in self.tests:
							# If the test belongs to the current user and they're absolutely finished it.
							if test['user_id'] == pupil['user_id'] and test['finished_timestamp'] != 'null':
								# If the date string is empty create it
								if not datestring:
									# Get the day the test was taken and assign it to d
									d = int(datetime.datetime.fromtimestamp(int(test['started_timestamp'][0:10])).strftime('%d'))
									# Append the test string to the test data store in the form e.g. 15th May 2013 15:20:15
									datestring = datetime.datetime.fromtimestamp(int(test['started_timestamp'][0:10])).strftime('%d' + ('th' if 11<=d<=13 else {1:'st',2:'nd',3:'rd'}.get(d%10, 'th')) + ' %B %Y') # 15th May 2013 - 17th May 2013
								# Clear test score
								score = 0
								# Iterate through test questions
								for test_question in self.test_questions:
									# If the test question belongs to the current test
									if test_question['test_id'] == test['test_id']:
										# if the user answered correctly
										if test_question['correct_answer'] == test_question['answer']:
											score += 1 # increment their score
								# Roughly use time to reduce the charted value of their score and append it to the scores list
								scores.append(score - abs((float(test['finished_timestamp']) - float(test['started_timestamp'])) / 45000))
				
				# If we didn't create a date string because a user in this group hasn't sat the test, set a default one
				if not datestring:
					datestring = "Unknown. Likely some time in the future."

				# Sort scores by reverse value
				scores = sorted(scores, reverse=True)

				# Create Group Name label
				self.canvas.create_text(y + 170, x + 40, text=group['group_name'], anchor="nw",font=("Helvetica",self.appdelegate.font_size_for_os(20)), fill="#2c3e50", activefill="#2c3e50")
				# Create group date label
				self.canvas.create_text(y + 170, x + 70, text="Date: " + datestring, anchor="nw",font=("Helvetica",self.appdelegate.font_size_for_os(15)), fill="#2c3e50", activefill="#2c3e50")
					
				# Set total tests value based on the number of tests a given user has taken for the number of users we have
				total_tests = len(scores)

				# If we have more than one score
				if len(scores):
					# Create average score label
					self.canvas.create_text(y + 170, x + 110, text=("Average Test Score: %.2f" % abs(reduce(lambda x, y: x + y, scores) / float(len(scores)))), anchor="nw",font=("Helvetica",self.appdelegate.font_size_for_os(15)), fill="#34495e", activefill="#34495e")
					# Create no. tests label
					self.canvas.create_text(y + 190, x + 132, text=("from %d tests." % total_tests), anchor="nw",font=("Helvetica", 11), fill="#34495e", activefill="#34495e")
				else: # Otherwise we don't have any scores, lets set default values
					# Create deafault no scores label
					self.canvas.create_text(y + 170, x + 110, text="No scores to average", anchor="nw",font=("Helvetica",self.appdelegate.font_size_for_os(15)), fill="#34495e", activefill="#34495e")
					# Create no. tests label
					self.canvas.create_text(y + 190, x + 132, text="from 0 tests.", anchor="nw",font=("Helvetica", 11), fill="#34495e", activefill="#34495e")
				
				# Create Delete button
				self.canvas.create_oval(y + 895, x + (row / 2) + 35,y +  915, x + (row / 2 - 25) + 80, fill="#bdc3c7", outline="#bdc3c7", activeoutline="#2c3e50", activefill="#2c3e50", tags=(("group-%s" % group['group_id']), "delete-group"))
				# Create Delete Text Label
				self.canvas.create_text(y + 905, x + (row / 2 + 46), text="✖",font=("Helvetica",self.appdelegate.font_size_for_os(12)),state="disabled", fill="#ecf0f1", tags=(("group-%s" % group['group_id']), "delete-group"))

				# Create Group link button
				self.canvas.create_oval(y + 880, x + (row / 2 - 25),y +  930, x + (row / 2 - 25) + 50, fill="#ecf0f1", outline="#ecf0f1", activeoutline="#bdc3c7", activefill="#bdc3c7", tags=(("group-%s" % group['group_id']), "group"))
				# Create group overview text 
				self.canvas.create_text(y + 906, x + (row / 2 + 2), text="⇢",font=("Helvetica",self.appdelegate.font_size_for_os(30)),state="disabled", fill="#2c3e50", activefill="", tags=(("group-%s" % group['group_id']), "group"))
				# Add a bottom border 
				self.canvas.create_line(y + 150, x + row, y + 850, x + row, fill="#BDC3C7")

				# Clear the animation index for this group chart
				animation_index = []
				
				# If we have scores
				if len(scores):
					# Decide on the number of pixels that the max value of a score should fill
					fact = 70 / 6 
					# Decide on where we want to start drawing from on x axis
					inset = y + 850
					# Set a lower edge value
					base = x + row - 1

					# Loop over all scores for this group
					for score in scores:
						# Reduce the inset
						inset -= 10
						# Check whether we're using Windows and if we are don't create animations
						if self.appdelegate.isWindows:
							chart_item = self.canvas.create_rectangle(inset, base, inset + 8, base - int(10 + int(score) * fact), fill="#3498db", outline="#3498db", activefill="#2980b9", activeoutline="#2980b9")
						else:
							# Create the small rectangle to be enlarged by the animation script
							chart_item = self.canvas.create_rectangle(inset, base, inset + 8, base, fill="#3498db", outline="#3498db", activefill="#2980b9", activeoutline="#2980b9")
							# Add this data to the animation index storage array
							animation_index.append({'name':chart_item, 'value' :int(10 + int(score) * fact)})

					# Add all animation information to a thread object and add this to a property of this class.
					if not self.appdelegate.isWindows:    
						self.animate_chart_thread.append(threading.Thread(target=animate_chart, args=(animation_index, inset, base)))
						# End animation if parent thread dies.
						self.animate_chart_thread[-1].daemon = True 
				# Add the height of a row to the vertical offset
				x += row
		# Add the 500 pixels to the vertical offset at the end of the page
		x += 500 

		# Set Canvas Dimensions
		self.canvas_height = max(x, 800, self.canvas_height)
		self.canvas.config(height=self.canvas_height)
		# Set Canvas Scroll Region
		self.canvas.config(scrollregion=(0,0,self.canvas_width,self.canvas_height))
		
		# Bind group overview button presss event to method 
		self.canvas.tag_bind('group', '<ButtonPress-1>', self.get_group)
		# Bind delete group button presss event to method 
		self.canvas.tag_bind('delete-group', '<ButtonPress-1>', self.delete_group)

		# Create a home button to log user out
		home_btn = Button(self.appdelegate, text="Home", style="Admin.TButton")
		home_btn['command'] = lambda: self.logout()
		self.canvas.create_window(20, 20, anchor=NW, window=home_btn)

		# Create a group button
		groups_btn = self.canvas.create_rectangle(83, 20, 163, 62, fill="#16a186", width=0, tag=("button", "hover-green"))
		groups_btn_text = self.canvas.create_text(121, 40, text="Groups", fill="#FFFFFF", tag="hover-green")        

		# Create a user button to show the user page
		users_btn = self.canvas.create_rectangle(163, 20, 243, 62, fill="#16a186", width=0, tag=("button", "hover-green"))
		users_btn_text = self.canvas.create_text(201, 40, text="Users", fill="#FFFFFF", tag="hover-green")

		# Bind the events for the above buttons press triggers
		self.canvas.tag_bind(users_btn, "<ButtonPress-1>", self.user_panel)
		self.canvas.tag_bind(users_btn_text, "<ButtonPress-1>", self.user_panel)

		# Bind button hover in and out events to methods 
		self.canvas.tag_bind("hover-green", "<Enter>", hover_in)
		self.canvas.tag_bind("hover-green", "<Leave>", hover_out)
		
		
		r, l = 83,163 # button left, button right
		# Create the small triangle to indicate which is the active button
		self.canvas.create_polygon((r + l) / 2 - 10, 62, (r + l) / 2, 55, (r + l) / 2 + 10, 62, fill="#ecf0f1", outline="#ecf0f1", state=DISABLED)

		# Create an add group button
		add_group_btn = Button(self.appdelegate, text="+ Group", style="Admin.TButton")
		add_group_btn['command'] = self.group_popup
		self.canvas.create_window(242, 20, anchor=NW, window=add_group_btn)
		
	"""
	"" @name: Single Group (Page)
	"" @author: Daniel Koehler	
	"" @description: Method to draw page for a group user of given ID.
	"" @prams: (Integer) Origin Y,(Integer) User ID
	"" @return: void
	"""
		
	def single_group(self, x, group_id):

		# Row height in pixels
		row = 160
		# Set horizontal offset
		y = 1004	

		# Create some nice auxiliary storage
		scores = []
		pupils = []
		
		# Clear textual date representation
		datestring = False

		# Create Back Button 
		self.canvas.create_oval(y + 65, x + 65, y +  115, x + 115, fill="#ecf0f1", outline="#ecf0f1", activeoutline="#bdc3c7", activefill="#bdc3c7", tags=(("back"), "group-back", "remove_for_move_one"))
		self.canvas.create_text(y + 91, x + 92, text="⇠",font=("Helvetica",self.appdelegate.font_size_for_os(30)),state="disabled", fill="#2c3e50", activefill="", tags=("remove_for_move_one"))
		
		# Loop over every group from the database
		for group in self.groups:
			# If it's the group we're looking forward break
			if group['group_id'] == group_id:
				break

		# Iterate over all user in database
		for pupil in self.pupils:
			if pupil['group_id'] == group['group_id']: # If this is the group we're looking for
				for test in self.tests: # Loop over all tests
					if test['user_id'] == pupil['user_id'] and test['finished_timestamp'] != 'null': # If this test was sat by the current user and they finished it
						# If the date-string is False.
						if not datestring:
							# Get the day the test was taken and assign it to d
							d = int(datetime.datetime.fromtimestamp(int(test['started_timestamp'][0:10])).strftime('%d'))
							# Append the test string to the test data store in the form e.g. 15th May 2013 15:20:15
							datestring = datetime.datetime.fromtimestamp(int(test['started_timestamp'][0:10])).strftime('%d' + ('th' if 11<=d<=13 else {1:'st',2:'nd',3:'rd'}.get(d%10, 'th')) + ' %B %Y') # 15th May 2013 - 17th May 2013
						# Clear score count
						score = 0
						# Iterate over all test questions
						for test_question in self.test_questions:
							# If it's the current test
							if test_question['test_id'] == test['test_id']:
								# If they got the correct answer
								if test_question['correct_answer'] == test_question['answer']:
									# Increment the score
									score += 1
						# Add this score to the data store
						scores.append(score)
						# Create test length string
						time = datetime.datetime.fromtimestamp(int(test['finished_timestamp'][0:10]) - int(test['started_timestamp'][0:10])).strftime('%M minutes and %S seconds')
						# Append the pupil data, test length, and score to the array of pupils 
						pupils.append({'info' : pupil, 'score': score, 'time': time})
						
		
		# Reverse and sort the scores and take the 20 highest.
		scores = sorted(sorted(scores), reverse=True)[0:20]

		# Create the group name label
		self.canvas.create_text(y + 170, x + 40, text=group['group_name'], anchor="nw",font=("Helvetica",self.appdelegate.font_size_for_os(20)), fill="#2c3e50", activefill="#2c3e50", tags=("remove_for_move_one"))
			
		# If there are no tests that have been taken then the datestring will be False, so lets set an alternate message.
		if not datestring:
			datestring = "Unknown. Likely some time in the future."

		# Create the group date label.
		self.canvas.create_text(y + 170, x + 70, text="Date: " + datestring, anchor="nw",font=("Helvetica",self.appdelegate.font_size_for_os(15)), fill="#2c3e50", activefill="#2c3e50", tags=("remove_for_move_one"))
		
		# Get the total number of tests for this group
		total_tests = len(scores)

		# If we have some scores
		if len(scores):
			# Create average group score
			self.canvas.create_text(y + 170, x + 110, text=("Average Test Score: %.2f" % abs(reduce(lambda x, y: x + y, scores) / float(len(scores)))), anchor="nw",font=("Helvetica",self.appdelegate.font_size_for_os(15)), fill="#34495e", activefill="#34495e", tags=("remove_for_move_one"))
			# Create number of tests label
			self.canvas.create_text(y + 190, x + 132, text=("from %d tests." % total_tests), anchor="nw",font=("Helvetica", 11), fill="#34495e", activefill="#34495e", tags=("remove_for_move_one"))
		else:   
			# Create error label 
			self.canvas.create_text(y + 170, x + 110, text="No scores to average", anchor="nw",font=("Helvetica",self.appdelegate.font_size_for_os(15)), fill="#34495e", activefill="#34495e", tags=("remove_for_move_one"))
			# Create static empty score label
			self.canvas.create_text(y + 190, x + 132, text="from 0 tests.", anchor="nw",font=("Helvetica", 11), fill="#34495e", activefill="#34495e", tags=("remove_for_move_one"))
	
		# Create top border for user title
		self.canvas.create_line(y + 150, x + 156, y + 850, x + 156, fill="#BDC3C7", tags=("remove_for_move_one"))
		# Create name label
		self.canvas.create_text(y + 200, x + 160, text="Name", anchor="nw",font=("Helvetica",self.appdelegate.font_size_for_os(15), "bold"), fill="#34495e", activefill="#34495e", tags=("remove_for_move_one"))
		# Create label to display users lastest score 
		self.canvas.create_text(y + 310, x + 160, text="Latest Score", anchor="nw",font=("Helvetica",self.appdelegate.font_size_for_os(15), "bold"), fill="#34495e", activefill="#34495e", tags=("remove_for_move_one"))
		# Create user time taken for latest label
		self.canvas.create_text(y + 505, x + 160, text="Time Taken", anchor="nw",font=("Helvetica",self.appdelegate.font_size_for_os(15), "bold"), fill="#34495e", activefill="#34495e", tags=("remove_for_move_one"))
		# Create bottom border for user title
		self.canvas.create_line(y + 150, x + 181, y + 850, x + 181, fill="#BDC3C7", tags=("remove_for_move_one"))        

		# Add height of user title to vertical offset
		x += 28

		# If there are no users
		if not len(pupils):
			# Create no users error message 
			self.canvas.create_text(y + 502, x + 360, text="No Users In This Group.",font=("Helvetica",self.appdelegate.font_size_for_os(15), "bold"), fill="#34495e", activefill="#34495e", tags=("remove_for_move_one"))

		# Iterate over each user in pupils from this group
		for pupil in pupils:
			# Create user's name label
			self.canvas.create_text(y + 202, x + 160, text="%s %s" % (pupil['info']['first_name'], pupil['info']['last_name']), anchor="nw",font=("Helvetica",self.appdelegate.font_size_for_os(15)), fill="#34495e", activefill="#34495e", tags=("remove_for_move_one"))
			# Create user's score label
			self.canvas.create_text(y + 395, x + 160, text="%s/6" % (pupil['score']), anchor="nw",font=("Helvetica",self.appdelegate.font_size_for_os(15)), fill="#34495e", activefill="#34495e", tags=("remove_for_move_one"))
			# Create time taken label
			self.canvas.create_text(y + 507, x + 160, text="%s" % (pupil['time']), anchor="nw",font=("Helvetica",self.appdelegate.font_size_for_os(15)), fill="#34495e", activefill="#34495e", tags=("remove_for_move_one"))
			# Create border bottom
			self.canvas.create_line(y + 150, x + 183, y + 850, x + 183, fill="#FFFFFF", tags=("remove_for_move_one"))
			# Create `view user` button
			self.canvas.create_oval(y + 850, x + 160, y +  870, x + 180, fill="#ecf0f1", outline="#ecf0f1", activeoutline="#bdc3c7", activefill="#bdc3c7", tags=(("user-%s" % pupil['info']['user_id']), "user", "remove_for_move_one"))
			# Create `view user` arrow
			self.canvas.create_text(y + 860, x + 170, text="⇢",font=("Helvetica",self.appdelegate.font_size_for_os(15)),state="disabled", fill="#2980b9", activefill="", tags=(("user-%s" % pupil['info']['user_id']), "user", "remove_for_move_one"))
			
			# Add height of user title to vertical offset
			x += 28

		# Set Canvas Dimensions
		self.canvas_height = max(x, 800, self.canvas_height)
		self.canvas.config(height=self.canvas_height)
		# Set Canvas Scroll Region
		self.canvas.config(scrollregion=(0,0,self.canvas_width,self.canvas_height))

		# Bind `on-click` to return button
		self.canvas.tag_bind('group-back', '<ButtonPress-1>', self.animate_left_for_column)
		# Bind View Student button press
		self.canvas.tag_bind('user', '<ButtonPress-1>', self.get_user)

	"""
	"" @name: Single User (Page)
	"" @author: Daniel Koehler	
	"" @description: Method to draw page for a single user of given ID.
	"" @prams: (Integer) Origin X,(Integer) Origin Y (Not the other way around),(Integer) User ID
	"" @return: void
	"""
		
	def single_user(self, y, x, user_id):

		# Create some nice auxiliary storage
		tests = {}
		# Clear textual date representation
		datestring = False
		# Row height in pixels
		row = 160

		# Create Back Button
		self.canvas.create_oval(y + 65, x + 65, y +  115, x + 115, fill="#ECF0F1", outline="#ECF0F1", activeoutline="#BDC3C7", activefill="#BDC3C7", tags=(("back"), "group-back", "remove_for_move_two", "remove_for_move_one"))
		self.canvas.create_text(y + 91, x + 92, text="⇠",font=("Helvetica",self.appdelegate.font_size_for_os(30)),state="disabled", fill="#2C3E50", activefill="", tags=("remove_for_move_two", "remove_for_move_one"))

		# Iterate over all user in database
		for pupil in self.pupils:
			if pupil['user_id'] == user_id: # If this is the user we're looking for
				for test in self.tests: # Loop over all tests
					if test['user_id'] == pupil['user_id'] and test['finished_timestamp'] != 'null': # If this test was sat by the current user and they finished it
						# Add this test to our tests dictionary
						tests[test['test_id']] = {'questions':[], 'score': 0} 
						# If the date-string is False.
						if not datestring:
							# Get the day the test was taken and assign it to d
							d = int(datetime.datetime.fromtimestamp(int(test['started_timestamp'][0:10])).strftime('%d'))
							# Append the test string to the test data store in the form e.g. 15th May 2013 15:20:15
							tests[test['test_id']]['time_taken'] = datetime.datetime.fromtimestamp(int(test['started_timestamp'][0:10])).strftime('%d' + ('th' if 11<=d<=13 else {1:'st',2:'nd',3:'rd'}.get(d%10, 'th')) + ' %B %Y,  %X ')
						# Iterate over all test questions
						for test_question in self.test_questions:
							if test_question['test_id'] == test['test_id']: # If the test question belongs to the current test
								# Check to see if the user got the correct answer
								if test_question['correct_answer'] == test_question['answer']:
									tests[test['test_id']]['score'] += 1 # They did so lets increment their score
								# Add this question to the tests data store
								tests[test['test_id']]['questions'].append(test_question)
				break # We're only interested in this Student.

		# Create user name label
		self.canvas.create_text(y + 170, x + 60, text=("%s %s" % (pupil['first_name'], pupil['last_name'])), anchor="nw",font=("Helvetica",self.appdelegate.font_size_for_os(40)), fill="#2c3e50", activefill="#2c3e50", tags=("remove_for_move_two", "remove_for_move_one"))
		# Create user email address label
		self.canvas.create_text(y + 170, x + 105, text=("Email Address: %s" % pupil['email_address']), anchor="nw",font=("Helvetica",self.appdelegate.font_size_for_os(16)), fill="#2c3e50", activefill="#2c3e50", tags=("remove_for_move_two", "remove_for_move_one"))
			
		# Add 50 pixels to the vertical offset
		x += 50
		# Create an empty auxiliary storage containers
		results = {}
		questionnaire = False

		# If we have questionnaires

		if len(self.questionnaires):
			# Loop over each questionnaire in the database
			for q in self.questionnaires:
				# Check if the questionnaire belongs to the current user
				if q['user_id'] == user_id: 
					questionnaire = q
					break # If it does break so that `questionnaire` contains current user's questionnaire 
		# If the the user has a questionnaire
		if questionnaire != False:
			# Loop over each questionnaire question in the database
			for question in self.questionnaire_questions:
				# Check if the questionnaire question belongs to the current questionnaire
				if question['questionnaire_id'] == questionnaire['questionnaire_id']:
					# If it does, store it.
					results[question['degree']] = question['weight']

		# Get the values only of the questionnaire data and store it in a variable called data
		data = [results[i] for i in results]

		# If data is not empty
		if len(data):
				
			# Instantiate a new instance of the Chart class
			chart = Chart(self.canvas)
			# Draw a dough nut chart
			chart.doughnut(centre=questionnaire['recommended_degree'], font_size=self.appdelegate.font_size_for_os(9), origin_x = y + 302, origin_y = x + 178, size = 400, outer_width = 40, data=data, label=results.keys())
				
			# Create the "Questionnaire" label
			self.canvas.create_text(y + 200, x + 110, text="Questionnaire", anchor="nw",font=("Helvetica",self.appdelegate.font_size_for_os(25)), fill="#2c3e50", activefill="#2c3e50", tags=("remove_for_move_two", "remove_for_move_one"))
			
			# Add 500 pixels to the vertical offset
			x += 500

		# If the user has taken more than zero tests
		if len(tests):
			# Create the "Test Results" label
			self.canvas.create_text(y + 200, x + 110, text="Test Results", anchor="nw",font=("Helvetica",self.appdelegate.font_size_for_os(25)), fill="#2c3e50", activefill="#2c3e50", tags=("remove_for_move_two", "remove_for_move_one"))

		# Add the row height in pixels to the vertical offset
		x += row
		 
		# Iterate over each test in tests 
		for test in tests:

			# Create individual test label
			self.canvas.create_text(y + 170, x, text=("Test Taken: %s - Score %s/6" % (tests[test]['time_taken'], tests[test]['score'])), anchor="nw",font=("Helvetica",self.appdelegate.font_size_for_os(17), "bold"), fill="#2c3e50", activefill="#2c3e50", tags=("remove_for_move_two", "remove_for_move_one")) 
			
			# Set question counter `i` to be 0
			i=0
			# Add 100 pixels to the horizontal offset
			y += 100

			for question in tests[test]['questions']:

				# Increment question counter
				i += 1
				# Create question text
				t = self.canvas.create_text(y + 95, x + 40, text=question['question'], width=700, anchor="nw",font=("Helvetica",self.appdelegate.font_size_for_os(15)), fill="#2c3e50", activefill="#2c3e50", tags=("remove_for_move_two", "remove_for_move_one"))
				# Get the rectangle bounding for the created element
				b = self.canvas.bbox(t)
				# Add bottom - top pixels to the vertical offset
				x += int(b[3]) - int(b[1])

				# Set default fill and active fill colours
				fill = "#1ABC9C"
				activefill = "#16A085"

				# If the user got the correct answer
				if question['answer'] != question['correct_answer']:
					# Set error fill and active fill colours
					fill = "#EC6363"
					activefill = "#C0392B"

				# Create Question Count Label
				self.canvas.create_text(y + 45, x + 20, text="%d." % i, anchor="nw",font=("Helvetica",self.appdelegate.font_size_for_os(40)), fill=fill, activefill=activefill, tags=("remove_for_move_two", "remove_for_move_one"))
				# Create Answer Title Label
				self.canvas.create_text(y + 95, x + 45, text="Answer:", width=800, anchor="nw",font=("Helvetica",self.appdelegate.font_size_for_os(15), "bold"), fill="#2c3e50", activefill="#2c3e50", tags=("remove_for_move_two", "remove_for_move_one"))
				# Create Answer Label
				self.canvas.create_text(y + 160, x + 45, text=question['answer'], width=800, anchor="nw",font=("Helvetica",self.appdelegate.font_size_for_os(15)), fill="#2c3e50", activefill="#2c3e50", tags=("remove_for_move_two", "remove_for_move_one"))
				# Create Correct Answer Title Label
				self.canvas.create_text(y + 95, x + 65, text="Correct Answer:", width=800, anchor="nw",font=("Helvetica",self.appdelegate.font_size_for_os(15), "bold"), fill="#2c3e50", activefill="#2c3e50", tags=("remove_for_move_two", "remove_for_move_one"))
				# Create Correct Answer Label
				self.canvas.create_text(y + 217, x + 65, text=question['correct_answer'], width=800, anchor="nw",font=("Helvetica",self.appdelegate.font_size_for_os(15)), fill="#2c3e50", activefill="#2c3e50", tags=("remove_for_move_two", "remove_for_move_one"))
				
				# Add 100 pixels to the vertical offset
				x += 100

			# Subtract 100 pixels from the horizontal offset to return to default a indent
			y -= 100
			# Add 50 pixels to the vertical offset
			x += 50

		# Set Canvas Dimensions
		self.canvas_height = max(x, 800, self.canvas_height)
		self.canvas.config(height=self.canvas_height)
		# Set Canvas Scroll Region
		self.canvas.config(scrollregion=(0,0,self.canvas_width,self.canvas_height))

		# Bind `on-click` to return button
		self.canvas.tag_bind('group-back', '<ButtonPress-1>', self.animate_left_for_column)

	"""
	"" @name: Get Group
	"" @author: Daniel Koehler	
	"" @description: Method to get, draw and animate to group page
	"" @prams: Event - From clicked object 
	"" @return: void
	"""

	def get_group(self, event):

		# Get canvas that imitated the event - the should be equivalent to "self.canvas".
		canvas = event.widget
		# Get absolute coordinates from relative event coordinates.
		x = canvas.canvasx(event.x)
		y = canvas.canvasy(event.y)
		# Get the specifier to the clicked item
		item = canvas.find_closest(x, y)[0]
		# Get group ID from the tags on the current element.
		group_id = self.canvas.gettags(item)[0].split("-")[1]

		# Get the vertical position at which the user page should be drawn.
		vertical_position = int(self.canvas.coords(canvas.find_closest(x, y))[1]) - 102
		
		# Store the position the user left the current column from in pixels, by index
		self.left_previous_column_with_top[self.current_column] = self.canvas.yview()[0] * self.canvas_height # Scroll top, store for return.
		
		# increment the class's column index.
		self.current_column += 1
		# Call a method to draw the user panel for ID at location.
		self.single_group(vertical_position, group_id)

		# Call the animate to function.
		self.animate_to((self.current_column - 1) * 1004, self.left_previous_column_with_top[self.current_column - 1], self.current_column * 1004, vertical_position) # Threaded function.
		
	"""
	"" @name: Delete Group
	"" @author: Daniel Koehler	
	"" @description: Method to "Delete" Group from database - in reality it only deactivates it.
	"" @prams: Event - From clicked object 
	"" @return: void
	"""

	def delete_group(self, event):

		# Get canvas that imitated the event - the should be equivalent to "self.canvas".
		canvas = event.widget
		# Get absolute coordinates from relative event coordinates.
		x = canvas.canvasx(event.x)
		y = canvas.canvasy(event.y)
		# Get the specifier to the clicked item
		item = canvas.find_closest(x, y)[0]
		# Get group ID from the tags on the current element.
		group_id = self.canvas.gettags(item)[0].split("-")[1]

		# "Delete" group by setting active to false in the database 
		self.appdelegate.db.update('group', data={'active':False}, where="(`group_id` == '%s')" % group_id, limit=1)
		# Clear the whole of the canvas
		self.canvas.delete("all")
		# Fetch data again
		self.fetch_data_thread()
		# Re-render the group panel.
		self.group_panel()

	"""
	"" @name: Get User
	"" @author: Daniel Koehler
	"" @description: Method to draw and animate to user page for user link.
	"" @prams: Event - must be from element with tag specifying the user ID that should be fetched.
	"" @return: void
	"""

	def get_user(self, event):

		# Get canvas that imitated the event - the should be equivalent to "self.canvas".
		canvas = event.widget
		# Get absolute coordinates from relative event coordinates.
		x = canvas.canvasx(event.x)
		y = canvas.canvasy(event.y)

		# Get the specifier to the clicked item
		item = canvas.find_closest(x, y)[0]

		# Get user ID from the tags on the current element.
		user_id = self.canvas.gettags(item)[0].split("-")[1]

		# Get the vertical position at which the user page should be drawn.
		vertical_position = int(self.canvas.coords(canvas.find_closest(x, y))[1]) - 102

		# Store the position the user left the current column from in pixels, by index
		self.left_previous_column_with_top[self.current_column] = self.canvas.yview()[0] * self.canvas_height # Scroll top, store for return.
		
		# Decrement the class's column index.
		self.current_column += 1

		# Call a method to draw the user panel for ID at location.
		self.single_user(self.current_column * 1004, vertical_position, user_id)

		# Call the animate to function.
		self.animate_to((self.current_column - 1) * 1004, self.left_previous_column_with_top[self.current_column - 1], (self.current_column) * 1004, vertical_position)# Threaded function.

	"""
	"" @name: Animate Left for Column
	"" @author: Daniel Koehler
	"" @description: Method to calculate and move the canvas a column to the left.
	"" @prams: Event - must be from current column, where column index greater than 0.
	"" @return: void
	"""
   
	def animate_left_for_column(self, event):

		# Get canvas that imitated the event - the should be equivalent to "self.canvas".
		canvas = event.widget
		# Get absolute coordinates from relative event coordinates.
		x = canvas.canvasx(event.x)
		y = canvas.canvasy(event.y)

		# Get the item that must have triggered the event.
		item = canvas.find_closest(x, y)[0]

		# Lets work out an approximate scroll top.
		scroll_top = canvas.yview()[0] * self.canvas_height

		# Decrement the class's column index.
		self.current_column -= 1

		# Call the animate to function.
		self.animate_to((self.current_column + 1) * 1004, scroll_top, self.current_column * 1004, self.left_previous_column_with_top[self.current_column])# Threaded function.

		# Remove all canvas elements that have a tag requesting deletion when the second column is no longer in user scope.
		if self.current_column == 0:
			self.canvas.delete("remove_for_move_one")

		# Remove all canvas elements that have a tag requesting deletion when the third column is no longer in user scope.
		if self.current_column == 1:
			self.canvas.delete("remove_for_move_two")
	
	"""
	"" @name: Animate To
	"" @author: Daniel Koehler
	"" @description: Method to move canvas to new coordinates.
	"" @prams: From horizontal, From vertical, To horizontal, To vertical - positions in pixels.
	"" @return: void
	"""

	def animate_to(self, fx, fy, tx, ty):
		def down(from_pos, to):
			# Set n to be horizontal starting position as a fraction of the width of the canvas.
			n = from_pos
			# While the canvas isn't at the requested position
			while from_pos < to:
				# Increment by a factor that seems smooth: .03
				n += 0.03
				# Increase exponentially 
				y = n * n
				# If new value is greater than or equal to the requested position, set canvas scroll to requested position and break.
				if n*n >= to:
					self.canvas.yview_moveto(to)
					break
				# Otherwise increment to new value of Y.
				self.canvas.yview_moveto(y)
				time.sleep(.0001)


		def left(from_pos, to):
			# Set n to be horizontal starting position as a fraction of the width of the canvas.
			n = from_pos
			# While the canvas isn't at the requested position
			while from_pos > to:
				# Increment by a factor that seems smooth: .03
				n -= 0.02
				y = n * n
				# If new value is less than or equal to near the requested position, set canvas scroll to requested position and break.
				if n*n <= to + .001:
					self.canvas.xview_moveto(to)
					break
				# Otherwise increment to new value of Y and loop after 1/1000 of a second.
				self.canvas.xview_moveto(y)
				time.sleep(.0001)

		def right(from_pos, to):
			# Set n to be horizontal starting position as a fraction of the width of the canvas.
			n = from_pos
			# While the canvas isn't at the requested position
			while from_pos < to:
				# Increment by a factor that seems smooth: .035
				n += 0.035
				# Increase exponentially 
				y = n * n
				# If new value is greater than or equal to the requested position, set canvas scroll to requested position and break.
				if n*n >= to:
					self.canvas.xview_moveto(to)
					break
				# Otherwise increment to new value of Y and loop after 1/1000 of a second.
				self.canvas.xview_moveto(from_pos + y)
				time.sleep(.0001)

		# If isWindows then don't animate, simply move canvas to new coordinates.
		if self.appdelegate.isWindows:
			self.canvas.xview_moveto(float(tx) / self.canvas_width)
			self.canvas.yview_moveto(float(ty) / self.canvas_height)
		else:
		# Else, we shall set up a thread for each axis of required animation
			if fy < ty: # Animating Down?
				self.animate_thread = threading.Thread(target=lambda: down(float(fy) / self.canvas_height, float(ty) / self.canvas_height))
				self.animate_thread.daemon = True
				self.animate_thread.start()
			elif fy > ty: # Animating Up?
				self.canvas.yview_moveto(float(ty) / self.canvas_height)

			if fx < tx: # Animating Right?
				self.animate_thread = threading.Thread(target=lambda: right(float(fx) / self.canvas_width, float(tx) / self.canvas_width))
				self.animate_thread.daemon = True
				self.animate_thread.start()
			elif fx > tx: # Animating Left?
				self.animate_thread = threading.Thread(target=lambda: left(float(fx) / self.canvas_width, float(tx) / self.canvas_width))
				self.animate_thread.daemon = True
				self.animate_thread.start()

	"""
	"" @name: Logout
	"" @author: Daniel Koehler
	"" @description: Method Used Ensure the administrator's authorization is removed before returning to the landing page.
	"" @prams: None
	"" @return: void
	"""

	def logout(self):
		# Clear authorised status
		self.isAuthorised = False
		# Open the landing page
		self.appdelegate.landing_page.draw()

