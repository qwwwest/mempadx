# views/menu_view.py
import tkinter as tk
from tkinter import ttk, filedialog
from beep import Beep


class MenuView(tk.Menu):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent

       # mempad_menu = tk.Menu(self, tearoff=0)
        file_menu = tk.Menu(self, tearoff=0)
       # page_menu = tk.Menu(self, tearoff=0)
       # export_menu = tk.Menu(self, tearoff=0)
        settings_menu = tk.Menu(self, tearoff=0)

        # for menu in [mempad_menu, file_menu, page_menu, export_menu, settings_menu]:
        #     for i in range(3):
        #         menu.add_command(label=f"Item {i+1}")

        # self.add_cascade(label="Mempad", menu=mempad_menu)

        file_menu.add_command(label="Open", accelerator="Ctrl+O",command=self.open_file_dialog)
        file_menu.add_command(label="New", accelerator="Ctrl+N",command=self.open_file_dialog)
        file_menu.add_command(label="Save", accelerator="Ctrl+S",command=lambda: self.dispatch('command', 'save'))
        file_menu.add_command(label="Save as...", accelerator="Ctrl+Shift+S", command=lambda: self.dispatch('command', 'save_as'))
        file_menu.add_command(label="Close", command=lambda: self.dispatch('command', 'close'))

        file_menu.add_separator()
        file_menu.add_command(label="Exit",accelerator="ESC", command= lambda: self.dispatch('command', 'exit') )
 

        self.add_cascade(label="File", menu=file_menu)

        exit_on_esc = tk.BooleanVar()
        settings_menu.add_checkbutton(
            label="Exit on ESC", 
            command=lambda: self.dispatch('command', 'settings','exit_on_esc', exit_on_esc),
            variable=exit_on_esc
        )
        auto_save = tk.BooleanVar()
        settings_menu.add_checkbutton(
            label="Auto Save", 
            command=lambda: self.dispatch('command', 'settings','auto_save', exit_on_esc),
            variable=auto_save
        )
        always_on_top = tk.BooleanVar()
        settings_menu.add_checkbutton(
            label="Always on top", 
            command=lambda: self.dispatch('command', 'settings','always_on_top', exit_on_esc),
            variable=always_on_top
        )


        theme_menu = tk.Menu(self, tearoff=False)
        theme = tk.IntVar()
        theme.set(1)  # Default theme ("Light".)
        theme_menu.add_radiobutton(
            label="Light",
            variable=theme,
            value=1,
            command=lambda: self.dispatch('command', 'settings','theme_changed', 1),
        )
        theme_menu.add_radiobutton(
            label="Dark",
            value=2,
            variable=theme,
            command=lambda: self.dispatch('command', 'settings','theme_changed', 2),
            
        )
        settings_menu.add_cascade(menu=theme_menu, label="Theme")

        self.add_cascade(label="Settings", menu=settings_menu)

        # self.add_cascade(label="Page", menu=page_menu)
        # self.add_cascade(label="Export", menu=export_menu)
        # self.add_cascade(label="Settings", menu=settings_menu)

        self.parent.config(menu=self)

    def open_file_dialog(self):
        file_path = filedialog.askopenfilename()
        if file_path:
            Beep.dispatch('command','open_mempad_file', file_path)

    def dispatch(self, *args):
        Beep.dispatch('command', *args)
