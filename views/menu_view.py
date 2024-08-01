# views/menu_view.py
import tkinter as tk
from tkinter import ttk, filedialog
from beep import Beep
from settings import MemPadSettings
import os.path


class MenuView(tk.Menu):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent
        self.conf = parent.conf
        self.settings = MemPadSettings.get_instance()
        #self.latestFiles = 

        self.latestFiles = []
        self.mempad_menu = tk.Menu(self, tearoff=0)
        file_menu = tk.Menu(self, tearoff=0)
       # page_menu = tk.Menu(self, tearoff=0)
       # export_menu = tk.Menu(self, tearoff=0)
        settings_menu = tk.Menu(self, tearoff=0)

        self.open_file = tk.IntVar()
       
        last_file = self.conf.getValue('MRU')
        nLatestFile = self.conf.getValue('LatestFiles').strip().split("\n")
        if not last_file in nLatestFile:
            nLatestFile.append(last_file)

        num_keep = self.conf.getValue('NumKeep','int') 
        nLatestFile = nLatestFile[ -num_keep:] 

        for i,file in enumerate(nLatestFile):
            
            self.add_open_mempad_file_item(file)
            if last_file == file:
                self.open_file.set(i) 

         
        # self.add_cascade(label="✖")
        # self.add_cascade(label="▢")
        # self.add_cascade(label="_")
        self.add_cascade(label="MemPad", menu=self.mempad_menu)

        file_menu.add_command(label="Open", accelerator="Ctrl+O",command=self.open_file_dialog)
        file_menu.add_command(label="New", accelerator="Ctrl+N",command=self.save_new_file_dialog)
        file_menu.add_command(label="Save", accelerator="Ctrl+S",command=self.bindcmd('save'))
        file_menu.add_command(label="Save as...", command=self.save_file_as_dialog)
        file_menu.add_separator( )
        file_menu.add_command(label="Export...", command= self.bindcmd('open_export_dialog') )
        file_menu.add_separator( )
        file_menu.add_command(label="Exit", command= self.bindcmd('exit') )
 
        
        self.add_cascade(label="File", menu=file_menu)

        # OnTop = 0
        # ExitEsc = 0
        # AutoSave = 0
        # NoBackup = 1
        settings_menu.add_checkbutton(
            label="Render Markdown Live", 
            command= self.bindcmd('settings-update','renderMarkdown'),
            variable= self.conf.getVariable('renderMarkdown', 'bool')
        )

        settings_menu.add_checkbutton(
            label="Exit on ESC", 
            command= self.bindcmd('settings-update','ExitEsc'),
            variable= self.conf.getVariable('ExitEsc', 'bool')
        )

        settings_menu.add_checkbutton(
            label="Auto Save", 
            command= self.bindcmd('settings-update','AutoSave'),
            variable= self.conf.getVariable('AutoSave', 'bool')
        )
        settings_menu.add_checkbutton(
            label="Always On Top", 
            command= self.bindcmd('settings-update','OnTop'),
            variable= self.conf.getVariable('OnTop', 'bool')
        )
 
        settings_menu.add_checkbutton(
            label="No BackUp", 
            command= self.bindcmd('settings-update','NoBackup'),
            variable= self.conf.getVariable('NoBackup', 'bool')
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
        # settings_menu.add_cascade(menu=theme_menu, label="Theme")

        self.add_cascade(label="Settings", menu=settings_menu)

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
    
    def add_open_mempad_file_item(self, file):
        if file == '':
            return
 
        abspath = os.path.abspath(file)
        
        if not file in self.latestFiles and os.path.isfile(abspath):
         
            self.mempad_menu.add_radiobutton(
                label=file,
                variable=self.open_file,
                value= len(self.latestFiles),
                command=self.bindcmd('open_mempad_file', file),
            )
     
            
            self.latestFiles.append(file)

            num_keep = self.conf.getValue('NumKeep','int') 
            conf_value = "\n".join(self.latestFiles[ -num_keep:])

            self.conf.setValue('LatestFiles', conf_value ) 
            

 
        # we update the menu checked item
        for i, latest_file in enumerate(self.latestFiles):
            if file == latest_file:
                self.open_file.set(i)
 