# views/main_view.py
import tkinter as tk
from tkinter import ttk
from views.menu_view import MenuView
from views.toolbar_view import ToolbarView
from views.treeview_view import TreeView
from views.textarea_view import TextAreaView
from views.footer_view import FooterView
from tkinterdnd2 import TkinterDnD
import  views.themes.pywinstyles as pywinstyles
import sys

from beep import Beep
import os

class MainView(TkinterDnD.Tk):
   
    def __init__(self, controller, conf):
        dirname = os.path.dirname(os.path.realpath(__file__))

        super().__init__()

        self.conf = conf
        self.search_window = None
        self.search_param = None

        # Creating object of photoimage class for window icons
        parentdir = os.path.dirname(dirname)
        self.ikon = tk.PhotoImage(file = parentdir + '/ressources/python.png') 

        #self.model = model    
        self.title("MemPadX")

        # Setting icon of master window 
        self.iconphoto(False, self.ikon) 

        #color titlebar hack
        
        # Example usage (replace `root` with the reference to your main/Toplevel window)
        self.apply_theme_to_titlebar(self)

        # self.overrideredirect(True)

        winWidth = self.conf.getValue('WinWidth', 'int')
        winHeight = self.conf.getValue('WinHeight', 'int') + 20
        winX = self.conf.getValue('winX', 'int')
        winY = self.conf.getValue('winY', 'int')
        iwidth = self.conf.getValue('Iwidth', 'int')


        self.minsize(480,320)
 
        screenwidth = self.winfo_screenwidth() 
        screenheight = self.winfo_screenheight() 

        if winWidth + winX > screenwidth or winHeight + winY > screenheight:
            geom ="640x480+0+0"
        else:    
            geom = f"{winWidth}x{winHeight}+{winX}+{winY}"
 
        self.geometry(geom)
        # self.attributes('-fullscreen', True)
        self.state('zoomed') 
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
        self.paned_window.add(self.treeview, width=iwidth)


        # Initialize the text area
        self.textarea = TextAreaView(self.paned_window)
        self.paned_window.add(self.textarea, stretch="always")

        self.width = 0
        self.height = 0

        self.always_on_top(self.conf.getValue('OnTop', 'bool'))
       
        self.renderMarkdown = self.conf.getValue('renderMarkdown', 'bool')


        self.bind("<Configure>", self.on_window_resize)
   
 
    def always_on_top(self, topmost):

        #Make the window jump above all
        self.attributes('-topmost',topmost)

    def on_window_resize(self, event):
        widget =  str(event.widget)
        
        if widget == '.':
            self.width = winWidth = event.width
            self.height = winHeight = event.height 
            winX, winY = self.winfo_x(), self.winfo_y()
 
    
            self.conf.setValue('WinWidth', winWidth)
            self.conf.setValue('WinHeight',winHeight)
            self.conf.setValue('winX', winX)
            self.conf.setValue('winY', winY)

            self.footer.label['text'] = f"X={winX}, Y={winY} Window: {winWidth}x{winHeight} [{self.winfo_screenwidth()}x{self.winfo_screenheight() }]"
            return
        
        if widget == '.!panedwindow.!treeview':
          
            self.conf.setValue('Iwidth', event.width)
            return


    def apply_theme_to_titlebar(self, root):

        # if os is not Windows return.
        if not hasattr(sys, 'getwindowsversion'):
            return

        version = sys.getwindowsversion()

        if version.major == 10 and version.build >= 22000:
            # Set the title bar color to the background color on Windows 11 for better appearance
            pywinstyles.change_header_color(root, "#1c1c1c" )
        elif version.major == 10:
            pywinstyles.apply_style(root, "dark" )

            # A hacky way to update the title bar's color on Windows 10 (it doesn't update instantly like on Windows 11)
            root.wm_attributes("-alpha", 0.99)
            root.wm_attributes("-alpha", 1)
