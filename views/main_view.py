# views/main_view.py
import tkinter as tk
from tkinter import ttk
from views.menu_view import MenuView
from views.toolbar_view import ToolbarView
from views.treeview_view import TreeView
from views.textarea_view import TextAreaView
from views.footer_view import FooterView
import os

 

class MainView(tk.Tk):
   
    def __init__(self, controller):
        dirname = os.path.dirname(os.path.realpath(__file__))
        super().__init__()
 

        # Creating object of photoimage class for window icons
        
        parentdir = os.path.dirname(dirname)
        self.ikon = tk.PhotoImage(file = parentdir + '/ressources/python.png') 

        #self.model = model    
        self.title("MemPad")

        # Setting icon of master window 
        self.iconphoto(False, self.ikon) 

        self.geometry("800x400")
        self.minsize(480,320)
        
        self.menu = MenuView(self)

        self.toolbar = ToolbarView(self)
        self.toolbar.pack(side=tk.TOP, fill=tk.X)

        # Initialize the footer
        self.footer = FooterView(self)
        self.footer.pack(side=tk.BOTTOM, fill=tk.X)

        # Initialize the main frame to hold the treeview and textarea
        self.paned_window = tk.PanedWindow(self, orient=tk.HORIZONTAL)
        self.paned_window.pack(expand=True, fill=tk.BOTH)
        
        # Initialize the treeview
        self.treeview = TreeView(self.paned_window,controller)
        self.paned_window.add(self.treeview, stretch="always")

        # Initialize the text area
        self.textarea = TextAreaView(self.paned_window)
        self.paned_window.add(self.textarea, stretch="always")

        self.width = 0
        self.height = 0
        
        self.bind("<Control-s>", self.save)
        # self.bind("<Configure>", self.on_window_resize)
 


    def on_window_resize(self, event):
        widget =  str(event.widget)

        # only main window
        if widget != '.':
           return
        
        if (self.width == event.width and
            self.height == event.height):
            return
        
        self.width = event.width
        self.height = event.height

        fh = self.footer.label.winfo_height()
        self.paned_window.winfo_height
        print(f"  resized to {event.width}x{event.height}")


    def save(self, event=None):
        self.controller.save()
