#!/usr/bin/env python
# encoding: utf-8
# Created by Daniel Koehler - 15/03/2014

from Tkinter import *
from ttk import *

import math
import platform
import threading, Queue, time

class Chart():
    def __init__(self, canvas):
        self.canvas = canvas

    """
    "" @name: Doughnut
    "" @author: Daniel Koehler
    "" @description: Method to render doughnut charts
    "" @prams: (Interger) Font Size, (String) centre, (Interger) Origin X, (Interger) Origin Y, (Interger) Size, (Interger) Outer Width, (List) Colour, data = [1,1,1,1], label = [], lastend = 0
    "" @return: 
    """

    def doughnut(self, font_size = 10, centre="", origin_x = 100, origin_y = 100, size = 200, outer_width = 20, colour = ["#1abc9c","#16a085","#2ecc71", "#27ae60", "#3498db", "#2980b9", "#9b59b6","#8e44ad","#e74c3c","#c0392b","#e67e22","#d35400"], data = [1,1,1,1], label = [], lastend = 0):

        """
        "" @name: Doughnut -> Show Popover
        "" @description: Method to show segment specific label
        "" @prams: None 
        "" @return: Void
        """
        
        def show_popover(event):
            # Get canvas that imitated the event - the should be equivalent to "self.canvas".
            canvas = event.widget
            # Get absolute coordinates from relative event coordinates.
            x = canvas.canvasx(event.x)
            y = canvas.canvasy(event.y)

            # Find the item ID of the object that caused the event to be fired.
            item = canvas.find_closest(x, y)[0]

            # Create new centre cover
            self.canvas.create_oval(origin_x + outer_width, origin_y + outer_width, origin_x + size - outer_width, origin_y + size - outer_width, fill="#ECF0F1", outline="#ECF0F1",  tags=("hide_popover","remove_for_move_two", "remove_for_move_one")) # Centre Cover
            # Create popover text
            self.result_text = self.canvas.create_text(origin_x + size / 2, origin_y + size / 2, text=self.canvas.gettags(item)[1],font=("Helvetica",font_size, "bold"),fill="#2c3e50", activefill="#2c3e50", tags=("hide_popover","remove_for_move_two", "remove_for_move_one"))
        
        """
        "" @name: Doughnut -> Hide Popover
        "" @description: Method hide segment specific label and show default centre text.
        "" @prams: None 
        "" @return: Void
        """

        def hide_popover(event):
            # Delete all items with tag hide_popover namely the added centre cover and text
            self.canvas.delete("hide_popover")

        """
        "" @name: Doughnut -> Animate Chart
        "" @description: Method to perform the animating out effect.
        "" @prams: None 
        "" @return: Void
        """

        def animate_chart():
            # Clear variable N
            n = 0
            # Draw a masking ARC of full exstent (360 degress) to cover all elements in the chart
            arc = self.canvas.create_arc(origin_x - 1, origin_y - 1, origin_x + size + 1, origin_y + size + 1,width=0, style=PIESLICE,  start=0, extent=360, fill="#ECF0F1", outline="#ECF0F1", tags=("remove_for_move_two", "remove_for_move_one"))   
            # Show reduce the exstent of this arc in a while loop.
            while 1:
                # Increment N a little
                n += 0.025
                # Calculate Y for X (n) at present this curve simply grows at N squared.
                y = n * n
                if n*n >= 1:
                    # Once animation is finished, lets delete the arc.
                    self.canvas.delete(arc)
                    break
                # Configure the masking ARC.
                self.canvas.itemconfig(arc, extent=min(360 - (360.0*y), 360))
                # Sleep for a nominal time that the animation might look clean.
                time.sleep(.0001)

            # Draw center text title
            self.canvas.create_text(origin_x + size / 2, origin_y + size / 2 - 20 / 2, text="You might like to study...",font=("Helvetica",font_size, "bold"),fill="#2c3e50", activefill="#2c3e50", tags=("remove_for_move_two", "remove_for_move_one"))
            # Draw center text
            self.canvas.create_text(origin_x + size / 2, origin_y + size / 2 + 20 / 2, text=centre, font=("Helvetica",font_size, "bold"),fill="#2c3e50", activefill="#2c3e50", tags=("remove_for_move_two", "remove_for_move_one"))

        
        # For each index in data.
        for i in range(len(data)):
            # If the segment actually carries weight - e.g. it's a valid percentage of the chart.
            if data[i] > 0:   
                # get the RGB colour
                rgb = colour[i].strip("#")
                # The amount to increment the colour components by
                light_factor = 20
                # This is a bit messy but basically it takes the Red Green and Blue Components and increments it by "light_factor" to create the `onhover` colour. 
                activefill = "#" + "".join([("%0.2X" % (max(int(rgb[y:y+2], 16) + light_factor, 1))) for y in range(0, len(rgb), 2)])

                # Create the segment of the chart from `lastend` as a function of the faction of the segment in the sum of the data array time PI*2 converted to degrees.
                item = self.canvas.create_arc(origin_x, origin_y, origin_x + size, origin_y + size,tag=("popover", "%s - %s%%" % (label[i], int(float(data[i]) / sum(data) * 100)), "remove_for_move_two", "remove_for_move_one"), width=0, style=PIESLICE,  start=lastend, extent=math.degrees(math.pi * 2 * (float(data[i]) / sum(data))), fill=colour[i], outline=colour[i], activeoutline=activefill, activefill=activefill)
                # Store the endpoint of the last segment so that on the next iterarion the above draws from that point for the calculated exstent.
                lastend += math.degrees(math.pi * 2 * (float(data[i]) / sum(data))) #extent
                
                # Bind the `hoverover` and `hoverout` events to thier handlers 
                self.canvas.tag_bind("popover","<Enter>", show_popover)
                self.canvas.tag_bind("popover","<Leave>", hide_popover)
            
        # Create Oval to Mask Centre of Chart. 
        self.canvas.create_oval(origin_x + outer_width, origin_y + outer_width, origin_x + size - outer_width, origin_y + size - outer_width, fill="#ECF0F1", outline="#ECF0F1", tags=("remove_for_move_two", "remove_for_move_one")) 
        
        # If we're working with windows, don't try to animate chart.
        if platform.system() == "Windows":
            # Windows - Draw Center Text
            self.canvas.create_text(origin_x + size / 2, origin_y + size / 2 - 20 / 2, text="You might like to study...",font=("Helvetica",font_size, "bold"),fill="#2c3e50", activefill="#2c3e50", tags=("remove_for_move_two", "remove_for_move_one"))
            self.canvas.create_text(origin_x + size / 2, origin_y + size / 2 + 20 / 2, text=centre, font=("Helvetica",font_size, "bold"),fill="#2c3e50", activefill="#2c3e50", tags=("remove_for_move_two", "remove_for_move_one"))
        else:
            # Otherwise, we must be working with a real OS so lets make it look lovely.
            animate_chart_thread = threading.Thread(target=animate_chart)
            animate_chart_thread.daemon = True
            animate_chart_thread.start()

        
