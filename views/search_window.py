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

class SearchWindow(tk.Toplevel):

    def __init__(self, parent, pos_x, pos_y, last_params):
        super().__init__(parent)
        self.parent = parent
        self.search_param = None
        
        self.pos_x = pos_x
        self.pos_y = pos_y
        if last_params :
            self.last_params = last_params
        else:
            # (search_term, match_case, whole_word, regex_mode, from_top, replace)
            self.last_params = ("", False, False, False, False, False)



        self.create_widgets()

    def create_widgets(self):

        # self.search_window = tk.Toplevel(self)
       
        self.attributes('-topmost', True)

        self.protocol("WM_DELETE_WINDOW", self.on_close_search_window)  # Bind the cleanup method

        self.title("Search & Replace")
        
        options_frame = ttk.Frame(self)
        options_frame.pack(fill='x', padx=10, pady=5)

        (search_term, match_case, whole_word, regex_mode, from_top, replace) = self.last_params
        self.match_case_var = tk.BooleanVar(value=match_case)
        self.whole_word_var = tk.BooleanVar(value=whole_word)
        self.regex_mode_var = tk.BooleanVar()
        self.from_top_var = tk.BooleanVar(value=from_top)
        # self.from_top_var = tk.BooleanVar()
        self.replace_var = tk.BooleanVar(value=replace)   

        ttk.Checkbutton(options_frame, text="Match case", variable=self.match_case_var).grid(row=0, column=0, sticky='w')
        ttk.Checkbutton(options_frame, text="Whole word", variable=self.whole_word_var).grid(row=0, column=1, sticky='w')
       # ttk.Checkbutton(options_frame, text="Regex Mode", variable=self.regex_mode_var).grid(row=0, column=2, sticky='w')
        ttk.Checkbutton(options_frame, text="From Top", variable=self.from_top_var).grid(row=0, column=3, sticky='w')
        # ttk.Checkbutton(options_frame, text="Within Node", variable=self.from_top_var).grid(row=0, column=4, sticky='w')
        ttk.Checkbutton(options_frame, text="Replace", variable=self.replace_var, command=self.toggle_replace).grid(row=0, column=5, sticky='w')

        find_frame = ttk.Frame(self)
        find_frame.pack(fill='x', padx=10, pady=5)

        ttk.Label(find_frame, text="Find:").pack(side='left')
        self.find_entry = ttk.Entry(find_frame)
        self.find_entry.pack(side='left', fill='x', expand=True, padx=5)
        self.find_entry.insert(0, search_term) 
        self.find_entry.focus_set()  # Set focus to the find_entry field

        button_frame = ttk.Frame(self)
        button_frame.pack(fill='x', padx=10, pady=5)

        # search_text, match_case, whole_word, regex_mode, from_top, search_forward
        ttk.Button(button_frame, text="Previous", command=lambda: Beep.dispatch('search_text',self.find_entry.get(), self.match_case_var.get(), self.whole_word_var.get(), self.regex_mode_var.get(),self.from_top_var.get(),self.replace_var.get(), False)).pack(side='left',padx=(0, 5))
         
        # search_text, match_case, whole_word, regex_mode, from_top, search_forward
        ttk.Button(button_frame, text="Next", command=lambda: Beep.dispatch('search_text',self.find_entry.get(), self.match_case_var.get(), self.whole_word_var.get(), self.regex_mode_var.get(), self.from_top_var.get(),self.replace_var.get(), True)).pack(side='left', padx=(5, 0))

        self.results_label = ttk.Label(button_frame, text="Results: 0")
        self.results_label.pack(side='left', padx=(10, 0))


        self.replace_frame = ttk.Frame(self)
        self.replace_frame.pack(fill='x', padx=10, pady=5)
        self.replace_frame.pack_forget()  # Hide the replace frame initially

        ttk.Label(self.replace_frame, text="With:").pack(side='left')
        self.replace_entry = ttk.Entry(self.replace_frame)
        self.replace_entry.pack(side='left', fill='x', expand=True, padx=5)

        self.replace_button = ttk.Button(self.replace_frame, text="Replace", command=lambda: Beep.dispatch('replace_text',self.find_entry.get(), self.replace_entry.get() ))


        self.replace_button.pack(side='left')
        self.replace_button["state"] = "disabled"

        geom = f"+{self.pos_x}+{self.pos_y}"
 
        self.geometry(geom)

        # To make the new Search Window modal
        self.transient(self.parent)
        self.grab_set()

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
 

    def on_close_search_window(self):

        Beep.dispatch('on_close_search_window', self.winfo_x(), self.winfo_y())
        self.grab_release()
        self.destroy() 
