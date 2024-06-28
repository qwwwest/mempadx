# views/toolbar_view.py
import tkinter as tk
from tkinter import ttk

class ToolbarView(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent

        buttons = [
            ("Add Page After", "add_page_after.svg"),
            ("Add Page As Child", "add_page_as_child.svg"),
            ("Cut Page", "cut_page.svg"),
            ("Paste Page", "paste_page.svg"),
            ("Delete Page", "delete_page.svg"),
            ("Save", "save.svg"),
            ("Show Raw/Rendered Text", "show_raw_text.svg"),
        ]

        for text, icon in buttons:
            button = ttk.Button(self, text=text)
            button.pack(side=tk.LEFT, padx=2, pady=2)
              
         
        # self.create_widgets()

    def create_widgets(self):
        add_page_button = tk.Button(self, text="Add Page After", command=lambda: print("Add Page After"))
        add_page_button.pack(side=tk.LEFT, padx=2, pady=2)

        add_child_page_button = tk.Button(self, text="Add Page as Child", command=lambda: print("Add Page as Child"))
        add_child_page_button.pack(side=tk.LEFT, padx=2, pady=2)

        cut_page_button = tk.Button(self, text="Cut Page", command=lambda: print("Cut Page"))
        cut_page_button.pack(side=tk.LEFT, padx=2, pady=2)

        paste_page_button = tk.Button(self, text="Paste Page", command=lambda: print("Paste Page"))
        paste_page_button.pack(side=tk.LEFT, padx=2, pady=2)

        delete_page_button = tk.Button(self, text="Delete Page", command=lambda: print("Delete Page"))
        delete_page_button.pack(side=tk.LEFT, padx=2, pady=2)

        move_up_button = tk.Button(self, text="Move Up", command=lambda: print("Move Up"))
        move_up_button.pack(side=tk.LEFT, padx=2, pady=2)

        # move_down_button = tk.Button(self, text="Move Down", command=lambda: print("Move Down"))
        # move_down_button.pack(side=tk.LEFT, padx=2, pady=2)

        # move_left_button = tk.Button(self, text="Move Left", command=lambda: print("Move Left"))
        # move_left_button.pack(side=tk.LEFT, padx=2, pady=2)

        # move_right_button = tk.Button(self, text="Move Right", command=lambda: print("Move Right"))
        # move_right_button.pack(side=tk.LEFT, padx=2, pady=2)

        save_button = tk.Button(self, text="Save", command=lambda: print("Save"))
        save_button.pack(side=tk.LEFT, padx=2, pady=2)

        toggle_view_button = tk.Button(self, text="Toggle View", command=lambda: print("Toggle View"))
        toggle_view_button.pack(side=tk.LEFT, padx=2, pady=2)