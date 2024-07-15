import tkinter as tk
from tkinter import filedialog, simpledialog
from pathlib import Path


class ExportDialog(simpledialog.Dialog):

    def __init__(self, parent, default_title):

        self.default_title =  Path(default_title).stem 
        self.default_folder =  Path(default_title).parent 
        super().__init__(parent)

    def body(self, master):
        self.title("Export...")

        # Format Selection
        tk.Label(master, text="Select Format:").grid(row=0, column=0, sticky=tk.W)
        self.format_var = tk.StringVar(value="Markdown")
        tk.Radiobutton(master, text="Markdown", variable=self.format_var, value="Markdown").grid(row=1, column=0, sticky=tk.W)
        tk.Radiobutton(master, text="HTML", variable=self.format_var, value="HTML").grid(row=1, column=1, sticky=tk.W)
        tk.Radiobutton(master, text="Text", variable=self.format_var, value="Text").grid(row=1, column=2, sticky=tk.W)

        # File Number Selection
        tk.Label(master, text="Number of Files:").grid(row=2, column=0, sticky=tk.W)
        self.file_var = tk.StringVar(value="One file")
        tk.Radiobutton(master, text="One file", variable=self.file_var, value="One file").grid(row=3, column=0, sticky=tk.W)
        # tk.Radiobutton(master, text="Split level 1", variable=self.file_var, value="Split level 1").grid(row=3, column=1, sticky=tk.W)

        # Options
        self.autotitle_var = tk.BooleanVar(value = True)
        self.add_page_title_var = tk.BooleanVar(value = True)
        tk.Checkbutton(master, text="Autotitle", variable=self.autotitle_var).grid(row=4, column=0, sticky=tk.W)
        tk.Checkbutton(master, text="Add Page Title", variable=self.add_page_title_var).grid(row=4, column=1, sticky=tk.W)

        # Document Title
        tk.Label(master, text="Document Title:").grid(row=5, column=0, sticky=tk.W)
        self.doc_title_entry = tk.Entry(master)
        self.doc_title_entry.insert(0, self.default_title) 
        self.doc_title_entry.grid(row=5, column=1, columnspan=2, sticky=tk.W+tk.E)

        # Export Folder
        tk.Label(master, text="Export Folder:").grid(row=6, column=0, sticky=tk.W)
        self.folder_var = tk.StringVar() 
        self.folder_var.set(self.default_folder)
        tk.Entry(master, textvariable=self.folder_var).grid(row=6, column=1, sticky=tk.W+tk.E)
        tk.Button(master, text="Browse", command=self.select_folder).grid(row=6, column=2)

        return self.doc_title_entry  # initial focus

    def apply(self):
        self.result = {
            "format": self.format_var.get(),
            "file_choice": self.file_var.get(),
            "autotitle": self.autotitle_var.get(),
            "add_page_title": self.add_page_title_var.get(),
            "doc_title": self.doc_title_entry.get(),
            "export_folder": self.folder_var.get()
        }

    def select_folder(self):
        folder_selected = filedialog.askdirectory(initialdir= self.default_folder)
        self.folder_var.set(folder_selected)

 

  
