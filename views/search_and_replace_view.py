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

class SearchAndReplaceWindow(TkinterDnD.Tk):
   
    def __init__(self, controller, conf):
        dirname = os.path.dirname(os.path.realpath(__file__))
        super().__init__()

        self.conf = conf
        self.search_window = None
        self.search_param = None

 

 
    def always_on_top(self, topmost):

        #Make the window jump above all
        self.attributes('-topmost',topmost)


 
    
 

    def on_close_search_window(self):
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