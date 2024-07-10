# views/menu_view.py
import tkinter as tk
from tkinter import ttk, filedialog
from beep import Beep
import os.path


class MenuView(tk.Menu):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent
        self.conf = parent.conf

        #self.latestFiles = 

        self.latestFiles = []
        self.mempad_menu = tk.Menu(self, tearoff=0)
        file_menu = tk.Menu(self, tearoff=0)
       # page_menu = tk.Menu(self, tearoff=0)
       # export_menu = tk.Menu(self, tearoff=0)
        settings_menu = tk.Menu(self, tearoff=0)

        self.open_file = tk.IntVar()
       
        last_file = self.conf.get('Main','MRU')
        for i,file in enumerate(self.conf.get('Main','LatestFiles').strip().split("\n")):
            
            self.add_open_mempad_file_item(file)
            if last_file == file:
                self.open_file.set(i) 

         
        self.add_cascade(label="MemPad", menu=self.mempad_menu)

        file_menu.add_command(label="Open", accelerator="Ctrl+O",command=self.open_file_dialog)
        file_menu.add_command(label="New", accelerator="Ctrl+N",command=self.save_new_file_dialog)
        file_menu.add_command(label="Save", accelerator="Ctrl+S",command=self.bindcmd('save'))
        file_menu.add_command(label="Save as...", command=self.save_file_as_dialog)
 
        file_menu.add_command(label="Exit", accelerator="ESC", command= self.bindcmd('exit') )
 
        
 
        self.add_cascade(label="File", menu=file_menu)

        exit_on_esc = tk.BooleanVar()
        settings_menu.add_checkbutton(
            label="Exit on ESC", 
            command=lambda: self.cmd('settings','exit_on_esc', exit_on_esc),
            variable=exit_on_esc
        )
        auto_save = tk.BooleanVar()
        settings_menu.add_checkbutton(
            label="Auto Save", 
            command=lambda: self.cmd('settings','auto_save', auto_save),
            variable=auto_save
        )
        always_on_top = tk.BooleanVar()
        settings_menu.add_checkbutton(
            label="Always on top", 
            command=lambda: self.cmd('settings','always_on_top', always_on_top),
            variable=always_on_top
        )


        theme_menu = tk.Menu(self, tearoff=False)
        theme = tk.IntVar()
        theme.set(1)  # Default theme ("Light".)
        theme_menu.add_radiobutton(
            label="Light",
            variable=theme,
            value=1,
            command=lambda: self.cmd('settings','theme_changed', 1),
        )
        theme_menu.add_radiobutton(
            label="Dark",
            value=2,
            variable=theme,
            command=lambda: self.cmd('settings','theme_changed', 2),
            
        )
        settings_menu.add_cascade(menu=theme_menu, label="Theme")

       # self.add_cascade(label="Settings", menu=settings_menu)

        # self.add_cascade(label="Page", menu=page_menu)
        # self.add_cascade(label="Export", menu=export_menu)
        # self.add_cascade(label="Settings", menu=settings_menu)

        self.parent.config(menu=self)

    def open_file_dialog(self):
        file_path = filedialog.askopenfilename()
        if file_path:
            self.cmd('open_mempad_file', file_path)

    def save_file_as_dialog(self):

        file_path = filedialog.asksaveasfilename(defaultextension=".lst", title="Save file as...")
        if file_path:
            
            self.cmd('save_as_mempad_file', file_path)

    def save_new_file_dialog(self):

        file_path = filedialog.asksaveasfilename(defaultextension=".lst", confirmoverwrite=False , title="Save NEW file as...")
        if file_path:
            self.cmd('save_as_new_mempad_file', file_path)

    def cmd(self, *args):
        Beep.dispatch('command', *args)

    def bindcmd(self, action, *args):
        return lambda: Beep.dispatch('command', action, *args)
    
    def add_open_mempad_file_item(self, file, add_first = False):
        
        if not file in self.latestFiles and os.path.isfile(file):
         
            self.mempad_menu.add_radiobutton(
                label=file,
                variable=self.open_file,
                value= len(self.latestFiles),
                command=self.bindcmd('open_mempad_file', file),
            )

            if add_first :
                self.latestFiles.insert(0, file)
            else:    
                self.latestFiles.append(file)

            conf_value = "\n".join(self.latestFiles)
            self.conf.set('Main','LatestFiles', conf_value) 

        # we update the menu checked item
        for i, latest_file in enumerate(self.latestFiles):
            if file == latest_file:
                self.open_file.set(i)
        
