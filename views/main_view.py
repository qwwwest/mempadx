# views/main_view.py
import tkinter as tk
from tkinter import ttk
from views.menu_view import MenuView
from views.toolbar_view import ToolbarView
from views.treeview_view import TreeView
from views.textarea_view import TextAreaView
from views.footer_view import FooterView
from tkinterdnd2 import DND_FILES, TkinterDnD
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
        
    
 

    def on_close_search_window(self):
        # Implement the data cleanup logic here
        self.search_window.destroy()
        self.search_window = None
        self.treeview.remove_treeview_item_color()
        self.textarea.highlight_text(None,None)
        Beep.dispatch('on_close_search_window')


    def open_search_window(self, controller):

        # to ensure we open it only one instance
        if self.search_window:
            self.search_window.lift()
            return

        self.search_window = tk.Toplevel(self)
        
        self.search_window.attributes('-topmost', True)

        self.search_window.protocol("WM_DELETE_WINDOW", self.on_close_search_window)  # Bind the cleanup method


        self.search_window.title("Search")
        
        options_frame = ttk.Frame(self.search_window)
        options_frame.pack(fill='x', padx=10, pady=5)

        self.search_param
        self.match_case_var = tk.BooleanVar()
        self.whole_word_var = tk.BooleanVar()
        self.regex_mode_var = tk.BooleanVar()
        self.from_top_var = tk.BooleanVar()
        # self.from_top_var = tk.BooleanVar()
        self.replace_var = tk.BooleanVar()

        ttk.Checkbutton(options_frame, text="Match case", variable=self.match_case_var).grid(row=0, column=0, sticky='w')
        ttk.Checkbutton(options_frame, text="Whole word", variable=self.whole_word_var).grid(row=0, column=1, sticky='w')
       # ttk.Checkbutton(options_frame, text="Regex Mode", variable=self.regex_mode_var).grid(row=0, column=2, sticky='w')
        ttk.Checkbutton(options_frame, text="From Top", variable=self.from_top_var).grid(row=0, column=3, sticky='w')
        # ttk.Checkbutton(options_frame, text="Within Node", variable=self.from_top_var).grid(row=0, column=4, sticky='w')
        ttk.Checkbutton(options_frame, text="Replace", variable=self.replace_var, command=self.toggle_replace).grid(row=0, column=5, sticky='w')

        find_frame = ttk.Frame(self.search_window)
        find_frame.pack(fill='x', padx=10, pady=5)

        ttk.Label(find_frame, text="Find:").pack(side='left')
        self.find_entry = ttk.Entry(find_frame)
        self.find_entry.pack(side='left', fill='x', expand=True, padx=5)
        self.find_entry.focus_set()  # Set focus to the find_entry field

        button_frame = ttk.Frame(self.search_window)
        button_frame.pack(fill='x', padx=10, pady=5)

        # search_text, match_case, whole_word, regex_mode, from_top, search_forward
        ttk.Button(button_frame, text="Previous", command=lambda: controller.search_text(self.find_entry.get(), self.match_case_var.get(), self.whole_word_var.get(), self.regex_mode_var.get(),self.from_top_var.get(), False)).pack(side='left',padx=(0, 5))
         
        # search_text, match_case, whole_word, regex_mode, from_top, search_forward
        ttk.Button(button_frame, text="Next", command=lambda: controller.search_text(self.find_entry.get(), self.match_case_var.get(), self.whole_word_var.get(), self.regex_mode_var.get(), self.from_top_var.get(), True)).pack(side='left', padx=(5, 0))

        self.results_label = ttk.Label(button_frame, text="Results: 0")
        self.results_label.pack(side='left', padx=(10, 0))


        self.replace_frame = ttk.Frame(self.search_window)
        self.replace_frame.pack(fill='x', padx=10, pady=5)
        self.replace_frame.pack_forget()  # Hide the replace frame initially

        ttk.Label(self.replace_frame, text="With:").pack(side='left')
        self.replace_entry = ttk.Entry(self.replace_frame)
        self.replace_entry.pack(side='left', fill='x', expand=True, padx=5)

        self.replace_button = ttk.Button(self.replace_frame, text="Replace", command=lambda: controller.replace_text(self.find_entry.get(), self.replace_entry.get(), self.match_case_var.get(), self.whole_word_var.get(), self.regex_mode_var.get()))


        self.replace_button.pack(side='left')
        self.replace_button["state"] = "disabled"

    def toggle_replace(self):
        if self.replace_var.get():
            self.replace_frame.pack(fill='x', padx=10, pady=5)
        else:
            self.replace_frame.pack_forget()

    def update_results_label(self, count, num_res):
        if count == 0 and  num_res == 0 : 
             self.results_label.config(text=f"No result")
        elif count == 0 :
            self.results_label.config(text=f"Results: {num_res}")
        else:
            self.results_label.config(text=f"Results: {count} / {num_res}")