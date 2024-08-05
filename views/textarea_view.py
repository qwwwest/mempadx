# views/textarea_view.py
import tkinter as tk
import tkinter.font as tkfont
from tkinter import ttk

import re

class TextAreaView(tk.Frame):
    def __init__(self, parent):

        super().__init__(parent)

        self._renderMarkdown = False
        self.font_name = "TkFixedFont"
        self.font_size = 16
        self.pack(expand=True, fill=tk.BOTH)
        text_font = tkfont.Font(family=self.font_name, size= self.font_size)
        self.text = tk.Text(self, undo=True, font=text_font, wrap = tk.WORD)

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
        print('selectaaaall')
        self.text.tag_add(tk.SEL, "1.0", tk.END)
        self.text.mark_set(tk.INSERT, "1.0")
        self.text.see(tk.INSERT)
        return 'break'      
        
     
    def config(self):
        
        default_font = tkfont.nametofont(self.font_name)


        default_size = self.font_size
        bold_font = tkfont.Font(**default_font.configure())
        italic_font = tkfont.Font(**default_font.configure())
        link_font = tkfont.Font(**default_font.configure())

        h1_font = tkfont.Font(**default_font.configure())
        h2_font = tkfont.Font(**default_font.configure())
        h3_font = tkfont.Font(**default_font.configure())


        bold_font.configure(weight="bold" ,size = default_size )
        italic_font.configure(slant="italic", size = default_size)
        link_font.configure(size = default_size,  underline=True)

        h1_font.configure(size=int(default_size*1.8), weight="bold")
        h2_font.configure(size=int(default_size*1.4), weight="bold")
        h3_font.configure(size=int(default_size*1.2), weight="bold")


        self.text.tag_configure("bold", font=bold_font)
        self.text.tag_configure("italic", font=italic_font)
        self.text.tag_configure("link", font=link_font)

        self.text.tag_configure("h1", font=h1_font, spacing3=default_size)
        self.text.tag_configure("h2", font=h2_font, spacing3=default_size)
        self.text.tag_configure("h3", font=h3_font, spacing3=default_size)
  
         

    def clear_tags(self):
        self.text.tag_remove('h1', "1.0", tk.END)
        self.text.tag_remove('h2', "1.0", tk.END)
        self.text.tag_remove('h3', "1.0", tk.END)
        self.text.tag_remove('bold', "1.0", tk.END)
        self.text.tag_remove('italic', "1.0", tk.END)
        self.text.tag_remove('link', "1.0", tk.END)
    
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

        self.re_replace_all(r'(^| )(\*\*.+?\*\*)(?!\*)', 'bold')
        self.re_replace_all(r' _(.+?)_ ', 'italic')
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