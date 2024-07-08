# views/main_view.py
import tkinter as tk
from tkinter import ttk
from views.menu_view import MenuView
from views.toolbar_view import ToolbarView
from views.treeview_view import TreeView
from views.textarea_view import TextAreaView
from views.footer_view import FooterView
from tkinterdnd2 import DND_FILES, TkinterDnD
import os

class MainView(TkinterDnD.Tk):
   
    def __init__(self, controller, conf):
        dirname = os.path.dirname(os.path.realpath(__file__))
        super().__init__()

        self.conf = conf
 

        # Creating object of photoimage class for window icons
        
        parentdir = os.path.dirname(dirname)
        self.ikon = tk.PhotoImage(file = parentdir + '/ressources/python.png') 

        #self.model = model    
        self.title("MemPad")

        # Setting icon of master window 
        self.iconphoto(False, self.ikon) 


        WinWidth = self.conf.getint('Main', 'WinWidth')
        WinHeight = self.conf.getint('Main', 'WinHeight')
        winX = self.conf.getint('Main','winX')
        winY = self.conf.getint('Main','winY')

        self.minsize(480,320)
 
        # width of the screen
        screenwidth = self.winfo_screenwidth() 
        # height of the screen
        screenheight = self.winfo_screenheight() 
        
        # print(f"{WinWidth}x{WinHeight}+{winX}+{winY} {WinWidth + winX}>{screenwidth} OR {WinWidth + winY}>{hs}")

        if WinWidth + winX > screenwidth or WinHeight + winY > screenheight:
            geom ="640x480+0+0"
        else:    
            geom = f"{WinWidth}x{WinHeight}+{winX}+{winY}"
        
        print(geom)
        self.geometry(geom)
        self.menu = MenuView(self)

       #  self.toolbar = ToolbarView(self)
      #  self.toolbar.pack(side=tk.TOP, fill=tk.X)

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

        
        #Make the window jump above all
        # self.attributes('-topmost',True)

        self.bind("<Configure>", self.on_window_resize)
 


    def on_window_resize(self, event):
        widget =  str(event.widget)

        # only main window
        if widget != '.':
           return
        
        # if (self.width == event.width and
        #     self.height == event.height):
        #     return
 
        self.width = event.width
        self.height = event.height
 
        self.conf.set('Main', 'WinWidth', str(event.width))
        self.conf.set('Main', 'WinHeight',str(event.height))
        self.conf.set('Main', 'winX', str(self.winfo_x()))
        self.conf.set('Main', 'winY', str(self.winfo_y()))
 
        fh = self.footer.label.winfo_height()
        self.paned_window.winfo_height
    
 
