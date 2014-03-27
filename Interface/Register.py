#!/usr/bin/env python
# encoding: utf-8
# Created by Ryan Day - 15/03/2014

from Tkinter import *
from ttk import *
import re
import urllib, hashlib, Image
import threading, time
import os

class RegisterPage():
    def __init__(self, appdelegate):
        self.appdelegate = appdelegate
        self.index_match = {}

    """
    "" @name: Create User
    "" @author: Daniel Koehler
    "" @description: Method to insert user into database - This method should be called from a thread as it takes serious time to complete.
    "" @prams: (String) First Name, (String) Surname, (String) Email Address, (Integer) Group ID. 
    "" @return: Void
    """

    def create_user(self, firstName, surname, emailAddress, groupId):

        
        # Varible to contain gravatar image size
        size = 80

        # Query of the database where the email is the same as that used to register 
        self.appdelegate.user_id = self.appdelegate.db.select("user", where="(`email_address` == '%s')" % emailAddress.lower())

        # Create new user from data in passed arguments and assign the insert ID as a property of the AppDelegate Class
        if not self.appdelegate.user_id:
            self.appdelegate.user_id = self.appdelegate.db.insert("user", {
                    'first_name': firstName,
                    'type':'pupil', 
                    'last_name': surname,
                    'email_address': emailAddress.lower(),
                    'group_id': groupId,
                    'added_timestamp':str(time.time())
                    })
       
        # Create the Gravatar URL by MD5ing the email address
        gravatar_url = "http://www.gravatar.com/avatar/" + hashlib.md5(emailAddress.lower()).hexdigest() + ".jpg?"
        gravatar_url += urllib.urlencode({'s':str(size),'d':403})

        # This will throw an exception should the Gravatar url return a 403 or if there is no network connection
        try:    
            # Try to fetch the Image
            urllib.urlretrieve(gravatar_url, os.path.join(self.appdelegate.relative_path, "Assets", "userprofile.jpg"))
            # If the email is associated with Gravitar then the return image will now be in userprofile.jpg so lets open it
            im = Image.open(os.path.join(self.appdelegate.relative_path, "Assets", "userprofile.jpg"))
            # Create a PNG version
            im.save(os.path.join(self.appdelegate.relative_path, "Assets", "userprofile.png"))
            # Remove the JPEG
            os.remove(os.path.join(self.appdelegate.relative_path, "Assets", "userprofile.jpg"))
            # Set property of root class to denote a successful Gravatar image load.
            self.appdelegate.user_has_gravatar = 1
        except:
            print "No network connection/User doesn't have Gravatar."
    
    """
    "" @name: Draw (Register Page)
    "" @author: Ryan Day
    "" @description: Method to draw Register Page
    "" @prams: None 
    "" @return: Void
    """

    def draw(self):

        # Auxiliary storage for PlaceholderManagedEntry widgets
        placeholders = {}

        """
        "" @name: Draw -> Placeholder Managed Entry
        "" @description: Method to add placeholders text input fields
        "" @prams:  
        "" @return:
        """

        def PlaceholderManagedEntry(context, placeholder="", style="InputBorder.TEntry", justify=None, validatecommand=None):
            entry_text = StringVar()
            entry_text.set(placeholder)
            entry = Entry(self.appdelegate, style=style, textvariable=entry_text, justify=justify)            
            entry_text.trace("w", validatecommand)    
            entry.bind("<FocusIn>", remove_placeholder) 
            placeholders[entry._name] = placeholder
            entry.bind("<FocusOut>", replace_placeholder) 
            return entry_text, entry

        """
        "" @name: Draw -> Remove Placeholder
        "" @description: Method to remove placeholders text input fields
        "" @prams:  
        "" @return:
        """

        def remove_placeholder(event):
            if(event.widget.get() == placeholders[event.widget._name] or event.widget.get() == ""):
                event.widget.delete(0, END)

        """
        "" @name: Draw -> Replace Placeholder
        "" @description: Method to add placeholders text input fields when user clicks off field with no input
        "" @prams:  
        "" @return:
        """

        def replace_placeholder(event):
            if(event.widget.get() == placeholders[event.widget._name] or event.widget.get() == ""):
                event.widget.delete(0, END)
                event.widget.insert(0, placeholders[event.widget._name])

        """
        "" @name: Draw -> Validate First Name
        "" @description: Method to validate whether First Name inputted is only letters (both upper and lower case) and is longer than 0 characters
        "" @prams:  
        "" @return: Boolean
        """

        def validate_first_name(*args):
            first_name_text.set(first_name_text.get().title())
            first_name_entry.config(style="InputBorder.TEntry")
            # compares inputted characters with letters and length
            if not re.match(r"^[A-Z][-a-zA-Z]+$", first_name_text.get()) and len(first_name_text.get()) > 0:
                # if input doesn't include only letters or has length 0... 
                if first_name_text.get() != placeholders[first_name_entry._name] or args[0]:
                    # then error is given
                    first_name_entry.config(style="InputBorderError.TEntry")
                    return False
            # if input has only letters and is longer than 0, then Fist Name is accepted
            return True


        """
        "" @name: Draw -> Validate Last Name
        "" @description: Method to validate whether Last Name inputted is only letters (both upper and lower case) and is longer than 0 characters
        "" @prams:  
        "" @return: Boolean
        """

        def validate_last_name(*args):
            last_name_text.set(last_name_text.get().title())
            last_name_entry.config(style="InputBorder.TEntry")
            # compares inputted characters with letters and length
            if not re.match(r"^[A-Z][-a-zA-Z]+$", last_name_text.get()) and len(last_name_text.get()) > 0: 
                # if input doesn't include only letters or has length 0...
                if last_name_text.get() != placeholders[last_name_entry._name] or args[0]:
                    # then error is given
                    last_name_entry.config(style="InputBorderError.TEntry")
                    return False
            # if input has only letters and is longer than 0, then Last Name is accepted
            return True

        """
        "" @name: Draw -> Validate Email Address
        "" @description: Method to validate whether Email Address inputted is anything but "@", followed by "@", followed by ".", followed by anything but "@" and has length greater than 0
        "" @prams:  
        "" @return: Boolean
        """

        def validate_email_address(*args):
            email_address_entry.config(style="InputBorder.TEntry")
            # if input is not : anything but "@", followed by "@", followed by ".", followed by anything but "@" and has length greater than 0...
            if not re.match(r"[^@]+@[^@]+\.[^@]+", email_address_text.get()) and len(email_address_text.get()) > 0: 
                if email_address_text.get() != placeholders[email_address_entry._name] or args[0]:
                    # then error is given
                    email_address_entry.config(style="InputBorderError.TEntry")
                    return False
            # if input has anything but "@", followed by "@", followed by ".", followed by anything but "@" and has length greater than 0, then Email Address is accepted
            return True

        """
        "" @name: Draw -> Validate Group ID
        "" @description: Method to validate whether user has selected a Group ID from Tuple
        "" @prams:  
        "" @return: Boolean
        """

        def validate_group_id(*args):
            # sets background of selected group to hex colour #3498DB
            group_id_entry.config(bg="#3498DB")
            group_id_entry_border.config(style="InputBorder.TFrame")

            # checks whether an index has been selected
            if len(group_id_entry.curselection()) == 0:
                    # if index hasn't been selected then background changes to hex colour #E74C3C
                    group_id_entry.config(bg="#E74C3C")
                    group_id_entry_border.config(style="InputBorderError.TFrame")
                    return False
            # accepts if group has been selected
            return True

        """
        "" @name: Draw -> Pass to User Creation Thread
        "" @description: Passes new user to database
        "" @prams: none
        "" @return: Boolean
        """

        def pass_user_creation_to_thread():
            # if all inputted values are not True
            if not (validate_first_name(True) or validate_last_name(True) or validate_email_address(True) or validate_group_id()):
                return False
            
            try:
                group_id = self.index_match[int(group_id_entry.curselection()[0])]
            except:
                print "Unknown Index Selection Error"
                return False

            # creates user
            self.user_creation_thread = threading.Thread(target=lambda:self.create_user(first_name_text.get(), last_name_text.get(), email_address_text.get(), group_id))
            self.user_creation_thread.daemon = True 
            self.user_creation_thread.start()
            
            # Set the global `user_logged_in` property.
            self.appdelegate.user_logged_in = True
            # Draw the landing page
            self.appdelegate.landing_page.draw()

        # Clean GUI
        self.appdelegate.flush_ui()
        # Change Window Title
        self.appdelegate.parent.title("Signup")
        # Make the Second Column, "1" (Zero Based Index) fill it's avaible space, by setting a weight.
        self.appdelegate.columnconfigure(1, weight=1)

        # Set up the PlaceholderManagedEntrys for First Name, Last Name, and Email Address.
        first_name_text, first_name_entry = PlaceholderManagedEntry(self.appdelegate, placeholder="First Name", style="InputBorder.TEntry", justify=CENTER, validatecommand=validate_first_name)
        last_name_text, last_name_entry = PlaceholderManagedEntry(self.appdelegate, placeholder="Last Name", style="InputBorder.TEntry", justify=CENTER, validatecommand=validate_last_name)
        email_address_text, email_address_entry = PlaceholderManagedEntry(self.appdelegate, placeholder="Email Address", style="InputBorder.TEntry", justify=CENTER, validatecommand=validate_email_address)

        # creates Submit button
        submit_btn = Button(self.appdelegate, text="Submit")
        submit_btn['command'] = pass_user_creation_to_thread
        
        # creates Home button
        home_btn = Button(self.appdelegate, style='Green.TButton', text="Home")
        home_btn['command'] = lambda: self.appdelegate.landing_page.draw()

        # creates text entry locations
        first_name_entry.grid(row=2, column=1, columnspan=2, pady=[300,0])
        last_name_entry.grid(row=3, column=1, columnspan=2, pady=[5,0])
        email_address_entry.grid(row=4, column=1, columnspan=2, pady=[5,5])
        
        group_id_entry_border = Frame(self.appdelegate, style="InputBorder.TFrame")

        # creates List Box for groups with scroll bar
        group_id_entry = Listbox(group_id_entry_border, height=5, bg="#3498DB", foreground="#FFFFFF", highlightthickness=0, bd=0)
        group_id_entry.bind("<<ListboxSelect>>", validate_group_id)
        scrollbar = Scrollbar(group_id_entry_border, command=group_id_entry.yview)
        group_id_entry.configure(yscrollcommand=scrollbar.set)

        # inserts groups into List Box
        i = 0
        for item in sorted(self.appdelegate.db.select("group"), key=lambda k: int(k['group_id']), reverse=True):
            if item['active']:
                self.index_match[i] = item['group_id']
                group_id_entry.insert(END, item['group_name'])
                i += 1

        group_id_entry.pack(side=LEFT, fill=X, padx=3, pady=3)
        
        scrollbar.pack(side=RIGHT,fill=Y)
        group_id_entry_border.grid(row=5, column=1)

        submit_btn.grid(row=6, column=1, columnspan=2, pady=[5,0])
        home_btn.grid(row=7, column=1, columnspan=2, pady=[5,0], sticky=S)

        self.appdelegate.update()

