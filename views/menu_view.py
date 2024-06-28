# views/menu_view.py
import tkinter as tk

class MenuView(tk.Menu):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent

        mempad_menu = tk.Menu(self, tearoff=0)
        file_menu = tk.Menu(self, tearoff=0)
        page_menu = tk.Menu(self, tearoff=0)
        export_menu = tk.Menu(self, tearoff=0)
        settings_menu = tk.Menu(self, tearoff=0)

        for menu in [mempad_menu, file_menu, page_menu, export_menu, settings_menu]:
            for i in range(3):
                menu.add_command(label=f"Item {i+1}")

        self.add_cascade(label="Mempad", menu=mempad_menu)
        self.add_cascade(label="File", menu=file_menu)
        self.add_cascade(label="Page", menu=page_menu)
        self.add_cascade(label="Export", menu=export_menu)
        self.add_cascade(label="Settings", menu=settings_menu)

        self.parent.config(menu=self)
