#!/usr/bin/env python
# encoding: utf-8
# Created by Dhiren Solanki & Matthew Thompson - 05/03/2014

from Tkinter import *
from ttk import *
from Application.Graph import *

import random
import threading

class Test():
    def __init__(self, appdelegate = False):
        
        self.isPractice = False;

        if appdelegate:
            self.appdelegate = appdelegate

        self.isLast = 0
        self.isFirst = 0
        # sets an intial value for the amount of skips
        self.skips = 0

        self.complement = []

        # Store for the textual questions
        self.verbal_reasoning = [
            {
                'question':"In a horse race: Hill Royal came in ahead of Trigger. Hill Royal finished after Black Beauty and Copenhagen beat black Beauty but finished after Bucephalu. Where did Hill Royal finish?",
                'answers':['First','Second', 'Third', 'Fourth'],
                'correct':3,
                # http://www.kent.ac.uk/careers/tests/logic-test.htm
            },
            {
                'question':"Forty two is seven times a particular number, what is eleven times that number?",
                'answers':['52','59','66','72'],
                'correct':2,
                # http://www.kent.ac.uk/careers/tests/logic-test.htm
            },
            {
                'question':"Debbie, Kimi and Michael have Ferraris. Michael also has a Reliant Robin. Jensen has a Mercedes and a Model T. Rubens also has a Mercedes. Debbie also has a Bugatti Veyron. Rubens has just bought a Toyota Prius. Who has the fewest cars?",
                'answers':['Kimi',' Debbie',' Jensen','Michael'],
                'correct':0,
                # http://www.kent.ac.uk/careers/tests/logic-test.htm
            },
            {
                'question':"Wayne is double the age of Fernando and one third as old as Didier who will be 48 years old in 6 years. How old is Fernando?",
                'answers':['7',' 8',' 9','10'],
                'correct':0,
                # http://www.kent.ac.uk/careers/tests/logic-test.htm
            },
            ]
        # start a thread to call a method to retrieve data
        self.data_retrival_thead = threading.Thread(target=self.data_retrival)
        # if parent dies, kill thread
        self.data_retrival_thead.daemon = True
        self.data_retrival_thead.start()

    """
    "" @name: Data retrival 
    "" @author: Dhiren Solanki
    "" @description: Method to insert an graph into the database
    "" @prams: None
    "" @return: Void
    """  

    def data_retrival(self):

        # inserts an instance of graph into the database
        self.graph_positioning = self.appdelegate.db.select('graph')

    """
    "" @name: Graph questionnaire
    "" @author: Dhiren Solanki
    "" @description: Method to clear the user interface
    "" @prams: Image, Text
    "" @return: Void
    """
            
    def graphQuestion(self, image = False, text = False):
        
        # clear graphical user interface of all widgets
        self.appdelegate.flush_ui()
        # adds a gravatar profile image if one exists
        self.appdelegate.overlay_user_profile()             

        """
        "" @name: Create graph
        "" @author: Dhiren Solanki
        "" @description: Method to create a randomly generating graph
        "" @prams: Nodes, Edges
        "" @return: Dictionary containing the start node, end node and length of the path 
        """

        def create_graph(nodes, edges):


            self.data_retrival_thead.join()
            # creates an empty graph with no nodes or edges
            graph = Graph()
            # for loop to add a nodes to the graph 
            for node in nodes:
                graph.add_node(node)
            # for loop to add edges to the graph where the minimum weight is 2 and the maximum weigh of a path is 15
            for edge in edges:
                graph.add_edge(edge[0],edge[1], random.randrange(2,15))
            # fetches a layout of the graph from the property graph_positioning 
            layout = random.choice([x['layout'] for x in self.graph_positioning])
    
            # for loop to loop over all nodes in layout
            for vertex in layout:
                # loop over each edge for node
                for edge in graph.edges[vertex]:
                    # assigns vertical and horizontal positioning to arbitrary variables a,b
                    a,b = layout[vertex], layout[edge]
                    # create the line representing an edge
                    self.canvas.create_line(a[0]*480 + 40, a[1]*340 + 40, b[0]*480 + 40, b[1]*340 + 40, smooth=True, splinesteps=120000, fill="#2c3e50")

                    # defines the values for left x, left y, right x and right y
                    lx, rx = (a[0]*480 + 40), (b[0]*480 + 40)
                    ly, ry = (a[1]*340 + 40), (b[1]*340 + 40)

                    # finds centre point of edge, and draws a masking oval
                    self.canvas.create_oval((lx + rx) / 2.0 - 10, (ly + ry) / 2.0 - 10, (lx + rx) / 2.0 + 10, (ly + ry) / 2.0 + 10, fill="#ecf0f1", width=0)
                    # adds edge weight label on top of mask
                    self.canvas.create_text((lx + rx) / 2.0, (ly + ry) / 2.0, text=graph.distances[(vertex, edge)])

            # loop over each node and render node with a letter
            for vertex in layout:
                # get position for node from layout
                a = layout[vertex]
                # draw a 40 pixel oval with an outline
                self.canvas.create_oval(a[0]*480 + 20, a[1]*340 + 20, a[0]*480 + 60, a[1]*340 + 60, fill="#2980b9", outline="#2c3e50")
                # add node letter
                self.canvas.create_text(a[0]*480 + 40, a[1]*340 + 40, text=vertex, fill="#ecf0f1")
            # sets a random starting node 
            start = random.choice(nodes)
            # sets a random end node that cannot be the starting node or incident nodes
            end = random.choice(list(set(graph.nodes) - set(start) - set(graph.edges[start])))
            # using the dijsktra method from the Graph.py to calculate the shortest path between nodes        
            total_weight = graph.dijsktra(start, end)
        
            return {'answer': total_weight, 'start':start, 'end': end}

        """
        "" @name: Get answers for answer
        "" @author: Dhiren Solanki
        "" @description: Method to create alternate answers for graph questions
        "" @prams: (Integer) Correct Answer 
        "" @return: Array of answers and correct answer index in a tuple
        """

        def get_answers_for_answer(answer):

            answers = [answer]
            # creates set of possible answers within a range of 4 to 2 times the answer 
            possible_values = set(range(4, (answer * 2)))
            for i in xrange(3):
                # append a new random choice from possible values
                answers.append(random.choice(list(possible_values - set(answers))))
            # randomly shuffle answer order
            random.shuffle(answers)
            # stores correct answer index
            index = answers.index(answer)
            # for loop that textifies answers 
            for i in range(4):
                answers[i] = "%s Miles" % answers[i]
            return answers[index], answers

        """
        "" @name: Skip Tuple
        "" @author: Dhiren Solanki
        "" @description: Method to fetches and collates data to be returned to continuity handler
        "" @prams: None
        "" @return: Dictionary containing the correct answer and the textual question
        """

        def skip_tuple():
            return dict({'correct_answer': correct_answer, 'question': textual_question })

        self.appdelegate.grid_rowconfigure(4, weight=100)
        
        # creates a canvas using the definitions for background colour, width, height, border and thickness     
        self.canvas = Canvas(self.appdelegate, bg='#ecf0f1', width=560, height=420, bd=0, highlightthickness=0)

        # Creates a new graph using some pre-defined data. This method saves a file called graph.png to the current working directory.
        question = create_graph(['A', 'B', 'C', 'D', 'E', 'F','G'], [('A', 'B'),('C','D'),('G','D'),('D','A'),('D','E'),('B','D'),('D','E'),('B','C'),('E','F'),('C','F')])
        
        # Computes some answers for our question
        correct_answer, answers = get_answers_for_answer(question['answer'])

        # Top Label
        
        description_lbl = Label(self.appdelegate, background="#ECF0F1", text="The diagram below is a map showing towns called A, B, C, etc.and the roads connecting them. Each section of road links two towns, and the number marked on the road is the distance in miles between the two towns.", border=6, width=70, wraplength=500,anchor=CENTER, justify=CENTER)

        if self.appdelegate.isWindows:
            description_lbl.config(wraplength=400)
        
        # Bottom Label  
        textual_question = "What is the shortest distance from %s to %s?" % (question['start'], question['end'])
        question_lbl = Label(self.appdelegate, background="#ECF0F1", text=textual_question, border=6, width=70, wraplength=500,anchor=CENTER, justify=CENTER)
        
        # creates four answer buttons 
        answer_one_btn = Button(self.appdelegate, text = answers[0])
        answer_one_btn['command'] = lambda: self.appdelegate.continuity_handler.answer(textual_question, answers[0], correct_answer)
        
        answer_two_btn = Button(self.appdelegate, text = answers[1])
        answer_two_btn['command'] = lambda: self.appdelegate.continuity_handler.answer(textual_question, answers[1], correct_answer)

        answer_three_btn = Button(self.appdelegate, text = answers[2])
        answer_three_btn['command'] = lambda: self.appdelegate.continuity_handler.answer(textual_question, answers[2], correct_answer)
        
        answer_four_btn = Button(self.appdelegate, text = answers[3])
        answer_four_btn['command'] = lambda: self.appdelegate.continuity_handler.answer(textual_question, answers[3], correct_answer)

        # if statement if it is a practice test and is the last question the display the buttons 'Home' and 'Skip & Finish Practice'
        if self.isPractice and self.isLast:
            home_btn = Button(self.appdelegate, text="Home")
            next_btn = Button(self.appdelegate, style='Wide.Green.TButton', text="Skip & Finish Practice")

        # else if statement for the last question in the logic test to display the buttons 'Home' and 'Skip & Finish'
        elif self.isLast:
            home_btn = Button(self.appdelegate, text="Home")
            next_btn = Button(self.appdelegate, style='Green.TButton', text="Skip & Finish")
        
        # else statement for the logic test to display the 'Quit' and 'Skip' buttons for questions in the test albeit the last question
        else:
            home_btn = Button(self.appdelegate, text="Quit")
            next_btn = Button(self.appdelegate, text="Skip")
        # home button command to sent the user to quit the test
        home_btn['command'] = lambda: self.appdelegate.continuity_handler.quit()
        # next button command to sent the user to the next question
        next_btn['command'] = lambda: self.appdelegate.continuity_handler.skip(skip_tuple())
        
        # renders items to screen
        description_lbl.grid(row=0, column=0, columnspan=4, pady=[20,0])
        self.canvas.grid(row=1, column=0, columnspan=4, pady=[60,20])
        question_lbl.grid(row=2, column=0, columnspan=4, pady=[0])

        # positioning of the four answer buttons
        answer_one_btn.grid(row=3, column=1, pady=[5, 0], sticky="se")
        answer_two_btn.grid(row=3, column=2, pady=[5, 0], padx=[5, 0], sticky="sw")
        answer_three_btn.grid(row=4, column=1, pady=[5, 0], sticky="ne")
        answer_four_btn.grid(row=4, column=2, pady=[5, 0], padx=[5, 0], sticky="nw")

        self.appdelegate.grid_columnconfigure(1, weight=1)
        self.appdelegate.grid_columnconfigure(2, weight=1)

        # positioning of the home and next navigational buttons
        home_btn.grid(row=5, column=0, pady=[5,30], sticky=S)
        next_btn.grid(row=5, column=3, pady=[5,30], sticky=S)
    
    """
    "" @name: Verbal Question
    "" @author: Matthew Thompson
    "" @description: Method to display verbal type questions
    "" @prams: Is first, Is last
    "" @return: none
    """

    def verbalQuestion(self, isFirst=0, isLast=0):

        """
        "" @name: Answer
        "" @author: Matthew Thompson
        "" @description: 
        "" @prams: 
        "" @return: 
        """ 

        def answer(index):
             # Checks to see if the answer chosen is correct based on what question it is
            self.appdelegate.continuity_handler.answer(question['question'], question['answers'][index], question['answers'][question['correct']])

        """
        "" @name: Skip Tupe
        "" @author: Matthew Thompson
        "" @description: Method to create tuple to pass data to continuity handler
        "" @prams: None
        "" @return: Void
        """

        def skip_tuple():
            #Skips the question and inputs an incorrect answer
            return dict({'correct_answer': question['answers'][question['correct']], 'question': question['question']})  
        
        self.appdelegate.flush_ui()
        self.appdelegate.overlay_user_profile()
        # Configures the rows where the ui should be
        self.appdelegate.grid_rowconfigure(4, weight=0)
        self.appdelegate.grid_rowconfigure(5, weight=100)
        # Checks if the question is practice and then sets it to verbal question, else does a random choice question
        if self.isPractice: 
            question = self.verbal_reasoning[3]
        else:
            question = random.choice([n for n in self.verbal_reasoning[:3] if n not in self.complement])
        
        self.complement.append(question)
        # Sets the answer to the question
        answers = question['answers']
        # Sets the description text to the question
        description_text = question['question']
        # Sets the background, text size, border, width and other sizes of the description label
        description_lbl = Label(self.appdelegate, background="#ECF0F1", text = description_text, border=6, width=70, wraplength=500,anchor=CENTER, justify=CENTER)

        if self.appdelegate.isWindows:
            #sets wrap length if platform is windows
            description_lbl.config(wraplength=400)

        # Set the style of the answer buttons and adds the buttons to the frame
        answer_one_btn = Button(self.appdelegate, style="Wide.TButton", text = answers[0])
        answer_one_btn['command'] = lambda: answer(0)

        answer_two_btn = Button(self.appdelegate, style="Wide.TButton", text = answers[1])
        answer_two_btn['command'] = lambda: answer(1)

        answer_three_btn = Button(self.appdelegate, style="Wide.TButton", text = answers[2])
        answer_three_btn['command'] = lambda: answer(2)

        answer_four_btn = Button(self.appdelegate, style="Wide.TButton", text = answers[3])
        answer_four_btn['command'] = lambda: answer(3)


        if self.isLast:
            # If the test is on the last question it shows the Home button
            home_btn = Button(self.appdelegate, text="Home")
            home_btn['command'] = lambda: self.appdelegate.landing_page.draw()
            # If the test is on the last question it shows the Skip & Finish button
            next_btn = Button(self.appdelegate, style='Green.TButton', text="Skip & Finish")
            next_btn['command'] = lambda: self.appdelegate.continuity_handler.skip(skip_tuple())
        else:
            # If the test is on any other question other than the last it shows the quit button instead of the home button
            home_btn = Button(self.appdelegate, text="Quit")
            home_btn['command'] = self.appdelegate.continuity_handler.quit
            # If the test is on any other question other than the last it shows the Skip button instead of the Skip & Finish button
            next_btn = Button(self.appdelegate, text="Skip")
            next_btn['command'] = lambda: self.appdelegate.continuity_handler.skip(skip_tuple())

        # Sets the layout to the correct column
        self.appdelegate.grid_columnconfigure(0, weight=1)
        self.appdelegate.grid_columnconfigure(1, weight=1)
        self.appdelegate.grid_columnconfigure(2, weight=1)
        self.appdelegate.grid_columnconfigure(3, weight=1)
        # Sets the column and columnspan of the description grid
        description_lbl.grid(row=0, column=1, columnspan= 2, pady=[260,0])

        # Sets the column and columnspan of the description grid
        answer_one_btn.grid(row=1, column=1, columnspan=2,pady=[5,0])
        answer_two_btn.grid(row=2, column=1, columnspan=2, pady=[5,0])
        answer_three_btn.grid(row=3, column=1, columnspan=2,pady=[5,0])    
        answer_four_btn.grid(row=4, column=1, columnspan=2,pady=[5,0])
        # Sets the column and columnspan of the buttons
        home_btn.grid(row=5, column=0, pady=[5,30], sticky=SW)
        next_btn.grid(row=5, column=3, pady=[5,30], sticky=SE)


    """
    "" @name: Results
    "" @author: Matthew Thompson
    "" @description: Method to display test results
    "" @prams: textual type of test, questions
    "" @return: Void
    """        

    def results(self, questions, textual_type):

        def _on_mousewheel(event):
            # Catch OS compaibility errors from yview_scroll method
            try: 
                self.canvas.yview_scroll(-1*(event.delta), "units")
            except:
                # cleanly handle error
                print "Scroll OS interoperability error, trying `-1*(event.delta)` - units."

        # Clear GUI
        self.appdelegate.flush_ui()
        # Create canvas
        self.canvas = Canvas(self.appdelegate, bg='#ECF0F1', width=1024, height=800, bd=0, highlightthickness=0)
        # Creates vertical scrollbar
        self.vbar = Scrollbar(self.appdelegate, orient=VERTICAL)
        # Link canvas to scrollbar
        self.vbar.config(command=self.canvas.yview)
        #Sets where the scrollbar is placed
        self.vbar.pack(side=RIGHT,fill=Y)
        # Pack canvas into the page 
        self.canvas.pack(side = LEFT)
        # Link scrollbar
        self.canvas.config(yscrollcommand=self.vbar.set)
        # Configure scrollable area
        self.canvas.config(scrollregion=(0,0, 1024, 2000))

        # Bind mouse scroll
        self.canvas.bind_all("<MouseWheel>", _on_mousewheel)
        
        # Set a row height 
        row = 160
        # Vertical offset
        x = 120
        # Horizontal offset
        y = 0

        # Create results label
        self.canvas.create_text(y + 170, x + 40, text="Results", anchor="nw",font=("Helvetica",self.appdelegate.font_size_for_os(40)), fill="#2c3e50", activefill="#2c3e50")
            
        # Increment vertical offset
        x += 100
        # Clear question index
        i=0
        # Loop over questions
        for question in questions:
            # Increment question index
            i += 1
            # question label
            t = self.canvas.create_text(y + 175, x + 40, text=question['question'], width=800, anchor="nw",font=("Helvetica",self.appdelegate.font_size_for_os(15)), fill="#2c3e50", activefill="#2c3e50")
            # question level bounding box
            b = self.canvas.bbox(t)
            # Add height of label to vertical offset
            x += int(b[3]) - int(b[1])
            # Default Fill Colours
            fill = "#1abc9c"
            activefill = "#16a085"
            # If the answer was incorrect
            if question['answer'] != question['correct_answer']:
                # Error Fill Colours
                fill = "#EC6363"
                activefill = "#c0392b"

            # Question Index label
            self.canvas.create_text(y + 45, x , text="%d." % i, anchor="nw",font=("Helvetica",self.appdelegate.font_size_for_os(100)), fill=fill, activefill=activefill)
            # Answer title 
            self.canvas.create_text(y + 175, x + 45, text="Answer:", width=800, anchor="nw",font=("Helvetica",self.appdelegate.font_size_for_os(15), "bold"), fill="#2c3e50", activefill="#2c3e50")
            # user answer label
            self.canvas.create_text(y + 240, x + 45, text=question['answer'], width=800, anchor="nw",font=("Helvetica",self.appdelegate.font_size_for_os(15)), fill="#2c3e50", activefill="#2c3e50")
            # Correct answer title label
            self.canvas.create_text(y + 175, x + 65, text="Correct Answer:", width=800, anchor="nw",font=("Helvetica",self.appdelegate.font_size_for_os(15), "bold"), fill="#2c3e50", activefill="#2c3e50")
            # Correct answer label
            self.canvas.create_text(y + 297, x + 65, text=question['correct_answer'], width=800, anchor="nw",font=("Helvetica",self.appdelegate.font_size_for_os(15)), fill="#2c3e50", activefill="#2c3e50")
            # Increment vertical hieght by the given local row height 
            x += row

        # Create home button
        home_btn = Button(self.appdelegate, text="Home")
        home_btn['command'] = lambda: self.appdelegate.landing_page.draw()
        self.canvas.create_window(0, max(738, x + 50), anchor=NW, window=home_btn) # 800 - button = 758

        # Configure canvas height 
        self.canvas.config(height=800)
        # Scroll Region
        self.canvas.config(scrollregion=(0,0,1024,x + 110))

