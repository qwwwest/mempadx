import tkinter as tk
from tkinter import ttk
import os

class View:
    def __init__(self, root):
        self.root = root
        
        self.label = tk.Label(root, text="")
        self.label.pack()

        self.entry = tk.Entry(root)
        self.entry.pack()

        self.button = tk.Button(root, text="Update")
        self.button.pack()
     
        # Creating object of photoimage class for window icons
        dirname = os.path.dirname(os.path.realpath(__file__))
        self.ikon = tk.PhotoImage(file = dirname + '/assets/python.png') 

        # Setting icon of master window 
        self.root.iconphoto(False, self.ikon) 
        self.root.title('MemPad')
        # window.geometry('800x600')
        self.root.config(width=800, height=600)
        self.root.minsize(640,480)
        # Create a button inside the main window that
        # invokes the open_secondary_window() function
        # when pressed.
        button_open = tk.Button(
            self.root,
            text="Open secondary window",
            command= self.open_secondary_window
        )

        button_open.place(x=100, y=100)

        treeview = ttk.Treeview()
        treeview.insert("", tk.END, text="Item 1")
        treeview.pack()


    def open_secondary_window(self):
        # Create secondary (or popup) window.
        secondary_window = tk.Toplevel()
        secondary_window.title("Secondary Window")
        # Setting icon of master window 
        secondary_window.iconphoto(False, self.ikon) 
        secondary_window.config(width=300, height=200)
        # Create a button to close (destroy) this window.
        button_close = tk.Button(
            secondary_window,
            text="Close window",
            command=secondary_window.destroy
        )
        button_close.place(x=75, y=75)

    def set_label_text(self, text):
        self.label.config(text=text)

    def get_entry_text(self):
        return self.entry.get()

    def set_button_command(self, command):
        self.button.config(command=command)
