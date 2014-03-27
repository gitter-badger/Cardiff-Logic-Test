 #!/usr/bin/env python
# encoding: utf-8
# Created by Daniel Koehler - 04/03/2014

from Assets.FlatUI import *
from Application.Database import *
from Application.ContinuityHandler import *
from Interface.Questionnaire import *
from Interface.Admin import *
from Interface.Landing import *
from Interface.Register import *
from Interface.Test import *

from Tkinter import * 
from ttk import *

import platform
import Image
import ImageTk

"""
"" @name: Application Delegate (Class)
"" @author: Daniel Koehler
"" @description: Class the holds compositions of all classes to make them globally accessible 
"" where needed and handles the set up and take down of the application.
"""

class ApplicationDelegate(Frame):

    def __init__(self, parent):
        # Initiate
        Frame.__init__(self, parent)

        # Set a relative path - this supports interoperability between platforms more effectively
        self.relative_path = os.path.normpath(os.path.join(os.path.dirname(__file__)))

        # Instantiate Database Class
        self.db = Database(relative_path = os.path.join(self.relative_path, "Data"))   

        # Store reference to parent.
        self.parent = parent

        # Set up test parameters.
        self.time = 0
        self.network_connection = 0
        self.user_logged_in = 0
        self.user_has_gravatar = 0

        # Set instantiate application classes as compositions of the delegates
        self.continuity_handler = ContinuityHandler(self);
        self.landing_page = LandingPage(self);
        self.register_page = RegisterPage(self);
        self.admin_page = AdminPage(self);
        self.questionnaire = Questionnaire(self);
        self.test = Test(self);

        # Construct some bits
        flatUI = FlatUI()
        self.style = flatUI.initiateWithStyle(Style())  

        # Set default state for operating system
        self.isWindows = False
        # If we're operating on Windows change this value.
        if platform.system() == "Windows":
            self.isWindows = True

        # Start Application
        self.parent.protocol('WM_DELETE_WINDOW', self.quit)
        # Draw landing page
        self.landing_page.draw()

    """
    "" @name: Flush UI
    "" @author: Daniel Koehler
    "" @description: Method to clear the Graphical User Interface of all widgets
    "" @prams: None
    "" @return: Void
    """
    
    def flush_ui(self):
        # Loop over each child in the frame
        for child in self.winfo_children():
            # Delete child widget
            child.destroy()

        # Loop over the first twenty rows and columns
        for i in range(0, 20):
            # Reset weights for columns and rows
            self.grid_rowconfigure(i, weight=0)
            self.grid_columnconfigure(i, weight=0)
            # Set default padding
            self.rowconfigure(i, pad=0)

    """
    "" @name: Overlay User Profile
    "" @author: Daniel Koehler
    "" @description: Overlays user profile
    "" @prams: None
    "" @return: Void
    """

    def overlay_user_profile(self):
        # If the user is logged in and thier profile image was successfuly downloaded
        if self.user_logged_in and self.user_has_gravatar:
            # Load image
            image = Image.open(os.path.join(self.relative_path, 'Assets', 'userprofile.png'))
            # Make it TK compatible
            tk_image = ImageTk.PhotoImage(image)

            # Create TK Button
            profile_image_btn = Button(self, image=tk_image, style="ProfileImage.TLabel")
            # Set image - important!
            profile_image_btn.image = tk_image
            # Place the button using absolute positioning.
            profile_image_btn.place(x=20,y=20)

    """
    "" @name: End Session
    "" @author: Daniel Koehler 
    "" @description: Log out current user 
    "" @prams: None 
    "" @return: Void
    """

    def end_session(self):
        # Clear logged in bool
        self.user_logged_in = 0
        # Clear gratatar bool
        self.user_has_gravatar = 0
        # Re-draw landing page
        self.landing_page.draw()

    """
    "" @name: Quit
    "" @author: Danile Koehler
    "" @description: Method to safely exit the application - saving the database before it exits.
    "" @prams: None
    "" @return: Void
    """ 

    def quit(self):
        # Save database to persistent store
        self.db.deconstruct()
        # Try to delete profile image
        try:
            os.remove(os.path.join(self.relative_path, "Assets", "userprofile.png"))
        except OSError: # An exception will normally only be thrown when this file doesn't exist
            pass # This is not an error we need to handle
        # Close application
        sys.exit()

    """
    "" @name: Font Size for Operating System
    "" @author: Daniel Koehler
    "" @description: Method to correctly scale the font size for given underlaying system.
    "" @prams: None
    "" @return: (Integer) Font Size
    """

    def font_size_for_os(self, size):
        # If the current operation system isn't Windows the configuration is designed for a Retina MacBook.
        if not self.isWindows:
            return size 
        else:
        # Windows need the sizing to be about 70%
            return int(size * 0.7)

root = Tk()
root.geometry("1024x800")
root.minsize(1024,800)
root.maxsize(1024,800)

app = ApplicationDelegate(root)
root.mainloop() 
