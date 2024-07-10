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


        winWidth = self.conf.getint('Main', 'WinWidth')
        winHeight = self.conf.getint('Main', 'WinHeight') + 20
        winX = self.conf.getint('Main','winX')
        winY = self.conf.getint('Main','winY')
        iwidth = self.conf.getint('Main','Iwidth')


        self.minsize(480,320)
 
        screenwidth = self.winfo_screenwidth() 
        screenheight = self.winfo_screenheight() 

        if winWidth + winX > screenwidth or winHeight + winY > screenheight:
            geom ="640x480+0+0"
        else:    
            geom = f"{winWidth}x{winHeight}+{winX}+{winY}"
 
        self.geometry(geom)
        # self.attributes('-fullscreen', True)
        # self.state('zoomed') 
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
        #self.paned_window.add(self.treeview, stretch="always")
        self.paned_window.add(self.treeview, width=iwidth)

        # self.after(50, lambda: self.win.sashpos(0, position))

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

        
        if widget == '.':
 
    
            self.width = winWidth = event.width
            self.height = winHeight = event.height 
            winX, winY = self.winfo_x(), self.winfo_y()
 

            self.conf.set('Main', 'WinWidth', str(winWidth))
            self.conf.set('Main', 'WinHeight',str(winHeight))
            self.conf.set('Main', 'winX', str(winX))
            self.conf.set('Main', 'winY', str(winY))
 
            self.footer.label['text'] = f"X={winX}, Y={winY} Window: {winWidth}x{winHeight} [{self.winfo_screenwidth()}x{self.winfo_screenheight() }]"
            return
        
        if widget == '.!panedwindow.!treeview':
          
            self.conf.set('Main', 'Iwidth', str( event.width))
            return
        
    
 
