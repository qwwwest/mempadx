# views/textarea_view.py
import tkinter as tk
from tkinter import ttk


class TextAreaView(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.pack(expand=True, fill=tk.BOTH)
        self.text = tk.Text(self, undo=True, font=("monospace", 14), wrap = tk.WORD)

        # Create a vertical scrollbar
        self.scrollbar = ttk.Scrollbar(self, orient=tk.VERTICAL, command=self.text.yview)
        self.text.configure(yscrollcommand=self.scrollbar.set)
        
        # Pack the tree and the scrollbar
        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)


        self.text.pack(expand=True, fill=tk.BOTH)
 
    # using property decorator 
    # a getter function for the content
    @property
    def content(self):
        return self.text.get(1.0, tk.END)
    
    # a setter function for the content
    @content.setter 
    def content(self, content):
        self.text.delete(1.0, tk.END)
        self.text.insert(tk.END, content)

 