# views/footer_view.py
import tkinter as tk

class FooterView(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent

        self.label = tk.Label(self, text="Page Path: /, Num Pages: 0, Position: 0")
        self.label.pack(fill=tk.X)

 
    def setText(self, text):
        self.label.config(text=text)


 
 