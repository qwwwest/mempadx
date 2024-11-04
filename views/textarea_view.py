# views/textarea_view.py
import tkinter as tk
import tkinter.font as tkfont
from tkinter import ttk
from tkinter import messagebox
import os
import re

class TextAreaView(tk.Frame):
    def __init__(self, parent):

        super().__init__(parent)

        self._renderMarkdown = False
        # was self.font_name = "TkFixedFont"
        # Define a monospace font for cross-platform consistency

        self.font_name = "Courier"
        
        # Check if "DejaVu Sans Mono" is installed
        if "DejaVu Sans Mono" in tkfont.families():
            self.font_name = "DejaVu Sans Mono"
        # Check if "Source Code Pro" is installed
        if "Source Code Pro" in tkfont.families():
            self.font_name = "Source Code Pro"
     
            

        self.font_size = 16
        self.pack(expand=True, fill=tk.BOTH)
        
       
        self.monospace = tkfont.Font(family=self.font_name, size=self.font_size )

    
        self.text = tk.Text(self, undo=True, font= self.monospace , wrap = tk.WORD)

        # Create a vertical scrollbar
        self.scrollbar = ttk.Scrollbar(self, orient=tk.VERTICAL, command=self.text.yview)
        self.text.configure(yscrollcommand=self.scrollbar.set)
        
        # Pack the tree and the scrollbar
        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        self.text.pack(expand=True, fill=tk.BOTH)

            # Add the binding
        self.text.bind("<Control-a>", self.select_all )
 
        self.text.bind("<KeyRelease>", self.setSimpleMarkdown)

        
        self.config()
       

    def current_cursor_position(self):
        count = len(self.text.get("1.0", tk.INSERT))
        return count
    
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
        self.setSimpleMarkdown('blep')

    # Select all the text in textbox
    def select_all(self, _):
        
        self.text.tag_add(tk.SEL, "1.0", tk.END)
        self.text.mark_set(tk.INSERT, "1.0")
        self.text.see(tk.INSERT)
        return 'break'      
        
    # get the selected text, None if nothing
    def get_selected_text(self, *_):
        if self.text.tag_ranges(tk.SEL):
            return self.text.get(tk.SEL_FIRST, tk.SEL_LAST)
        
        return None      
    


    def config(self):
        
        yellow = "#ffeeaa"
        yellow2 = "#ffffCC"
        green = "#88ffcc"
        blue = "#ccccff"
 
        h1_font = tkfont.Font(family=self.font_name, size=int(self.font_size * 1.6), weight="bold" )
        h2_font = tkfont.Font(family=self.font_name, size=int(self.font_size * 1.2), weight="bold")
        h3_font = tkfont.Font(family=self.font_name, size=int(self.font_size * 1.1), weight="bold")
        bold_font = tkfont.Font(family=self.font_name,size = self.font_size, weight="bold")
        italic_font = tkfont.Font(family=self.font_name,size = self.font_size, slant="italic")
        link_font = tkfont.Font(family=self.font_name,size = self.font_size, underline=True)
        
        shortcode_font = tkfont.Font(family=self.font_name, size=int(self.font_size * 1.2), weight="bold")
 
        self.text.tag_configure("bold", font=bold_font)
        self.text.tag_configure("italic", font=italic_font)
        self.text.tag_configure("link", font=link_font, foreground=blue)

        
        self.text.tag_configure("h1", font=h1_font, foreground=yellow)
        self.text.tag_configure("h2", font=h2_font,   foreground=yellow)
        self.text.tag_configure("h3", font=h3_font,   foreground=yellow)
        self.text.tag_configure("shortcode", font=shortcode_font,   foreground=green)
  
         

    def clear_tags(self):
        self.text.tag_remove('h1', "1.0", tk.END)
        self.text.tag_remove('h2', "1.0", tk.END)
        self.text.tag_remove('h3', "1.0", tk.END)
        self.text.tag_remove('bold', "1.0", tk.END)
        self.text.tag_remove('italic', "1.0", tk.END)
        self.text.tag_remove('link', "1.0", tk.END)
        self.text.tag_remove('shortcode', "1.0", tk.END)
    
    def renderMarkdown(self, state):
        self._renderMarkdown = state
        
        if self._renderMarkdown:
            self.setSimpleMarkdown('blep')
        else:    
            self.clear_tags()

    def setSimpleMarkdown(self,_):

        if not self._renderMarkdown:
            return
         
        self.clear_tags()

        self.re_replace_all(r'^# (.+?)$', 'h1')
        self.re_replace_all(r'^## (.+?)$', 'h2')
        self.re_replace_all(r'^### (.+?)$', 'h3')
        self.re_replace_all(r'^\[(.+?)\]$', 'shortcode')
        self.re_replace_all(r'^\[@@@(.+?)$', 'shortcode')
        self.re_replace_all(r'^(.*?)@@@\]$', 'shortcode')

        self.re_replace_all(r'(^| )(\*\*.+?\*\*)(?!\*)', 'bold')
        self.re_replace_all(r' _(.+?)_', 'italic')
        self.re_replace_all(r'http[s]?\://[a-zA-Z0-9-./?=]+', 'link')
        

            
    
    def re_replace_all(self, pattern, tag):
        for match in self.search_re(pattern):
            self.text.tag_add(tag, match[0], match[1])
            

    def search_re(self, pattern):
        """
        Uses the python re library to match patterns.

        Arguments:
            pattern - The pattern to match.
        Return value:
            A list of tuples containing the start and end indices of the matches.
            e.g. [("0.4", "5.9"]
        """
        matches = []
        text = self.text.get("1.0", tk.END).splitlines()
        for i, line in enumerate(text):
            for match in re.finditer(pattern, line):
                matches.append((f"{i + 1}.{match.start()}", f"{i + 1}.{match.end()}"))
                
        return matches
    
    def highlight_text(self, start_pos, end_pos):

        self.text.tag_remove('highlight', '1.0', tk.END)
        if start_pos == None:
            return
        self.text.tag_add('highlight', start_pos, end_pos)
        self.text.tag_config('highlight', background='yellow')
        self.text.mark_set(tk.INSERT, end_pos)
        self.text.see(start_pos)